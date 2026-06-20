# inventario/views.py
from rest_framework import viewsets
from .models import Producto
from .serializers import ProductoSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample


@extend_schema_view(
    list=extend_schema(
        summary="Listar productos",
        description="Obtiene el catálogo completo de productos disponibles. Incluye stock, precio y categoría.",
        tags=["Inventario"],
    ),
    create=extend_schema(
        summary="Crear producto",
        description="Añade un nuevo producto al inventario. Requiere autenticación.",
        tags=["Inventario"],
        request=ProductoSerializer,
        responses={201: ProductoSerializer, 400: "Error de validación", 401: "No autenticado"},
        examples=[
            OpenApiExample(
                "Ejemplo de creación",
                value={
                    "nombre": "Anillo de Oro 18k",
                    "descripcion": "Anillo elegante de oro amarillo 18 quilates",
                    "precio": "250000.00",
                    "stock": 15,
                    "categoria": "Anillos",
                    "referencia": "AN-ORO-001",
                },
                request_only=True,
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Obtener producto",
        description="Obtiene los detalles de un producto específico por su ID.",
        tags=["Inventario"],
        responses={200: ProductoSerializer, 404: "Producto no encontrado"},
    ),
    update=extend_schema(
        summary="Actualizar producto (completo)",
        description="Reemplaza todos los datos de un producto existente.",
        tags=["Inventario"],
        responses={200: ProductoSerializer, 400: "Error de validación"},
    ),
    partial_update=extend_schema(
        summary="Actualizar producto (parcial)",
        description="Actualiza parcialmente los datos de un producto (ej. solo el stock).",
        tags=["Inventario"],
        responses={200: ProductoSerializer, 400: "Error de validación"},
        examples=[
            OpenApiExample(
                "Actualizar stock",
                value={"stock": 25},
                request_only=True,
            ),
        ],
    ),
    destroy=extend_schema(
        summary="Eliminar producto",
        description="Elimina un producto del inventario de forma permanente.",
        tags=["Inventario"],
        responses={204: "Producto eliminado correctamente", 404: "Producto no encontrado"},
    ),
)
class ProductoViewSet(viewsets.ModelViewSet):
    # `queryset` define los objetos que esta vista puede manejar.
    # Aquí, recuperamos todos los productos.
    queryset = Producto.objects.all()

    # `serializer_class` le dice a la vista qué serializador usar para convertir datos.
    serializer_class = ProductoSerializer

    # Permisos: GET permitido a todos, POST/PUT/PATCH/DELETE solo autenticados
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Opcional: Puedes añadir filtros, permisos, autenticación aquí mismo
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # search_fields = ['nombre', 'categoria']
    # permission_classes = [IsAdminUser] # Solo administradores pueden acceder