# Unit tests for models.
from decimal import Decimal
import pytest
from ..models import Banco, Cliente, Credito
from datetime import timedelta
# ---------------------------------------------------------------------------
# Model tests – Banco
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestBancoModel:
    def test_str_representation(self, banco):
        assert str(banco) == "Banco Nacional (Privado)"

    def test_str_gobierno(self, banco_gobierno):
        assert str(banco_gobierno) == "Banco Del Estado (Gobierno)"

    def test_default_ordering(self, banco, banco_gobierno):
        nombres = list(Banco.objects.values_list("nombre", flat=True))
        assert nombres == sorted(nombres)

    def test_direccion_optional(self, db):
        b = Banco.objects.create(nombre="Sin Dirección", tipo_banco=Banco.TipoBanco.PRIVADO)
        assert b.direccion == ""

    def test_tipo_banco_choices(self):
        assert Banco.TipoBanco.PRIVADO == "PRIVADO"
        assert Banco.TipoBanco.GOBIERNO == "GOBIERNO"


# ---------------------------------------------------------------------------
# Model tests – Cliente
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestClienteModel:
    def test_str_representation(self, cliente):
        assert str(cliente) == "Ana Gómez"

    def test_banco_nullable(self, cliente_sin_banco):
        assert cliente_sin_banco.banco is None

    def test_email_is_unique(self, db, cliente):
        with pytest.raises(Exception):
            Cliente.objects.create(
                nombre_completo="Otro",
                fecha_nacimiento="2000-01-01",
                email="ana@example.com",  # duplicado
            )

    def test_related_name_clientes(self, banco, cliente):
        assert cliente in banco.clientes.all()

    def test_banco_set_null_on_delete(self, db, banco, cliente):
        banco.delete()
        cliente.refresh_from_db()
        assert cliente.banco is None

    def test_tipo_persona_choices(self):
        assert Cliente.TipoPersona.NATURAL == "NATURAL"
        assert Cliente.TipoPersona.JURIDICO == "JURIDICO"

    def test_edad_optional(self, db):
        c = Cliente.objects.create(
            nombre_completo="Sin Edad",
            fecha_nacimiento="1980-01-01",
            email="sinedad@example.com",
        )
        assert c.edad is None


# ---------------------------------------------------------------------------
# Model tests – Credito
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestCreditoModel:
    def test_str_representation(self, credito):
        assert str(credito) == "Ana Gómez – Hipotecario (Banco Nacional)"

    def test_fecha_registro_auto(self, credito):
        assert credito.fecha_registro is not None

    def test_related_name_creditos_cliente(self, cliente, credito):
        assert credito in cliente.créditos.all()

    def test_related_name_creditos_banco(self, banco, credito):
        assert credito in banco.créditos.all()

    def test_cliente_protected_on_delete(self, db, cliente, credito):
        from django.db.models import ProtectedError
        with pytest.raises(ProtectedError):
            cliente.delete()

    def test_banco_protected_on_delete(self, db, banco, credito):
        from django.db.models import ProtectedError
        with pytest.raises(ProtectedError):
            banco.delete()

    def test_tipo_credito_choices(self):
        assert Credito.TipoCredito.AUTOMOTRIZ == "AUTOMOTRIZ"
        assert Credito.TipoCredito.HIPOTECARIO == "HIPOTECARIO"
        assert Credito.TipoCredito.COMERCIAL == "COMERCIAL"

    def test_pago_minimo_decimal(self, credito):
        assert credito.pago_minimo == Decimal("500.00")

    def test_ordering_by_fecha_registro_desc(self, db, cliente, banco):
        c1 = Credito.objects.create(
            cliente=cliente, banco=banco,
            descripcion="Primero", pago_minimo=100, pago_maximo=200, plazo_meses=12,
            fecha_registro='2026-04-25 00:00:00',
        )
        c2 = Credito.objects.create(
            cliente=cliente, banco=banco,
            descripcion="Segundo", pago_minimo=100, pago_maximo=200, plazo_meses=12,
            fecha_registro='2026-04-25 01:00:00',
        )
        # Assert fecha_registro for c1 is older than c2.
        c1.fecha_registro = c1.fecha_registro - timedelta(seconds=1)
        c1.save(update_fields=['fecha_registro'])
        ids = list(Credito.objects.values_list("id", flat=True))
        assert ids[0] == c2.id  # el más reciente primero.