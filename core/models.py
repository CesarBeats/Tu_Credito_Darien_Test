"""Modelos de datos de la app core: Banco, Cliente y Crédito."""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Banco(models.Model):
    """Entidad bancaria que puede ser de tipo privado o de gobierno."""
    class TipoBanco(models.TextChoices):
        PRIVADO = 'PRIVADO', 'Privado'
        GOBIERNO = 'GOBIERNO', 'Gobierno'

    nombre = models.CharField()
    tipo_banco = models.CharField(choices=TipoBanco.choices)
    direccion = models.CharField(blank=True)

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} ({self.get_tipo_banco_display()})'


class Cliente(models.Model):
    """Persona natural o jurídica asociada a un banco, con datos de contacto."""
    class TipoPersona(models.TextChoices):
        NATURAL = 'NATURAL', 'Natural'
        JURIDICO = 'JURIDICO', 'Jurídico'

    nombre_completo = models.CharField()
    fecha_nacimiento = models.DateField()
    edad = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        blank=True,
        null=True,
    )
    nacionalidad = models.CharField(blank=True)
    direccion = models.CharField(blank=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(blank=True)
    tipo_persona = models.CharField(choices=TipoPersona.choices, blank=True)
    banco = models.ForeignKey(
        Banco,
        on_delete=models.SET_NULL,
        related_name='clientes',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre_completo']

    def __str__(self):
        return self.nombre_completo


class Credito(models.Model):
    """Producto crediticio vinculado a un cliente y un banco."""
    class TipoCredito(models.TextChoices):
        AUTOMOTRIZ = 'AUTOMOTRIZ', 'Automotriz'
        HIPOTECARIO = 'HIPOTECARIO', 'Hipotecario'
        COMERCIAL = 'COMERCIAL', 'Comercial'

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='créditos')
    descripcion = models.TextField()
    pago_minimo = models.DecimalField(max_digits=12, decimal_places=2)
    pago_maximo = models.DecimalField(max_digits=12, decimal_places=2)
    plazo_meses = models.PositiveIntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    banco = models.ForeignKey(Banco, on_delete=models.PROTECT, related_name='créditos')
    tipo_credito = models.CharField(choices=TipoCredito.choices, blank=True)

    class Meta:
        verbose_name = 'Crédito'
        verbose_name_plural = 'Créditos'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f'{self.cliente.nombre_completo} – {self.get_tipo_credito_display()} ({self.banco.nombre})'
