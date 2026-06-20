from rest_framework import viewsets
from .models import Proveedor
from .serializers import ProveedorSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample


@extend_schema_view(
    list=extend_schema(
        summary="Listar proveedores",
        description="Obtiene una lista de todos los proveedores registrados en el sistema.",
        tags=["Proveedores"],
        responses={200: ProveedorSerializer(many=True)},
    ),
    create=extend_schema(
        summary="Crear proveedor",
        description="Registra un nuevo proveedor. El nombre debe ser único.",
        tags=["Proveedores"],
        request=ProveedorSerializer,
        responses={201: ProveedorSerializer, 400: "Error de validación"},
        examples=[
            OpenApiExample(
                "Ejemplo de creación",
                value={
                    "nombre": "Joyas Finas S.A.S.",
                    "direccion": "Av. Principal #12-34",
                    "telefono": "6012345678",
                    "correo_electronico": "contacto@joyasfinas.com",
                },
                request_only=True,
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Obtener proveedor",
        description="Obtiene los detalles de un proveedor específico por su ID.",
        tags=["Proveedores"],
        responses={200: ProveedorSerializer, 404: "Proveedor no encontrado"},
    ),
    update=extend_schema(
        summary="Actualizar proveedor (completo)",
        description="Reemplaza todos los datos de un proveedor existente.",
        tags=["Proveedores"],
        responses={200: ProveedorSerializer, 400: "Error de validación"},
    ),
    partial_update=extend_schema(
        summary="Actualizar proveedor (parcial)",
        description="Actualiza parcialmente los datos de un proveedor existente.",
        tags=["Proveedores"],
        responses={200: ProveedorSerializer, 400: "Error de validación"},
    ),
    destroy=extend_schema(
        summary="Eliminar proveedor",
        description="Elimina un proveedor del sistema de forma permanente.",
        tags=["Proveedores"],
        responses={204: "Proveedor eliminado correctamente", 404: "Proveedor no encontrado"},
    ),
)
class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
