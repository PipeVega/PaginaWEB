from django.contrib import admin
from .models import Categoria, Producto, Carrito, Perfil, Boleta, DetalleBoleta, Bodega

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(Perfil)
admin.site.register(Boleta)
admin.site.register(DetalleBoleta)
admin.site.register(Bodega)