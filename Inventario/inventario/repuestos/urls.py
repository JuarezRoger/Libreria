from django.urls import path
from .views import (
    DashboardView,
    RepuestoListView, RepuestoCreateView, RepuestoUpdateView, RepuestoDeleteView,
    MovimientoStockListView, MovimientoStockCreateView
)

app_name = 'repuestos'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', RepuestoListView.as_view(), name='list'),
    path('nuevo/', RepuestoCreateView.as_view(), name='create'),
    path('editar/<int:pk>/', RepuestoUpdateView.as_view(), name='update'),
    path('eliminar/<int:pk>/', RepuestoDeleteView.as_view(), name='delete'),
    path('movimientos/', MovimientoStockListView.as_view(), name='movimientos_list'),
    path('movimientos/nuevo/', MovimientoStockCreateView.as_view(), name='movimientos_create'),
]