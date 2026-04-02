from rest_framework import viewsets
from .serializers import (
    RepuestoSerializer,
    UbicacionSerializer,
    StockSerializer,
    MovimientoSerializer,
    MovimientoItemSerializer,
)
from app_inventario.models import Repuesto, Ubicacion, Stock, Movimiento, MovimientoItem


class RepuestoViewSet(viewsets.ModelViewSet):
    queryset = Repuesto.objects.all()
    serializer_class = RepuestoSerializer


class UbicacionViewSet(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer


class MovimientoItemViewSet(viewsets.ModelViewSet):
    queryset = MovimientoItem.objects.all()
    serializer_class = MovimientoItemSerializer