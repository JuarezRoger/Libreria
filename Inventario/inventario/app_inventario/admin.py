from django.contrib import admin
from .models import Repuesto

# Register your models here.
admin.site.register(Repuesto)
from .models import Ubicacion, Stock, Movimiento, MovimientoItem

admin.site.register(Ubicacion)
admin.site.register(Stock)
admin.site.register(Movimiento)
admin.site.register(MovimientoItem)
