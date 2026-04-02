from django.db import models
from django.contrib.auth import get_user_model
from productos.models import Producto
from almacenes.models import Almacen


class Movimiento(models.Model):
    TIPO_CHOICES = [
        ('IN', 'Entrada'),
        ('OUT', 'Salida'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.tipo} {self.cantidad}"