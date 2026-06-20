from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .serializers import UserRegistrationSerializer

class Flujo1RegistroPublicoTest(TestCase):
    """
    Pruebas para el Flujo 1: Registro Público (Auto-servicio para Clientes)
    Verifica que los usuarios se registren automáticamente en el grupo 'Clientes'
    """
    
    def setUp(self):
        """Configura el grupo 'Clientes' necesario para las pruebas"""
        self.clientes_group, created = Group.objects.get_or_create(name='Clientes')
    
    def test_registro_publico_asigna_grupo_clientes(self):
        """
        Verifica que al registrar un usuario público, se le asigne automáticamente
        el grupo 'Clientes'
        """
        # Datos de prueba para el registro
        user_data = {
            'username': 'cliente_test',
            'email': 'cliente@test.com',
            'password': 'testpass123',
            'first_name': 'Juan',
            'last_name': 'Pérez'
        }
        
        # Crear usuario usando el serializer
        serializer = UserRegistrationSerializer(data=user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        
        # Verificar que el usuario se creó correctamente
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'cliente_test')
        
        # Verificar que se asignó al grupo 'Clientes'
        self.assertTrue(user.groups.filter(name='Clientes').exists())
        self.assertEqual(user.groups.count(), 1)
        
        # Verificar que el usuario NO es staff ni superuser
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_registro_publico_grupo_no_existe(self):
        """
        Verifica que si el grupo 'Clientes' no existe, se lance un error
        """
        # Eliminar el grupo 'Clientes' para simular que no existe
        Group.objects.filter(name='Clientes').delete()
        
        # Datos de prueba
        user_data = {
            'username': 'cliente_test2',
            'email': 'cliente2@test.com',
            'password': 'testpass123',
            'first_name': 'María',
            'last_name': 'García'
        }
        
        # Intentar crear usuario - debería fallar
        serializer = UserRegistrationSerializer(data=user_data)
        self.assertTrue(serializer.is_valid())
        
        with self.assertRaises(Exception) as context:
            serializer.save()
        
        # Verificar que el error contiene el mensaje esperado
        self.assertIn("El grupo 'Clientes' no existe", str(context.exception))

class Flujo1APITest(APITestCase):
    """
    Pruebas de API para el Flujo 1: Registro Público
    """
    
    def setUp(self):
        """Configura el grupo 'Clientes' necesario para las pruebas"""
        self.clientes_group, created = Group.objects.get_or_create(name='Clientes')
    
    def test_endpoint_registro_publico(self):
        """
        Verifica que el endpoint de registro público funcione correctamente
        """
        url = reverse('user-register')
        data = {
            'username': 'nuevo_cliente',
            'email': 'nuevo@cliente.com',
            'password': 'password123',
            'first_name': 'Ana',
            'last_name': 'López'
        }
        
        response = self.client.post(url, data, format='json')
        
        # Verificar que la respuesta sea exitosa
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que el usuario se creó
        user = User.objects.get(username='nuevo_cliente')
        self.assertIsNotNone(user)
        
        # Verificar que se asignó al grupo 'Clientes'
        self.assertTrue(user.groups.filter(name='Clientes').exists())
        
        # Verificar que la contraseña se encriptó correctamente
        self.assertTrue(user.check_password('password123'))
    
    def test_registro_publico_permisos_minimos(self):
        """
        Verifica que los usuarios registrados tengan los menores privilegios posibles
        """
        url = reverse('user-register')
        data = {
            'username': 'cliente_minimo',
            'email': 'minimo@cliente.com',
            'password': 'password123',
            'first_name': 'Carlos',
            'last_name': 'Rodríguez'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        user = User.objects.get(username='cliente_minimo')
        
        # Verificar privilegios mínimos
        self.assertFalse(user.is_staff)  # No es staff
        self.assertFalse(user.is_superuser)  # No es superusuario
        self.assertTrue(user.is_active)  # Está activo
        self.assertEqual(user.groups.count(), 1)  # Solo un grupo (Clientes)
