from django.db import models
from django.conf import settings
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Repuesto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='repuestos')
    numero_parte = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    unidad_medida = models.CharField(max_length=20, blank=True)
    minimo_reposicion = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.numero_parte})"

class MovimientoStock(models.Model):
    TIPO_ENTRADA = 'ENT'
    TIPO_SALIDA = 'SAL'
    TIPO_CHOICES = [
        (TIPO_ENTRADA, 'Entrada'),
        (TIPO_SALIDA, 'Salida'),
    ]
    repuesto = models.ForeignKey(Repuesto, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    referencia = models.CharField(max_length=200, blank=True)
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.repuesto} x {self.cantidad}"