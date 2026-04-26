"""Configuración del panel de administración de Django para Banco, Cliente y Crédito."""
from django.contrib import admin
from .models import Banco, Cliente, Credito


@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    """Admin para gestión de bancos con filtro por tipo."""
    list_display = ('nombre', 'tipo_banco', 'direccion')
    list_filter = ('tipo_banco',)
    search_fields = ('nombre', 'direccion')


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """Admin para gestión de clientes con filtros por tipo de persona, banco y nacionalidad."""
    list_display = ('nombre_completo', 'email', 'telefono', 'tipo_persona', 'banco', 'edad', 'nacionalidad')
    list_filter = ('tipo_persona', 'banco', 'nacionalidad')
    search_fields = ('nombre_completo', 'email', 'telefono')
    raw_id_fields = ('banco',)


@admin.register(Credito)
class CreditoAdmin(admin.ModelAdmin):
    """Admin para gestión de créditos con filtros por tipo y banco."""
    list_display = ('cliente', 'tipo_credito', 'banco', 'pago_minimo', 'pago_maximo', 'plazo_meses', 'fecha_registro')
    list_filter = ('tipo_credito', 'banco__tipo_banco', 'banco')
    search_fields = ('cliente__nombre_completo', 'descripcion')
    raw_id_fields = ('cliente', 'banco')
    readonly_fields = ('fecha_registro',)