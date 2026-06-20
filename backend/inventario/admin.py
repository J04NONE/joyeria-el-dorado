# inventario/admin.py
from django.contrib import admin
from .models import Producto # Importa tu modelo Producto

@admin.register(Producto) # Decorador para registrar el modelo
class ProductoAdmin(admin.ModelAdmin):
    # Define cómo se mostrará el modelo en el panel de administración
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'fecha_actualizacion')
    search_fields = ('nombre', 'categoria', 'descripcion') # Campos por los que se puede buscar
    list_filter = ('categoria', 'fecha_creacion') # Filtros en la barra lateral