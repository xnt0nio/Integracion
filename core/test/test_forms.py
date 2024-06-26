from django.test import TestCase
from .forms import ProductoForm, CarritoForm
from .models import Producto, Carrito, TipoProducto

class ProductoFormTest(TestCase):

    def setUp(self):
        self.tipo_producto = TipoProducto.objects.create(descripcion='Tipo de Prueba')

    def test_producto_form_valido(self):
        form_data = {
            'nombre': 'Producto de Prueba',
            'precio': 100,
            'stock': 50,
            'descripcion': 'Esta es una descripción válida de producto.',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_producto_form_invalido(self):
        form_data = {
            'nombre': 'Pro',
            'precio': None,
            'stock': -5,
            'descripcion': 'Corta',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
        self.assertIn('precio', form.errors)
        self.assertIn('stock', form.errors)
        self.assertIn('descripcion', form.errors)

    def test_nombre_vacio(self):
        form_data = {
            'nombre': '',
            'precio': 100,
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_precio_negativo(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': -10,
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('precio', form.errors)

    def test_stock_negativo(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100,
            'stock': -10,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('stock', form.errors)

    def test_descripcion_corta(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100,
            'stock': 50,
            'descripcion': 'Corta',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('descripcion', form.errors)

    def test_vencimiento_pasado(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100,
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '2020-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertTrue(form.is_valid())  # Depende de si tu lógica permite fechas pasadas

    def test_nombre_largo(self):
        form_data = {
            'nombre': 'P' * 51,
            'precio': 100,
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_descripcion_larga(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100,
            'stock': 50,
            'descripcion': 'D' * 251,
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('descripcion', form.errors)

    def test_precio_no_numerico(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 'cien',
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('precio', form.errors)

    def test_stock_no_numerico(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100,
            'stock': 'cincuenta',
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('stock', form.errors)

    def test_sin_tipo_producto(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100,
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': None
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('tipo', form.errors)

    def test_vencimiento_formato_invalido(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100,
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '31-12-2025',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('vencimiento', form.errors)

    def test_nombre_minimo(self):
        form_data = {
            'nombre': 'Pr',
            'precio': 100,
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_precio_muy_alto(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 1000000000,
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertTrue(form.is_valid())  # Depende de si tu lógica permite precios muy altos

    def test_stock_muy_alto(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100,
            'stock': 1000000000,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertTrue(form.is_valid())  # Depende de si tu lógica permite stocks muy altos


class CarritoFormTest(TestCase):

    def setUp(self):
        self.tipo_producto = TipoProducto.objects.create(descripcion='Tipo de Prueba')
        self.producto = Producto.objects.create(
            nombre='Producto',
            precio=100,
            stock=50,
            descripcion='Descripción del producto',
            vencimiento='2025-12-31',
            vigente=True,
            tipo=self.tipo_producto
        )

    def test_carrito_form_valido(self):
        form_data = {
            'producto': self.producto.id,
            'cantidad_agregada': 10
        }
        form = CarritoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_carrito_form_invalido(self):
        form_data = {
            'producto': self.producto.id,
            'cantidad_agregada': -1
        }
        form = CarritoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn('La cantidad agregada no puede ser negativa', form.errors['__all__'])

    def test_sin_producto(self):
        form_data = {
            'producto': None,
            'cantidad_agregada': 10
        }
        form = CarritoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('producto', form.errors)

    def test_cantidad_agregada_nula(self):
        form_data = {
            'producto': self.producto.id,
            'cantidad_agregada': None
        }
        form = CarritoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cantidad_agregada', form.errors)

    def test_cantidad_agregada_muy_alta(self):
        form_data = {
            'producto': self.producto.id,
            'cantidad_agregada': 1000000
        }
        form = CarritoForm(data=form_data)
        self.assertTrue(form.is_valid())  # Depende de si tu lógica permite cantidades muy altas

    def test_producto_no_existente(self):
        form_data = {
            'producto': 999,  # ID de producto que no existe
            'cantidad_agregada': 10
        }
        form = CarritoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('producto', form.errors)

    def test_cantidad_agregada_no_numerica(self):
        form_data = {
            'producto': self.producto.id,
            'cantidad_agregada': 'diez'
        }
        form = CarritoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cantidad_agregada', form.errors)

    def test_producto_con_espacios(self):
        form_data = {
            'producto': ' ',
            'cantidad_agregada': 10
        }
        form = CarritoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('producto', form.errors)

    

    def test_producto_inactivo(self):
        producto_inactivo = Producto.objects.create(
            nombre='Producto Inactivo',
            precio=100,
            stock=50,
            descripcion='Descripción del producto',
            vencimiento='2025-12-31',
            vigente=False,
            tipo=self.tipo_producto
        )
        form_data = {
            'producto': producto_inactivo.id,
            'cantidad_agregada': 10
        }
        form = CarritoForm(data=form_data)
        self.assertTrue(form.is_valid())  # Depende de si tu lógica permite productos inactivos

    def test_cantidad_agregada_cero(self):
        form_data = {
            'producto': self.producto.id,
            'cantidad_agregada': 0
        }
        form = CarritoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_producto_vencido(self):
        producto_vencido = Producto.objects.create(
            nombre='Producto Vencido',
            precio=100,
            stock=50,
            descripcion='Descripción del producto',
            vencimiento='2020-12-31',
            vigente=True,
            tipo=self.tipo_producto
        )
        form_data = {
            'producto': producto_vencido.id,
            'cantidad_agregada': 10
        }
        form = CarritoForm(data=form_data)
        self.assertTrue(form.is_valid())  # Depende de si tu lógica permite productos vencidos

    def test_producto_con_stock_insuficiente(self):
        form_data = {
            'producto': self.producto.id,
            'cantidad_agregada': 100
        }
        form = CarritoForm(data=form_data)
        self.assertTrue(form.is_valid())  # Depende de si tu lógica valida el stock disponible

    def test_producto_con_stock_justo(self):
        form_data = {
            'producto': self.producto.id,
            'cantidad_agregada': 50
        }
        form = CarritoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_producto_con_stock_exacto(self):
        form_data = {
            'producto': self.producto.id,
            'cantidad_agregada': 50
        }
        form = CarritoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_carrito_form_vacio(self):
        form_data = {}
        form = CarritoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('producto', form.errors)
        self.assertIn('cantidad_agregada', form.errors)
