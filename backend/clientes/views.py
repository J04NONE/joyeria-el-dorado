# clientes/views.py
from rest_framework import viewsets
from .models import Cliente
from .serializers import ClienteSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample


@extend_schema_view(
    list=extend_schema(
        summary="Listar clientes",
        description="Obtiene una lista paginada de todos los clientes registrados en el sistema.",
        tags=["Clientes"],
    ),
    create=extend_schema(
        summary="Crear cliente",
        description="Registra un nuevo cliente en el sistema. El correo electrónico debe ser único.",
        tags=["Clientes"],
        request=ClienteSerializer,
        responses={201: ClienteSerializer, 400: "Error de validación"},
        examples=[
            OpenApiExample(
                "Ejemplo de creación",
                value={
                    "nombre": "María",
                    "apellido": "González",
                    "direccion": "Calle 123 #45-67",
                    "telefono": "3001234567",
                    "correo_electronico": "maria@example.com",
                },
                request_only=True,
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Obtener cliente",
        description="Obtiene los detalles de un cliente específico por su ID.",
        tags=["Clientes"],
        responses={200: ClienteSerializer, 404: "Cliente no encontrado"},
    ),
    update=extend_schema(
        summary="Actualizar cliente (completo)",
        description="Reemplaza todos los datos de un cliente existente.",
        tags=["Clientes"],
        responses={200: ClienteSerializer, 400: "Error de validación"},
    ),
    partial_update=extend_schema(
        summary="Actualizar cliente (parcial)",
        description="Actualiza parcialmente los datos de un cliente existente.",
        tags=["Clientes"],
        responses={200: ClienteSerializer, 400: "Error de validación"},
        examples=[
            OpenApiExample(
                "Ejemplo de actualización parcial",
                value={"telefono": "3201112233"},
                request_only=True,
            ),
        ],
    ),
    destroy=extend_schema(
        summary="Eliminar cliente",
        description="Elimina un cliente del sistema de forma permanente.",
        tags=["Clientes"],
        responses={204: "Cliente eliminado correctamente", 404: "Cliente no encontrado"},
    ),
)
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer