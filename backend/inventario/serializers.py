# inventario/serializers.py
from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'categoria', 'imagen', 'fecha_creacion', 'fecha_actualizacion']
        # O puedes listar campos específicos:
        # fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'categoria', 'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion') # Campos que no se pueden modificar vía API