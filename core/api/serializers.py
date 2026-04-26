# Serializers de la app core del proyecto tu_credito.
from datetime import date
from rest_framework import serializers
from ..models import Banco, Cliente, Credito


class BancoSerializer(serializers.ModelSerializer):
    tipo_banco_display = serializers.CharField(source='get_tipo_banco_display', read_only=True)

    class Meta:
        model = Banco
        fields = ['id', 'nombre', 'tipo_banco', 'tipo_banco_display', 'direccion']


class ClienteSerializer(serializers.ModelSerializer):
    tipo_persona_display = serializers.CharField(source='get_tipo_persona_display', read_only=True)
    banco_nombre = serializers.CharField(source='banco.nombre', read_only=True)

    class Meta:
        model = Cliente
        fields = [
            'id', 'nombre_completo', 'fecha_nacimiento', 'edad', 'nacionalidad',
            'direccion', 'email', 'telefono', 'tipo_persona', 'tipo_persona_display',
            'banco', 'banco_nombre',
        ]

    def validate_edad(self, value):
        if value is not None and (value < 1 or value > 99):
            raise serializers.ValidationError('La edad debe estar entre 1 y 99 años.')
        return value

    def validate_fecha_nacimiento(self, value):
        today = date.today()
        if value >= today:
            raise serializers.ValidationError('Fecha de nacimiento debe estar en el pasado.')
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age > 99:
            raise serializers.ValidationError('Fecha de nacimiento implica una edad irrealista.')
        return value

    def validate(self, data):
        dob = data.get('fecha_nacimiento')
        age = data.get('edad')
        if dob is not None and age is not None:
            today = date.today()
            calculated_age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if abs(calculated_age - age) > 1:
                raise serializers.ValidationError(
                    {'edad': 'La edad no es congruente con la fecha de nacimiento.'}
                )
        return data


class CreditoSerializer(serializers.ModelSerializer):
    tipo_credito_display = serializers.CharField(source='get_tipo_credito_display', read_only=True)
    nombre_cliente = serializers.CharField(source='cliente.nombre_completo', read_only=True)
    nombre_banco = serializers.CharField(source='banco.nombre', read_only=True)

    class Meta:
        model = Credito
        fields = [
            'id', 'cliente', 'nombre_cliente', 'descripcion', 'pago_minimo', 'pago_maximo',
            'plazo_meses', 'fecha_registro', 'banco', 'nombre_banco',
            'tipo_credito', 'tipo_credito_display',
        ]
        read_only_fields = ['fecha_registro']

    def validate(self, data):
        min_pay = data.get('pago_minimo')
        max_pay = data.get('pago_maximo')
        if min_pay is not None and max_pay is not None:
            if min_pay > max_pay:
                raise serializers.ValidationError(
                    {'pago_minimo': 'Pago mínimo debe ser menor o igual a Pago máximo.'}
                )
        return data