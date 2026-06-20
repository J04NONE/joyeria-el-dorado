from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from clientes.models import Cliente
from inventario.models import Producto
from .models import Venta, VentaProducto, Garantia
from datetime import date, timedelta
import time


class VentaModelTest(TestCase):
    """Pruebas unitarias para el modelo Venta."""

    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre="Cliente",
            apellido="Prueba",
            correo_electronico="cliente@test.com"
        )
        self.producto = Producto.objects.create(
            nombre="Anillo de Oro",
            precio=100.00,
            stock=10,
            categoria="Anillo"
        )
        self.venta = Venta.objects.create(
            cliente=self.cliente,
            total=200.00
        )
        VentaProducto.objects.create(
            venta=self.venta,
            producto=self.producto,
            cantidad=2,
            precio_unitario=100.00
        )

    def test_venta_creation(self):
        """Verifica que una venta se cree con sus atributos básicos."""
        self.assertEqual(self.venta.cliente, self.cliente)
        self.assertEqual(float(self.venta.total), 200.00)
        self.assertIsNotNone(self.venta.fecha)

    def test_venta_str_representation(self):
        """Verifica que __str__ incluya ID, cliente y total."""
        str_repr = str(self.venta)
        self.assertIn("Venta", str_repr)
        self.assertIn(str(self.venta.id), str_repr)
        self.assertIn("$200.00", str_repr)

    def test_venta_ordering(self):
        """Verifica orden descendente por fecha (más reciente primero)."""
        venta_vieja = Venta.objects.create(cliente=self.cliente)
        time.sleep(0.01)
        venta_reciente = Venta.objects.create(cliente=self.cliente)
        ventas = Venta.objects.all()
        self.assertEqual(ventas.count(), 3)
        # La más reciente debe ir primero (ordering = ['-fecha'])
        self.assertEqual(ventas[0].id, venta_reciente.id)

    def test_venta_sin_cliente(self):
        """Verifica que una venta pueda existir sin cliente (SET_NULL)."""
        cliente_id = self.cliente.id
        self.cliente.delete()
        self.venta.refresh_from_db()
        self.assertIsNone(self.venta.cliente)

    def test_venta_total_default(self):
        """Verifica que el total por defecto sea 0.00."""
        venta_sin_total = Venta.objects.create()
        self.assertEqual(float(venta_sin_total.total), 0.00)

    def test_ventaproducto_creation(self):
        """Verifica la creación de un item de VentaProducto."""
        vp = VentaProducto.objects.first()
        self.assertIsNotNone(vp)
        self.assertEqual(vp.cantidad, 2)
        self.assertEqual(float(vp.precio_unitario), 100.00)
        self.assertEqual(vp.producto.nombre, "Anillo de Oro")

    def test_ventaproducto_str(self):
        """Verifica que __str__ de VentaProducto funcione."""
        vp = VentaProducto.objects.first()
        str_repr = str(vp)
        self.assertIn("Anillo de Oro", str_repr)
        self.assertIn(str(self.venta.id), str_repr)


class GarantiaModelTest(TestCase):
    """Pruebas unitarias para el modelo Garantía."""

    def setUp(self):
        self.producto = Producto.objects.create(
            nombre="Collar de Perlas",
            precio=250.00,
            stock=5,
            categoria="Collar"
        )
        self.garantia = Garantia.objects.create(
            producto=self.producto,
            fecha_fin=date.today() + timedelta(days=365),
            estado="Activa"
        )

    def test_garantia_creation(self):
        """Verifica creación de garantía."""
        self.assertEqual(self.garantia.producto, self.producto)
        self.assertEqual(self.garantia.estado, "Activa")
        self.assertIsNotNone(self.garantia.fecha_inicio)
        self.assertIsNotNone(self.garantia.fecha_fin)

    def test_garantia_str(self):
        """Verifica que __str__ incluya nombre y estado."""
        str_repr = str(self.garantia)
        self.assertIn("Collar de Perlas", str_repr)
        self.assertIn("Activa", str_repr)

    def test_garantia_producto_onetoone(self):
        """Verifica que al eliminar el producto se elimine la garantía."""
        producto_id = self.producto.id
        self.producto.delete()
        with self.assertRaises(Garantia.DoesNotExist):
            Garantia.objects.get(producto_id=producto_id)

    def test_garantia_estado_default(self):
        """Verifica que el estado por defecto sea 'Activa'."""
        nueva_garantia = Garantia.objects.create(
            producto=Producto.objects.create(
                nombre="Reloj Dorado",
                precio=500.00,
                stock=3,
                categoria="Reloj"
            ),
            fecha_fin=date.today() + timedelta(days=180)
        )
        self.assertEqual(nueva_garantia.estado, "Activa")


