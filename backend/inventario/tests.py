from django.test import TestCase
from django.urls import reverse # Para obtener URLs por nombre
from rest_framework import status
from rest_framework.test import APITestCase # Para probar APIs
from .models import Producto

class ProductoModelTest(TestCase):
    """
    Pruebas unitarias para el modelo Producto.
    Verifica la creación básica del objeto y su representación de cadena.
    """
    def setUp(self):
        # Configura datos iniciales para las pruebas
        self.producto = Producto.objects.create(
            nombre="Anillo de Plata",
            descripcion="Anillo sencillo de plata 925",
            precio=50.00,
            stock=20,
            categoria="Anillo"
        )

    def test_producto_creation(self):
        """
        Verifica que un producto se pueda crear y sus atributos sean correctos.
        """
        self.assertEqual(self.producto.nombre, "Anillo de Plata")
        self.assertEqual(self.producto.stock, 20)
        self.assertEqual(float(self.producto.precio), 50.00) # Convertir a float para comparar con float
        self.assertEqual(self.producto.categoria, "Anillo")
        self.assertIsNotNone(self.producto.fecha_creacion)
        self.assertIsNotNone(self.producto.fecha_actualizacion)

    def test_producto_str_representation(self):
        """
        Verifica que el método __str__ del producto devuelva el nombre correcto.
        """
        self.assertEqual(str(self.producto), "Anillo de Plata")

    def test_producto_default_stock(self):
        """
        Verifica que el stock por defecto sea 0 si no se especifica.
        """
        new_producto = Producto.objects.create(
            nombre="Collar de Perlas",
            precio=150.00,
            categoria="Collar"
        )
        self.assertEqual(new_producto.stock, 0)

class ProductoAPITest(APITestCase):
    """
    Pruebas para la API REST del modelo Producto.
    Verifica los endpoints de listado y creación de productos.
    """
    def setUp(self):
        # Crear un usuario autenticado para las pruebas de escritura
        # El ProductoViewSet usa IsAuthenticatedOrReadOnly, por lo que POST requiere autenticación
        from django.contrib.auth.models import User
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Crear un producto de prueba para las pruebas de API
        self.producto = Producto.objects.create(
            nombre="Pulsera de Oro",
            descripcion="Pulsera elegante de oro 18k",
            precio=200.00,
            stock=15,
            categoria="Pulsera"
        )

    def test_listar_productos(self):
        """
        Verifica que se puedan listar todos los productos.
        """
        url = reverse('producto-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Debería haber 1 producto

    def test_crear_producto(self):
        """
        Verifica que se pueda crear un nuevo producto a través de la API.
        El usuario debe estar autenticado (IsAuthenticatedOrReadOnly).
        """
        url = reverse('producto-list')
        data = {
            'nombre': 'Aretes de Diamante',
            'descripcion': 'Aretes con diamantes naturales',
            'precio': 500.00,
            'stock': 8,
            'categoria': 'Aretes'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Producto.objects.count(), 2)  # Debería haber 2 productos ahora

    def test_obtener_producto_especifico(self):
        """
        Verifica que se pueda obtener un producto específico por ID.
        """
        url = reverse('producto-detail', args=[self.producto.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Pulsera de Oro')
