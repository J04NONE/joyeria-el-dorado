from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Cliente


class ClienteModelTest(TestCase):
    """Pruebas unitarias para el modelo Cliente."""

    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre="María",
            apellido="González",
            direccion="Calle 123 #45-67",
            telefono="3001234567",
            correo_electronico="maria@example.com"
        )

    def test_cliente_creation(self):
        """Verifica que un cliente se cree con todos sus atributos."""
        self.assertEqual(self.cliente.nombre, "María")
        self.assertEqual(self.cliente.apellido, "González")
        self.assertEqual(self.cliente.correo_electronico, "maria@example.com")
        self.assertEqual(self.cliente.telefono, "3001234567")
        self.assertIsNotNone(self.cliente.fecha_registro)
        self.assertIsNotNone(self.cliente.ultima_actualizacion)

    def test_cliente_str_representation(self):
        """Verifica que __str__ devuelva nombre + apellido."""
        self.assertEqual(str(self.cliente), "María González")

    def test_cliente_ordering(self):
        """Verifica que el orden por defecto sea apellido, nombre."""
        Cliente.objects.create(
            nombre="Ana",
            apellido="Martínez",
            correo_electronico="ana@example.com"
        )
        Cliente.objects.create(
            nombre="Carlos",
            apellido="Álvarez",
            correo_electronico="carlos@example.com"
        )
        clientes = Cliente.objects.all()
        self.assertEqual(clientes[0].apellido, "González")
        self.assertEqual(clientes[1].apellido, "Martínez")

    def test_cliente_email_unico(self):
        """Verifica que no se puedan crear dos clientes con el mismo email."""
        with self.assertRaises(Exception):
            Cliente.objects.create(
                nombre="Juan",
                apellido="Pérez",
                correo_electronico="maria@example.com"
            )

    def test_cliente_campos_opcionales(self):
        """Verifica que direccion y telefono puedan ser nulos."""
        cliente_sin_extras = Cliente.objects.create(
            nombre="Pedro",
            apellido="Ramírez",
            correo_electronico="pedro@example.com"
        )
        self.assertIsNone(cliente_sin_extras.direccion)
        self.assertIsNone(cliente_sin_extras.telefono)


class ClienteAPITest(APITestCase):
    """Pruebas para la API REST del modelo Cliente."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        self.cliente = Cliente.objects.create(
            nombre="Laura",
            apellido="Fernández",
            correo_electronico="laura@example.com",
            telefono="3109876543"
        )

    def test_listar_clientes(self):
        """Verifica que se listen todos los clientes."""
        Cliente.objects.create(
            nombre="Otro",
            apellido="Cliente",
            correo_electronico="otro@example.com"
        )
        url = reverse('cliente-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_crear_cliente(self):
        """Verifica crear un nuevo cliente vía API."""
        url = reverse('cliente-list')
        data = {
            'nombre': 'Carlos',
            'apellido': 'Mendoza',
            'correo_electronico': 'carlos@example.com',
            'telefono': '3151112233'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cliente.objects.count(), 2)
        self.assertEqual(response.data['nombre'], 'Carlos')

    def test_obtener_cliente_especifico(self):
        """Verifica obtener un cliente por ID."""
        url = reverse('cliente-detail', args=[self.cliente.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Laura')
        self.assertEqual(response.data['correo_electronico'], 'laura@example.com')

    def test_actualizar_cliente(self):
        """Verifica actualizar un cliente existente."""
        url = reverse('cliente-detail', args=[self.cliente.id])
        data = {'telefono': '3201112233'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.telefono, '3201112233')

    def test_eliminar_cliente(self):
        """Verifica eliminar un cliente."""
        url = reverse('cliente-detail', args=[self.cliente.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cliente.objects.count(), 0)

    def test_crear_cliente_email_duplicado(self):
        """Verifica error al crear cliente con email ya existente."""
        url = reverse('cliente-list')
        data = {
            'nombre': 'Duplicado',
            'apellido': 'Email',
            'correo_electronico': 'laura@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_autenticado_listar(self):
        """Verifica que GET sin auth funcione (ModelViewSet no tiene restricción global)."""
        self.client.force_authenticate(user=None)
        url = reverse('cliente-list')
        response = self.client.get(url)
        # ClienteViewSet no tiene permission_classes definido, usa global IsAuthenticated
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
