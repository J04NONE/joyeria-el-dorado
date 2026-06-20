# ventas/serializers.py
from rest_framework import serializers
from .models import Venta, VentaProducto, Garantia
from inventario.serializers import ProductoSerializer # Para serializar detalles del producto
from clientes.serializers import ClienteSerializer # Para serializar detalles del cliente
from inventario.models import Producto # Para manejar la lógica de stock

# Serializador para la tabla intermedia VentaProducto
class VentaProductoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True) # Para mostrar el nombre del producto

    class Meta:
        model = VentaProducto
        fields = ['producto', 'cantidad', 'precio_unitario', 'producto_nombre']
        read_only_fields = ['precio_unitario', 'producto_nombre'] # El precio unitario debería fijarse al añadir

# Serializador para el modelo Venta
class VentaSerializer(serializers.ModelSerializer):
    # Usamos un nested serializer para los productos de la venta
    productos_venta = VentaProductoSerializer(source='ventaproducto_set', many=True, read_only=True)
    cliente_detalle = ClienteSerializer(source='cliente', read_only=True) # Para ver detalles del cliente

    class Meta:
        model = Venta
        fields = ['id', 'cliente', 'cliente_detalle', 'fecha', 'total', 'productos', 'productos_venta']
        read_only_fields = ('fecha', 'total', 'productos_venta', 'cliente_detalle') # Total y fecha se calculan

    # Método para manejar la creación de productos_venta al crear una Venta
    def create(self, validated_data):
        # Extraer los productos de la venta si se envían
        productos_data = self.context['request'].data.get('productos_compra', []) # Usamos un nombre diferente para el input

        # Eliminar 'productos' del validated_data si viene (se maneja por el through)
        if 'productos' in validated_data:
            del validated_data['productos']

        venta = Venta.objects.create(**validated_data)

        total_calculado = 0
        for item_data in productos_data:
            producto_id = item_data.get('producto_id')
            cantidad = item_data.get('cantidad')
            if producto_id and cantidad:
                try:
                    producto = Producto.objects.get(id=producto_id)
                    if producto.stock >= cantidad:
                        precio_unitario = producto.precio # Usamos el precio actual del producto
                        VentaProducto.objects.create(
                            venta=venta,
                            producto=producto,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario
                        )
                        producto.stock -= cantidad # Descontar stock
                        producto.save()
                        total_calculado += (precio_unitario * cantidad)
                    else:
                        raise serializers.ValidationError(f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}")
                except Producto.DoesNotExist:
                    raise serializers.ValidationError(f"Producto con ID {producto_id} no existe.")
            else:
                raise serializers.ValidationError("Cada item de producto debe tener 'producto_id' y 'cantidad'.")

        venta.total = total_calculado # Actualizar el total de la venta
        venta.save()
        return venta

# Serializador para el modelo Garantía
class GarantiaSerializer(serializers.ModelSerializer):
    producto_detalle = ProductoSerializer(source='producto', read_only=True) # Para ver detalles del producto

    class Meta:
        model = Garantia
        fields = ['producto', 'producto_detalle', 'fecha_inicio', 'fecha_fin', 'estado']
        read_only_fields = ('fecha_inicio', 'producto_detalle') # La fecha de inicio se genera automáticamente 