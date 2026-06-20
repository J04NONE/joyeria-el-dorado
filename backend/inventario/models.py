from django.db import models


class Producto(models.Model):

    # ID Producto (identificador único) - Django crea automáticamente un campo 'id'
    # como Primary Key (clave primaria) si no se especifica uno.
    # Por defecto, es un campo BigAutoField (bigint en PostgreSQL), que es perfecto.

    nombre = models.CharField(max_length=255, help_text="Nombre del producto")
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción detallada del producto")
    precio = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio de venta del producto")
    stock = models.IntegerField(default=0, help_text="Cantidad de productos en Inventario")
    categoria = models.CharField(max_length=100, help_text="Categoría del producto (ej. Anillo, Collar, Pulsera)")
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, help_text="Imagen del producto")

    # Campos adicionales útiles para la gestión y auditoría:
    fecha_creacion = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de creación del producto")
    fecha_actualizacion = models.DateTimeField(auto_now=True, help_text="Última fecha y hora de actualización del producto")

    class Meta:
        # Opciones de metadatos para el modelo
        verbose_name = "Producto"
        verbose_name_plural = "Productos" # Nombre en plural para el Admin de Django
        ordering = ['nombre'] # Ordenar productos por nombre por defecto

    def __str__(self):
        return self.nombre
