# Fixtures for testing.
from decimal import Decimal
import pytest
from ..models import Banco, Cliente, Credito
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client(db, api_client):
    """Creates a user and returns an authenticated API client."""
    user = User.objects.create_user(username="testuser", password="password")
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def banco(db):
    return Banco.objects.create(
        nombre="Banco Nacional",
        tipo_banco=Banco.TipoBanco.PRIVADO,
        direccion="Av. Principal 123",
    )


@pytest.fixture
def banco_gobierno(db):
    return Banco.objects.create(
        nombre="Banco Del Estado",
        tipo_banco=Banco.TipoBanco.GOBIERNO,
    )


@pytest.fixture
def cliente(db, banco):
    return Cliente.objects.create(
        nombre_completo="Ana Gómez",
        fecha_nacimiento="1990-05-15",
        edad=34,
        nacionalidad="Venezolana",
        email="ana@example.com",
        telefono="0412-1234567",
        tipo_persona=Cliente.TipoPersona.NATURAL,
        banco=banco,
    )


@pytest.fixture
def cliente_sin_banco(db):
    return Cliente.objects.create(
        nombre_completo="Luis Pérez",
        fecha_nacimiento="1985-03-20",
        email="luis@example.com",
    )


@pytest.fixture
def credito(db, cliente, banco):
    return Credito.objects.create(
        cliente=cliente,
        banco=banco,
        descripcion="Crédito hipotecario para vivienda principal",
        pago_minimo=Decimal("500.00"),
        pago_maximo=Decimal("1500.00"),
        plazo_meses=120,
        tipo_credito=Credito.TipoCredito.HIPOTECARIO,
    )