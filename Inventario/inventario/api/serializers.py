from rest_framework import serializers
from app_inventario.models import Repuesto, Ubicacion, Stock, Movimiento, MovimientoItem


class RepuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repuesto
        fields = '__all__'


class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class MovimientoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoItem
        fields = '__all__'


class MovimientoSerializer(serializers.ModelSerializer):
    items = MovimientoItemSerializer(many=True)

    class Meta:
        model = Movimiento
        fields = ['id', 'tipo', 'fecha', 'usuario', 'referencia', 'notas', 'items']
