from django.urls import path
from . import views

app_name = 'app_inventario'

urlpatterns = [
    path('inicio/', views.index, name='inicio'),
    path('repuestos_inventario/', views.inventario_view, name='repuestos_inventario'),
    path('reportes/', views.reportes_view, name='reportes'),
    path('historial_tecnico/', views.historial_tecnico_view, name='historial_tecnico'),
    path('lista_de_repuestos/', views.lista_de_repuestos_view, name='lista_de_repuestos'),
]
