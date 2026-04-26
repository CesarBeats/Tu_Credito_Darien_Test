"""Rutas de la API REST: registra los ViewSets de Banco, Cliente y Crédito."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BancoViewSet, ClienteViewSet, CreditoViewSet

router = DefaultRouter()
router.register('bancos', BancoViewSet, basename='banco')
router.register('clientes', ClienteViewSet, basename='cliente')
router.register('creditos', CreditoViewSet, basename='credito')

urlpatterns = [
    path('', include(router.urls)),
]