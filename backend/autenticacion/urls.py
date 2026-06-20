from django.urls import path
from .views import UserRegistrationView, UserProfileView, AdminUserCreateView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('admin/create-user/', AdminUserCreateView.as_view(), name='admin-create-user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Más adelante, aquí podemos añadir URLs para login, logout, etc.
] 