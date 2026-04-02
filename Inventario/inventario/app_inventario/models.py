from django.db import models, transaction
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Repuesto(models.Model):
    numero_parte = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    unidad_medida = models.CharField(max_length=20, blank=True)
    minimo_reposicion = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.numero_parte})"

    def total_stock(self):
        # calcula sumatoria de stock en todas las ubicaciones
        return self.stocks.aggregate(total=models.Sum('cantidad'))['total'] or 0


class Ubicacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Stock(models.Model):
    repuesto = models.ForeignKey(Repuesto, related_name='stocks', on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion, related_name='stocks', on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.IntegerField(default=0)

    class Meta:
        unique_together = ('repuesto', 'ubicacion')

    def __str__(self):
        loc = self.ubicacion.nombre if self.ubicacion else "Sin ubicación"
        return f"{self.repuesto} @ {loc}: {self.cantidad}"


class Movimiento(models.Model):
    TIPO_ENTRADA = 'ENT'
    TIPO_SALIDA = 'SAL'
    TIPO_AJUSTE = 'ADJ'
    TIPO_TRANSFER = 'TRF'
    TIPO_CHOICES = [
        (TIPO_ENTRADA, 'Entrada'),
        (TIPO_SALIDA, 'Salida'),
        (TIPO_AJUSTE, 'Ajuste'),
        (TIPO_TRANSFER, 'Transferencia'),
    ]

    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES)
    fecha = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    referencia = models.CharField(max_length=200, blank=True)
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.fecha.date()} - {self.referencia or self.id}"


class MovimientoItem(models.Model):
    movimiento = models.ForeignKey(Movimiento, related_name='items', on_delete=models.CASCADE)
    repuesto = models.ForeignKey(Repuesto, on_delete=models.PROTECT)
    ubicacion_origen = models.ForeignKey(Ubicacion, related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    ubicacion_destino = models.ForeignKey(Ubicacion, related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.repuesto} x {self.cantidad}"

    def apply(self):
        """
        Aplica este item al stock. Debe ejecutarse dentro de una transacción atómica
        y con select_for_update cuando sea una operación que reduzca stock.
        """
        # Caso entrada: sumar a ubicacion_destino (o a null-location si no se usan ubicaciones)
        if self.movimiento.tipo == Movimiento.TIPO_ENTRADA:
            dest = self.ubicacion_destino
            stock, _ = Stock.objects.select_for_update().get_or_create(repuesto=self.repuesto, ubicacion=dest)
            stock.cantidad = stock.cantidad + self.cantidad
            stock.save()
        elif self.movimiento.tipo == Movimiento.TIPO_SALIDA:
            orig = self.ubicacion_origen
            stock = Stock.objects.select_for_update().get(repuesto=self.repuesto, ubicacion=orig)
            if stock.cantidad < self.cantidad:
                raise ValueError(f"Stock insuficiente para {self.repuesto} en {orig} (tiene {stock.cantidad}, pide {self.cantidad})")
            stock.cantidad = stock.cantidad - self.cantidad
            stock.save()
        elif self.movimiento.tipo == Movimiento.TIPO_AJUSTE:
            # Ajuste hacia cantidad (puedes definir lógica distinta: sumar/restar)
            dest = self.ubicacion_destino or self.ubicacion_origen
            stock, _ = Stock.objects.select_for_update().get_or_create(repuesto=self.repuesto, ubicacion=dest)
            stock.cantidad = stock.cantidad + self.cantidad
            stock.save()
        elif self.movimiento.tipo == Movimiento.TIPO_TRANSFER:
            # Mover desde origen a destino
            orig = self.ubicacion_origen
            dest = self.ubicacion_destino
            if orig is None or dest is None:
                raise ValueError("Transferencia requiere origen y destino")
            stock_orig = Stock.objects.select_for_update().get(repuesto=self.repuesto, ubicacion=orig)
            if stock_orig.cantidad < self.cantidad:
                raise ValueError("Stock insuficiente para transferir")
            stock_dest, _ = Stock.objects.select_for_update().get_or_create(repuesto=self.repuesto, ubicacion=dest)
            stock_orig.cantidad -= self.cantidad
            stock_dest.cantidad += self.cantidad
            stock_orig.save()
            stock_dest.save()


# Opcional: helper para aplicar un movimiento completo atómicamente
def apply_movimiento(movimiento: Movimiento):
    """
    Aplica todos los items de un movimiento dentro de una transacción atómica.
    Lanza excepción si alguna aplicación falla.
    """
    with transaction.atomic():
        # Bloquea filas de stock necesarias individualmente dentro de cada item
        for item in movimiento.items.select_related('repuesto', 'ubicacion_origen', 'ubicacion_destino').all():
            item.apply()