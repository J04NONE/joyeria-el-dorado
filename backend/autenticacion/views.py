from rest_framework import generics, status, serializers
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from .serializers import UserSerializer, UserRegistrationSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, OpenApiExample


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="Registrar usuario",
        description="Registro público de nuevos usuarios. No requiere autenticación. Crea un usuario con rol 'Cliente' por defecto.",
        tags=["Autenticación"],
        request=UserRegistrationSerializer,
        responses={201: UserRegistrationSerializer, 400: "Error de validación"},
        examples=[
            OpenApiExample(
                "Ejemplo de registro",
                value={
                    "username": "nuevo_usuario",
                    "email": "usuario@example.com",
                    "password": "MiPassword123!",
                    "password2": "MiPassword123!",
                },
                request_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    @extend_schema(
        summary="Obtener perfil",
        description="Obtiene el perfil del usuario autenticado. Requiere token JWT en el header Authorization.",
        tags=["Autenticación"],
        responses={200: UserSerializer, 401: "No autenticado"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar perfil",
        description="Actualiza los datos del perfil del usuario autenticado.",
        tags=["Autenticación"],
        request=UserSerializer,
        responses={200: UserSerializer, 400: "Error de validación"},
        examples=[
            OpenApiExample(
                "Actualizar email",
                value={"email": "nuevo_email@example.com"},
                request_only=True,
            ),
        ],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar perfil (completo)",
        description="Reemplaza todos los datos del perfil del usuario autenticado.",
        tags=["Autenticación"],
        request=UserSerializer,
        responses={200: UserSerializer, 400: "Error de validación"},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class AdminUserCreateView(generics.CreateAPIView):
    """
    Vista para que un ADMINISTRADOR cree nuevos usuarios y asigne roles (grupos).
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (IsAdminUser,)

    @extend_schema(
        summary="Crear usuario (admin)",
        description="Permite a un administrador crear usuarios y asignarles un rol específico (grupo). Requiere ser administrador.",
        tags=["Administración"],
        request=UserRegistrationSerializer,
        responses={201: UserRegistrationSerializer, 400: "Error de validación", 403: "No autorizado"},
        examples=[
            OpenApiExample(
                "Crear vendedor",
                value={
                    "username": "nuevo_vendedor",
                    "email": "vendedor@joyeria.com",
                    "password": "PassVendedor2025!",
                    "password2": "PassVendedor2025!",
                    "group": "Vendedores",
                },
                request_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        requested_group_name = self.request.data.get('group', 'Vendedores')
        user = serializer.save()
        try:
            target_group = Group.objects.get(name=requested_group_name)
            user.groups.add(target_group)
        except Group.DoesNotExist:
            user.delete()
            raise serializers.ValidationError(
                {"group": f"El grupo '{requested_group_name}' no existe. Contacte al administrador."}
            )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        summary="Iniciar sesión",
        description="Obtiene un par de tokens JWT (access + refresh) al autenticarse con username y password.",
        tags=["Autenticación"],
        request=CustomTokenObtainPairSerializer,
        responses={200: CustomTokenObtainPairSerializer, 401: "Credenciales inválidas"},
        examples=[
            OpenApiExample(
                "Inicio de sesión exitoso",
                value={
                    "username": "admin@joyeria.com",
                    "password": "Admin123!",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Respuesta exitosa",
                value={
                    "refresh": "eyJhbGciOiJIUzI1NiIs...",
                    "access": "eyJhbGciOiJIUzI1NiIs...",
                    "role": "administrador",
                    "user_id": 1,
                    "username": "admin@joyeria.com",
                },
                response_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
