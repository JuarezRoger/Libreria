from rest_framework import routers
from django.urls import path, include
from .views import (
    RepuestoViewSet,
    UbicacionViewSet,
    StockViewSet,
    MovimientoViewSet,
    MovimientoItemViewSet,
)

router = routers.DefaultRouter()
router.register(r'repuestos', RepuestoViewSet)
router.register(r'ubicaciones', UbicacionViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'movimientos', MovimientoViewSet)
router.register(r'movimientos-items', MovimientoItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]