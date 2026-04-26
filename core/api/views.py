from rest_framework import viewsets
from ..models import Banco, Cliente, Credito
from .serializers import BancoSerializer, ClienteSerializer, CreditoSerializer
from .filters import BancoFilter, ClienteFilter, CreditoFilter


class BancoViewSet(viewsets.ModelViewSet):
    queryset = Banco.objects.all()
    serializer_class = BancoSerializer
    filterset_class = BancoFilter
    search_fields = ['nombre', 'direccion']
    ordering_fields = ['nombre', 'tipo_banco']
    ordering = ['nombre']


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.select_related('banco').all()
    serializer_class = ClienteSerializer
    filterset_class = ClienteFilter
    search_fields = ['nombre_completo', 'email', 'telefono']
    ordering_fields = ['nombre_completo', 'edad', 'fecha_nacimiento']
    ordering = ['nombre_completo']


class CreditoViewSet(viewsets.ModelViewSet):
    queryset = Credito.objects.select_related('cliente', 'banco').all()
    serializer_class = CreditoSerializer
    filterset_class = CreditoFilter
    search_fields = ['descripcion', 'cliente__nombre_completo']
    ordering_fields = ['fecha_registro', 'pago_minimo', 'pago_maximo', 'plazo_meses']
    ordering = ['-fecha_registro']