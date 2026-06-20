from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Proveedor


class ProveedorModelTest(TestCase):
    """Pruebas unitarias para el modelo Proveedor."""

    def setUp(self):
        self.proveedor = Proveedor.objects.create(
            nombre="Joyas Finas S.A.S.",
            direccion="Av. Principal #12-34",
            telefono="6012345678",
            correo_electronico="contacto@joyasfinas.com"
        )

    def test_proveedor_creation(self):
        """Verifica que un proveedor se cree con todos sus atributos."""
        self.assertEqual(self.proveedor.nombre, "Joyas Finas S.A.S.")
        self.assertEqual(self.proveedor.direccion, "Av. Principal #12-34")
        self.assertEqual(self.proveedor.telefono, "6012345678")
        self.assertEqual(self.proveedor.correo_electronico, "contacto@joyasfinas.com")
        self.assertIsNotNone(self.proveedor.fecha_registro)
        self.assertIsNotNone(self.proveedor.ultima_actualizacion)

    def test_proveedor_str_representation(self):
        """Verifica que __str__ devuelva el nombre."""
        self.assertEqual(str(self.proveedor), "Joyas Finas S.A.S.")

    def test_proveedor_nombre_unico(self):
        """Verifica que no se puedan crear dos proveedores con el mismo nombre."""
        with self.assertRaises(Exception):
            Proveedor.objects.create(
                nombre="Joyas Finas S.A.S.",
                correo_electronico="otro@correo.com"
            )

    def test_proveedor_campos_opcionales(self):
        """Verifica que direccion, telefono y email puedan ser nulos."""
        proveedor_minimo = Proveedor.objects.create(
            nombre="Proveedor Mínimo"
        )
        self.assertIsNone(proveedor_minimo.direccion)
        self.assertIsNone(proveedor_minimo.telefono)
        self.assertIsNone(proveedor_minimo.correo_electronico)

    def test_proveedor_ordering(self):
        """Verifica el orden alfabético por nombre."""
        Proveedor.objects.create(nombre="Zafiros Ltda.")
        Proveedor.objects.create(nombre="Aretes Express")
        proveedores = Proveedor.objects.all()
        self.assertEqual(proveedores[0].nombre, "Aretes Express")
        self.assertEqual(proveedores[1].nombre, "Joyas Finas S.A.S.")


class ProveedorAPITest(APITestCase):
    """Pruebas para la API REST del modelo Proveedor."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        self.proveedor = Proveedor.objects.create(
            nombre="Distribuidora de Joyas",
            telefono="6023456789",
            correo_electronico="ventas@distribuidora.com"
        )

    def test_listar_proveedores(self):
        """Verifica que se listen todos los proveedores."""
        Proveedor.objects.create(nombre="Otro Proveedor")
        url = reverse('proveedor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_crear_proveedor(self):
        """Verifica crear un nuevo proveedor vía API."""
        url = reverse('proveedor-list')
        data = {
            'nombre': 'Nuevo Proveedor S.A.',
            'telefono': '6033334455',
            'correo_electronico': 'info@nuevoproveedor.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Proveedor.objects.count(), 2)
        self.assertEqual(response.data['nombre'], 'Nuevo Proveedor S.A.')

    def test_obtener_proveedor_especifico(self):
        """Verifica obtener un proveedor por ID."""
        url = reverse('proveedor-detail', args=[self.proveedor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Distribuidora de Joyas')

    def test_actualizar_proveedor(self):
        """Verifica actualizar un proveedor existente."""
        url = reverse('proveedor-detail', args=[self.proveedor.id])
        data = {'telefono': '6044445566'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.proveedor.refresh_from_db()
        self.assertEqual(self.proveedor.telefono, '6044445566')

    def test_eliminar_proveedor(self):
        """Verifica eliminar un proveedor."""
        url = reverse('proveedor-detail', args=[self.proveedor.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Proveedor.objects.count(), 0)

    def test_crear_proveedor_nombre_duplicado(self):
        """Verifica error al crear proveedor con nombre ya existente."""
        url = reverse('proveedor-list')
        data = {
            'nombre': 'Distribuidora de Joyas',
            'correo_electronico': 'duplicado@correo.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_autenticado_listar(self):
        """Verifica que sin auth devuelva 401."""
        self.client.force_authenticate(user=None)
        url = reverse('proveedor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
