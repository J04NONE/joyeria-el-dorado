# ventas/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VentaViewSet, VentaProductoViewSet, GarantiaViewSet

# Router para VentaProducto y Garantia (prefijos únicos)
router_secundario = DefaultRouter()
router_secundario.register(r'productos', VentaProductoViewSet, basename='venta-producto')
router_secundario.register(r'garantias', GarantiaViewSet)

# VentaViewSet con rutas explícitas para evitar /api/ventas/ventas/
venta_list = VentaViewSet.as_view({'get': 'list', 'post': 'create'})
venta_detail = VentaViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', venta_list, name='venta-list'),
    path('<int:pk>/', venta_detail, name='venta-detail'),
    path('', include(router_secundario.urls)),
] 