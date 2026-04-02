from django.db import models


class Almacen(models.Model):
    nombre = models.CharField(max_length=255)
    ubicacion = models.CharField(max_length=255, blank=True)
    capacidad = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.nombre}"