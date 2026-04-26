# Unit tests for api views.
import pytest
from django.db.models import ProtectedError
from ...models import Banco, Cliente, Credito
from rest_framework import status
from datetime import timedelta


# ---------------------------------------------------------------------------
# ViewSet tests – BancoViewSet
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestBancoViewSet:
    base_url = "/api/bancos/"

    def test_list_returns_200(self, auth_client, banco):
        response = auth_client.get(self.base_url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_contains_banco(self, auth_client, banco):
        response = auth_client.get(self.base_url)
        nombres = [b["nombre"] for b in (response.data["results"] if "results" in response.data else response.data)]
        data = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        nombres = [b["nombre"] for b in data]
        assert "Banco Nacional" in nombres

    def test_create_banco(self, auth_client, db):
        payload = {"nombre": "Nuevo Banco", "tipo_banco": "PRIVADO", "direccion": "Calle 1"}
        response = auth_client.post(self.base_url, payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Banco.objects.filter(nombre="Nuevo Banco").exists()

    def test_retrieve_banco(self, auth_client, banco):
        response = auth_client.get(f"{self.base_url}{banco.pk}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["nombre"] == "Banco Nacional"

    def test_update_banco(self, auth_client, banco):
        payload = {"nombre": "Banco Actualizado", "tipo_banco": "GOBIERNO"}
        response = auth_client.put(f"{self.base_url}{banco.pk}/", payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        banco.refresh_from_db()
        assert banco.nombre == "Banco Actualizado"

    def test_partial_update_banco(self, auth_client, banco):
        response = auth_client.patch(f"{self.base_url}{banco.pk}/", {"direccion": "Nueva Dir"}, format="json")
        assert response.status_code == status.HTTP_200_OK
        banco.refresh_from_db()
        assert banco.direccion == "Nueva Dir"

    def test_delete_banco(self, auth_client, banco):
        pk = banco.pk
        response = auth_client.delete(f"{self.base_url}{banco.pk}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Banco.objects.filter(pk=pk).exists()

    def test_retrieve_nonexistent_returns_404(self, auth_client, db):
        response = auth_client.get(f"{self.base_url}9999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_ordering_by_nombre(self, auth_client, banco, banco_gobierno):
        response = auth_client.get(self.base_url + "?ordering=nombre")
        assert response.status_code == status.HTTP_200_OK

    def test_search_by_nombre(self, auth_client, banco):
        response = auth_client.get(self.base_url + "?search=Nacional")
        data = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        assert any("Nacional" in b["nombre"] for b in data)


# ---------------------------------------------------------------------------
# ViewSet tests – ClienteViewSet
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestClienteViewSet:
    base_url = "/api/clientes/"

    def test_list_returns_200(self, auth_client, cliente):
        response = auth_client.get(self.base_url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_cliente(self, auth_client, db, banco):
        payload = {
            "nombre_completo": "Carlos López",
            "fecha_nacimiento": "1995-07-10",
            "email": "carlos@example.com",
            "banco": banco.pk,
            "tipo_persona": "NATURAL",
        }
        response = auth_client.post(self.base_url, payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Cliente.objects.filter(email="carlos@example.com").exists()

    def test_create_cliente_email_duplicado(self, auth_client, db, cliente):
        payload = {
            "nombre_completo": "Otro",
            "fecha_nacimiento": "2000-01-01",
            "email": "ana@example.com",  # ya existe
        }
        response = auth_client.post(self.base_url, payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_retrieve_cliente(self, auth_client, cliente):
        response = auth_client.get(f"{self.base_url}{cliente.pk}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == "ana@example.com"

    def test_update_cliente(self, auth_client, cliente, banco):
        payload = {
            "nombre_completo": "Ana Actualizada",
            "fecha_nacimiento": "1990-05-15",
            "email": "ana_nueva@example.com",
            "banco": banco.pk,
        }
        response = auth_client.put(f"{self.base_url}{cliente.pk}/", payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        cliente.refresh_from_db()
        assert cliente.nombre_completo == "Ana Actualizada"

    def test_partial_update_telefono(self, auth_client, cliente):
        response = auth_client.patch(f"{self.base_url}{cliente.pk}/", {"telefono": "0424-9999999"}, format="json")
        assert response.status_code == status.HTTP_200_OK
        cliente.refresh_from_db()
        assert cliente.telefono == "0424-9999999"

    def test_delete_cliente_sin_creditos(self, auth_client, cliente_sin_banco):
        pk = cliente_sin_banco.pk
        response = auth_client.delete(f"{self.base_url}{pk}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Cliente.objects.filter(pk=pk).exists()

    def test_delete_cliente_con_credito_falla(self, auth_client, cliente, credito):
        with pytest.raises(ProtectedError):
            auth_client.delete(f"{self.base_url}{cliente.pk}/")
        # PROTECT impide la eliminación; la respuesta puede ser 400 o 500 según el manejo de excepciones
        assert Cliente.objects.filter(id=cliente.pk).exists()

    def test_search_by_email(self, auth_client, cliente):
        response = auth_client.get(self.base_url + "?search=ana@example.com")
        data = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        assert any(c["email"] == "ana@example.com" for c in data)

    def test_ordering_by_edad(self, auth_client, cliente):
        response = auth_client.get(self.base_url + "?ordering=edad")
        assert response.status_code == status.HTTP_200_OK

    def test_select_related_banco_no_extra_queries(self, auth_client, cliente, django_assert_num_queries):
        # El queryset usa select_related('banco'), por lo que un solo query debe bastar
        with django_assert_num_queries(1):
            auth_client.get(f"{self.base_url}{cliente.pk}/")


# ---------------------------------------------------------------------------
# ViewSet tests – CreditoViewSet
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestCreditoViewSet:
    base_url = "/api/creditos/"

    def test_list_returns_200(self, auth_client, credito):
        response = auth_client.get(self.base_url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_credito(self, auth_client, db, cliente, banco):
        payload = {
            "cliente": cliente.pk,
            "banco": banco.pk,
            "descripcion": "Crédito automotriz",
            "pago_minimo": "200.00",
            "pago_maximo": "800.00",
            "plazo_meses": 36,
            "tipo_credito": "AUTOMOTRIZ",
        }
        response = auth_client.post(self.base_url, payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_retrieve_credito(self, auth_client, credito):
        response = auth_client.get(f"{self.base_url}{credito.pk}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["plazo_meses"] == 120

    def test_update_credito(self, auth_client, credito, cliente, banco):
        payload = {
            "cliente": cliente.pk,
            "banco": banco.pk,
            "descripcion": "Actualizado",
            "pago_minimo": "300.00",
            "pago_maximo": "900.00",
            "plazo_meses": 60,
            "tipo_credito": "COMERCIAL",
        }
        response = auth_client.put(f"{self.base_url}{credito.pk}/", payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        credito.refresh_from_db()
        assert credito.plazo_meses == 60

    def test_partial_update_descripcion(self, auth_client, credito):
        response = auth_client.patch(
            f"{self.base_url}{credito.pk}/",
            {"descripcion": "Nueva descripción"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        credito.refresh_from_db()
        assert credito.descripcion == "Nueva descripción"

    def test_delete_credito(self, auth_client, credito):
        pk = credito.pk
        response = auth_client.delete(f"{self.base_url}{credito.pk}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Credito.objects.filter(pk=pk).exists()

    def test_ordering_default_fecha_registro_desc(self, auth_client, db, cliente, banco):
        c1 = Credito.objects.create(
            cliente=cliente, banco=banco,
            descripcion="A", pago_minimo=100, pago_maximo=200, plazo_meses=12,
        )
        c2 = Credito.objects.create(
            cliente=cliente, banco=banco,
            descripcion="B", pago_minimo=100, pago_maximo=200, plazo_meses=12,
        )
        # Assert fecha_registro for c1 is older than c2.
        c1.fecha_registro = c1.fecha_registro - timedelta(seconds=1)
        c1.save(update_fields=['fecha_registro'])
        response = auth_client.get(self.base_url)
        data = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        assert data[0]["id"] == c2.pk  # más reciente primero

    def test_search_by_descripcion(self, auth_client, credito):
        response = auth_client.get(self.base_url + "?search=hipotecario")
        data = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        assert len(data) >= 1

    def test_search_by_nombre_cliente(self, auth_client, credito):
        response = auth_client.get(self.base_url + "?search=Ana")
        data = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        assert len(data) >= 1

    def test_ordering_by_pago_minimo(self, auth_client, credito):
        response = auth_client.get(self.base_url + "?ordering=pago_minimo")
        assert response.status_code == status.HTTP_200_OK

    def test_select_related_no_extra_queries(self, auth_client, credito, django_assert_num_queries):
        # select_related('cliente', 'banco') → un solo query por detalle
        with django_assert_num_queries(1):
            auth_client.get(f"{self.base_url}{credito.pk}/")

    def test_create_sin_cliente_falla(self, auth_client, db, banco):
        payload = {
            "banco": banco.pk,
            "descripcion": "Sin cliente",
            "pago_minimo": "100.00",
            "pago_maximo": "500.00",
            "plazo_meses": 12,
        }
        response = auth_client.post(self.base_url, payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
