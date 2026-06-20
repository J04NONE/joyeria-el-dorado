from django.db import models
from clientes.models import Cliente # Importamos el modelo Cliente
from inventario.models import Producto # Importamos el modelo Producto

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True) # Si el cliente se elimina, la venta no
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Relación Many-to-Many con Producto a través de una tabla intermedia (VentaProducto)
    productos = models.ManyToManyField(Producto, through='VentaProducto')

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha'] # Últimas ventas primero

    def __str__(self):
        return f"Venta #{self.id} - Cliente: {self.cliente or 'Anónimo'} - Total: ${self.total:.2f}"

# Modelo Intermedio para la relación Many-to-Many con campos adicionales
class VentaProducto(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2) # Precio al momento de la venta

    class Meta:
        unique_together = ('venta', 'producto') # Un producto solo puede estar una vez en una venta (para evitar duplicados directos)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Venta #{self.venta.id}"

# Modelo para gestionar garantías de productos
class Garantia(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, primary_key=True) # Un producto tiene una garantía, y si se borra el producto, se borra la garantía
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=50, default="Activa") # Ej. Activa, Expirada, Cancelada

    class Meta:
        verbose_name = "Garantía"
        verbose_name_plural = "Garantías"
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"Garantía para {self.producto.nombre} - Estado: {self.estado}"
