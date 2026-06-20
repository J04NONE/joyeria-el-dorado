# inventario/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet

# Crea un router para registrar automáticamente las URLs de tu ViewSet
router = DefaultRouter()
router.register(r'productos', ProductoViewSet) # 'productos' será el prefijo de la URL (ej. /api/productos/)

urlpatterns = [
    path('', include(router.urls)), # Incluye las URLs generadas por el router
]
