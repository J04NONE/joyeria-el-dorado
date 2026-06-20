# clientes/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet

# Crea un router para registrar automáticamente las URLs de tu ViewSet
router = DefaultRouter()
router.register(r'', ClienteViewSet) # El prefijo viene del urls.py raíz (api/clientes/)

# Exporta el router directamente, para que pueda ser incluido por el urls.py principal
urlpatterns = router.urls # ¡Cambia esto si tenías otra cosa!