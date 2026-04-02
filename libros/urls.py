from django.urls import path
from . import views

app_name = 'libros'

urlpatterns = [
    path('', views.home, name='home'),
    path('libro/<int:libro_id>/', views.detalle_libro, name='detalle_libro'),
    path('categoria/<int:categoria_id>/', views.por_categoria, name='por_categoria'),
    path('carrito/', views.carrito, name='carrito'),
    path('carrito/agregar/<int:libro_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('resena/<int:libro_id>/', views.agregar_resena, name='agregar_resena'),
    path('contacto/', views.contacto, name='contacto'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('buscar/', views.buscar, name='buscar'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin/libro/editar/<int:libro_id>/', views.editar_libro, name='editar_libro'),
    path('admin/libro/eliminar/<int:libro_id>/', views.eliminar_libro, name='eliminar_libro'),
    path('admin/libro/nuevo/', views.nuevo_libro, name='nuevo_libro'),
    path('admin/ofertas/', views.gestionar_ofertas, name='gestionar_ofertas'),
]
