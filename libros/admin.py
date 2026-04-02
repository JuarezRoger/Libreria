from django.contrib import admin
from .models import Categoria, Libro, Resena, CarritoItem, Contacto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'categoria', 'precio', 'stock', 'fecha_publicacion']
    list_filter = ['categoria', 'fecha_publicacion']
    search_fields = ['titulo', 'autor', 'isbn']
    list_editable = ['precio', 'stock']

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ['libro', 'usuario', 'calificacion', 'fecha_creacion']
    list_filter = ['calificacion', 'fecha_creacion']
    search_fields = ['usuario__username', 'libro__titulo']

@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'libro', 'cantidad', 'subtotal', 'fecha_agregado']
    list_filter = ['fecha_agregado']

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'telefono', 'fecha_envio', 'leido']
    list_filter = ['leido', 'fecha_envio']
    search_fields = ['nombre', 'email', 'mensaje']
    list_editable = ['leido']
