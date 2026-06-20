from rest_framework import viewsets
from .models import Venta, VentaProducto, Garantia
from .serializers import VentaSerializer, VentaProductoSerializer, GarantiaSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample


@extend_schema_view(
    list=extend_schema(
        summary="Listar ventas",
        description="Obtiene el historial de todas las ventas registradas. Incluye productos, cantidades y totales.",
        tags=["Ventas"],
    ),
    create=extend_schema(
        summary="Crear venta",
        description="Registra una nueva venta. Los productos se especifican en 'productos_compra' con 'producto_id' y 'cantidad'. El stock se descuenta automáticamente y el total se calcula.",
        tags=["Ventas"],
        request=VentaSerializer,
        responses={201: VentaSerializer, 400: "Error de validación (stock insuficiente, producto inexistente)"},
        examples=[
            OpenApiExample(
                "Ejemplo de venta",
                value={
                    "cliente": 1,
                    "productos_compra": [
                        {"producto_id": 1, "cantidad": 2},
                        {"producto_id": 3, "cantidad": 1},
                    ],
                },
                request_only=True,
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Obtener venta",
        description="Obtiene los detalles de una venta específica incluyendo los productos vendidos.",
        tags=["Ventas"],
        responses={200: VentaSerializer, 404: "Venta no encontrada"},
    ),
    update=extend_schema(
        summary="Actualizar venta (completo)",
        description="Reemplaza todos los datos de una venta existente.",
        tags=["Ventas"],
        responses={200: VentaSerializer, 400: "Error de validación"},
    ),
    partial_update=extend_schema(
        summary="Actualizar venta (parcial)",
        description="Actualiza parcialmente los datos de una venta existente.",
        tags=["Ventas"],
        responses={200: VentaSerializer, 400: "Error de validación"},
    ),
    destroy=extend_schema(
        summary="Eliminar venta",
        description="Elimina una venta del registro. No revierte el descuento de stock.",
        tags=["Ventas"],
        responses={204: "Venta eliminada correctamente", 404: "Venta no encontrada"},
    ),
)
class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Listar productos de ventas",
        description="Obtiene todos los items de productos vendidos en todas las ventas.",
        tags=["Ventas - Productos"],
    ),
    create=extend_schema(
        summary="Asociar producto a venta",
        description="Registra un producto como parte de una venta existente.",
        tags=["Ventas - Productos"],
        request=VentaProductoSerializer,
        responses={201: VentaProductoSerializer, 400: "Error de validación"},
    ),
    retrieve=extend_schema(
        summary="Obtener detalle de producto en venta",
        description="Obtiene el detalle de un producto específico dentro de una venta.",
        tags=["Ventas - Productos"],
        responses={200: VentaProductoSerializer, 404: "No encontrado"},
    ),
    update=extend_schema(
        summary="Actualizar producto en venta (completo)",
        description="Reemplaza todos los datos de un producto en una venta.",
        tags=["Ventas - Productos"],
        responses={200: VentaProductoSerializer, 400: "Error de validación"},
    ),
    partial_update=extend_schema(
        summary="Actualizar producto en venta (parcial)",
        description="Actualiza parcialmente los datos de un producto en una venta.",
        tags=["Ventas - Productos"],
        responses={200: VentaProductoSerializer, 400: "Error de validación"},
    ),
    destroy=extend_schema(
        summary="Eliminar producto de venta",
        description="Elimina un producto de una venta. No revierte el descuento de stock.",
        tags=["Ventas - Productos"],
        responses={204: "Eliminado correctamente"},
    ),
)
class VentaProductoViewSet(viewsets.ModelViewSet):
    queryset = VentaProducto.objects.all()
    serializer_class = VentaProductoSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Listar garantías",
        description="Obtiene todas las garantías registradas para los productos.",
        tags=["Garantías"],
    ),
    create=extend_schema(
        summary="Crear garantía",
        description="Registra una nueva garantía para un producto. Cada producto puede tener solo una garantía activa.",
        tags=["Garantías"],
        request=GarantiaSerializer,
        responses={201: GarantiaSerializer, 400: "Error de validación"},
        examples=[
            OpenApiExample(
                "Ejemplo de garantía",
                value={
                    "producto": 1,
                    "fecha_fin": "2026-06-19",
                    "estado": "Activa",
                },
                request_only=True,
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Obtener garantía",
        description="Obtiene la garantía de un producto específico por su ID de producto.",
        tags=["Garantías"],
        responses={200: GarantiaSerializer, 404: "Garantía no encontrada"},
    ),
    update=extend_schema(
        summary="Actualizar garantía (completo)",
        description="Reemplaza todos los datos de una garantía existente.",
        tags=["Garantías"],
        responses={200: GarantiaSerializer, 400: "Error de validación"},
    ),
    partial_update=extend_schema(
        summary="Actualizar garantía (parcial)",
        description="Actualiza parcialmente los datos de una garantía.",
        tags=["Garantías"],
        responses={200: GarantiaSerializer, 400: "Error de validación"},
    ),
    destroy=extend_schema(
        summary="Eliminar garantía",
        description="Elimina la garantía de un producto.",
        tags=["Garantías"],
        responses={204: "Garantía eliminada correctamente"},
    ),
)
class GarantiaViewSet(viewsets.ModelViewSet):
    queryset = Garantia.objects.all()
    serializer_class = GarantiaSerializer
