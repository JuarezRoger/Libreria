from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.nombre} ({self.sku})"