class VentaAPITest(APITestCase):
    """Pruebas para la API REST de Ventas."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        self.cliente = Cliente.objects.create(
            nombre="Cliente",
            apellido="API",
            correo_electronico="clienteapi@test.com"
        )
        self.producto = Producto.objects.create(
            nombre="Pulsera de Plata",
            precio=75.00,
            stock=20,
            categoria="Pulsera"
        )

    def test_listar_ventas(self):
        """Verifica listar todas las ventas."""
        Venta.objects.create(cliente=self.cliente, total=150.00)
        url = reverse('venta-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_crear_venta_con_productos(self):
        """
        Verifica crear una venta con productos incluidos.
        El serializador espera 'productos_compra' con 'producto_id' y 'cantidad'.
        """
        url = reverse('venta-list')
        data = {
            'cliente': self.cliente.id,
            'productos_compra': [
                {'producto_id': self.producto.id, 'cantidad': 3}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Venta.objects.count(), 1)
        self.assertEqual(VentaProducto.objects.count(), 1)

        # Verificar que se descontó el stock
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 17)

        # Verificar que el total se calculó correctamente
        venta = Venta.objects.first()
        self.assertEqual(float(venta.total), 225.00)  # 3 x 75.00

    def test_crear_venta_sin_stock_suficiente(self):
        """Verifica error si no hay stock suficiente."""
        url = reverse('venta-list')
        data = {
            'cliente': self.cliente.id,
            'productos_compra': [
                {'producto_id': self.producto.id, 'cantidad': 999}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_venta_producto_inexistente(self):
        """Verifica error si el producto no existe."""
        url = reverse('venta-list')
        data = {
            'cliente': self.cliente.id,
            'productos_compra': [
                {'producto_id': 99999, 'cantidad': 1}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_venta_sin_productos(self):
        """Verifica crear una venta sin productos (total = 0)."""
        url = reverse('venta-list')
        data = {
            'cliente': self.cliente.id,
            'productos_compra': []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        venta = Venta.objects.first()
        self.assertEqual(float(venta.total), 0.00)

    def test_obtener_venta_especifica(self):
        """Verifica obtener una venta por ID."""
        venta = Venta.objects.create(cliente=self.cliente, total=300.00)
        url = reverse('venta-detail', args=[venta.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total']), 300.00)

    def test_no_autenticado_listar_ventas(self):
        """Verifica que sin auth devuelva 401."""
        self.client.force_authenticate(user=None)
        url = reverse('venta-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GarantiaAPITest(APITestCase):
    """Pruebas para la API REST de Garantías."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        self.producto = Producto.objects.create(
            nombre="Anillo Diamante",
            precio=1000.00,
            stock=5,
            categoria="Anillo"
        )
        self.garantia = Garantia.objects.create(
            producto=self.producto,
            fecha_fin=date.today() + timedelta(days=365),
            estado="Activa"
        )

    def test_listar_garantias(self):
        """Verifica listar todas las garantías."""
        url = reverse('garantia-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_obtener_garantia_especifica(self):
        """Verifica obtener una garantía por producto (OneToOne)."""
        url = reverse('garantia-detail', args=[self.producto.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['estado'], 'Activa')
        self.assertIsNotNone(response.data['producto_detalle'])

    def test_crear_garantia(self):
        """Verifica crear una nueva garantía."""
        nuevo_producto = Producto.objects.create(
            nombre="Nuevo Producto",
            precio=200.00,
            stock=10,
            categoria="Anillo"
        )
        url = reverse('garantia-list')
        data = {
            'producto': nuevo_producto.id,
            'fecha_fin': (date.today() + timedelta(days=180)).isoformat(),
            'estado': 'Activa'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Garantia.objects.count(), 2)

    def test_eliminar_garantia(self):
        """Verifica eliminar una garantía."""
        url = reverse('garantia-detail', args=[self.producto.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Garantia.objects.count(), 0)
