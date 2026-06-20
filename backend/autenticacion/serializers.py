from rest_framework import serializers
from django.contrib.auth.models import User, Group # Importamos el modelo User y Group de Django
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name') # Campos que queremos exponer
        read_only_fields = ('id',) # El ID es de solo lectura

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # Campo para la contraseña, solo para escritura

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Asignación automática al grupo 'Clientes' - Flujo 1: Registro Público
        try:
            clientes_group = Group.objects.get(name='Clientes')
            user.groups.add(clientes_group) # Asigna al grupo 'Clientes'
        except Group.DoesNotExist:
            raise serializers.ValidationError("El grupo 'Clientes' no existe. Contacte al administrador.")
        
        user.save()
        return user 

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        identifier = attrs.get('username')
        user = User.objects.filter(Q(username__iexact=identifier) | Q(email__iexact=identifier)).first()
        if user:
            attrs['username'] = user.get_username()
        data = super().validate(attrs)

        # Mapeo de roles a formato estándar (minúscula, singular)
        role_map = {
            'Administradores': 'administrador',
            'Vendedores': 'vendedor',
            'Clientes': 'cliente',
        }
        user_group = self.user.groups.first() if self.user and self.user.groups.exists() else None
        role = 'invitado'
        if user_group and user_group.name:
            role = role_map.get(user_group.name, user_group.name.lower())

        data['username'] = str(self.user.username) if self.user and self.user.username else ''
        data['role'] = str(role)
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        role_map = {
            'Administradores': 'administrador',
            'Vendedores': 'vendedor',
            'Clientes': 'cliente',
        }
        user_group = user.groups.first() if user and user.groups.exists() else None
        role = 'invitado'
        if user_group and user_group.name:
            role = role_map.get(user_group.name, user_group.name.lower())
        token['username'] = str(user.username) if user and user.username else ''
        token['role'] = str(role)
        return token 