import django_filters
from ..models import Banco, Cliente, Credito

class BancoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr="icontains")
    tipo_banco = django_filters.ChoiceFilter(choices=Banco.TipoBanco.choices)
 
    class Meta:
        model = Banco
        fields = ["nombre", "tipo_banco"]


class ClienteFilter(django_filters.FilterSet):
    nombre_completo = django_filters.CharFilter(lookup_expr="icontains")
    nacionalidad = django_filters.CharFilter(lookup_expr="icontains")
    tipo_persona = django_filters.ChoiceFilter(choices=Cliente.TipoPersona.choices)
    nombre_banco = django_filters.CharFilter(field_name="banco__nombre", lookup_expr="icontains")
    tipo_banco = django_filters.ChoiceFilter(field_name="banco__tipo_banco", choices=Banco.TipoBanco.choices)
    edad_min = django_filters.NumberFilter(field_name="edad", lookup_expr="gte")
    edad_max = django_filters.NumberFilter(field_name="edad", lookup_expr="lte")
 
    class Meta:
        model = Cliente
        fields = ["nombre_completo", "nacionalidad", "tipo_persona", "nombre_banco", "tipo_banco", "edad_min", "edad_max"]


class CreditoFilter(django_filters.FilterSet):
    tipo_credito = django_filters.ChoiceFilter(choices=Credito.TipoCredito.choices)
    nombre_banco = django_filters.CharFilter(field_name="banco__name", lookup_expr="icontains")
    tipo_banco = django_filters.ChoiceFilter(field_name="banco__tipo_banco", choices=Banco.TipoBanco.choices)
    nombre_cliente = django_filters.CharFilter(field_name="cliente__nombre_completo", lookup_expr="icontains")
    pago_minimo_gte = django_filters.NumberFilter(field_name="pago_minimo", lookup_expr="gte")
    pago_maximo_lte = django_filters.NumberFilter(field_name="pago_maximo", lookup_expr="lte")
    plazo_meses_min = django_filters.NumberFilter(field_name="plazo_meses", lookup_expr="gte")
    plazo_meses_max = django_filters.NumberFilter(field_name="plazo_meses", lookup_expr="lte")
 
    class Meta:
        model = Credito
        fields = [
            "tipo_credito", "nombre_banco", "tipo_banco", "nombre_cliente",
            "pago_minimo_gte", "pago_maximo_lte", "plazo_meses_min", "plazo_meses_max",
        ]