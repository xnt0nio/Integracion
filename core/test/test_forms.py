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


    def test_precio_muy_bajo(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 0.01,
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertTrue(form.is_valid())  # Depende de si tu lógica permite precios muy bajos

    def test_precio_exacto(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100.00,
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_vencimiento_lejano(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100,
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '2100-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_stock_muy_bajo(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100,
            'stock': 1,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_tipo_producto_no_existente(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100,
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': 999  # ID de tipo de producto que no existe
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('tipo', form.errors)

    def test_vencimiento_formato_iso(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100,
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31T00:00:00Z',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('vencimiento', form.errors)

    def test_formulario_completamente_vacio(self):
        form_data = {}
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
        self.assertIn('precio', form.errors)
        self.assertIn('stock', form.errors)
        self.assertIn('descripcion', form.errors)
        self.assertIn('vencimiento', form.errors)
        self.assertIn('vigente', form.errors)
        self.assertIn('tipo', form.errors)

    def test_descripcion_con_espacios(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100,
            'stock': 50,
            'descripcion': '    ',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('descripcion', form.errors)

    def test_nombre_con_caracteres_especiales(self):
        form_data = {
            'nombre': 'Producto @#$%',
            'precio': 100,
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_precio_con_muchos_decimales(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100.123456789,
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertTrue(form.is_valid())


    def test_precio_decimal(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 99.99,
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_nombre_espacios_alrededor(self):
        form_data = {
            'nombre': '  Producto válido  ',
            'precio': 100,
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_vencimiento_letra(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100,
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '202a-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('vencimiento', form.errors)

    def test_vencimiento_letras(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100,
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': 'abcd-ef-gh',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('vencimiento', form.errors)

    def test_precio_espacio(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': ' 100 ',
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_stock_espacio(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100,
            'stock': ' 50 ',
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_precio_coma_en_vez_de_punto(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': '100,00',
            'stock': 50,
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('precio', form.errors)

    def test_stock_coma_en_vez_de_punto(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100,
            'stock': '50,0',
            'descripcion': 'Descripción válida',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('stock', form.errors)

    def test_descripcion_simbolos(self):
        form_data = {
            'nombre': 'Producto válido',
            'precio': 100,
            'stock': 50,
            'descripcion': 'Descripción con símbolos @#$%',
            'vencimiento': '2025-12-31',
            'vigente': True,
            'tipo': self.tipo_producto.id
        }
        form = ProductoForm(data=form_data)
        self.assertTrue(form.is_valid())    
    


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

    def test_cantidad_agregada_decimal(self):
        form_data = {
            'producto': self.producto.id,
            'cantidad_agregada': 10.5
        }
        form = CarritoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cantidad_agregada', form.errors)

    def test_producto_con_caracteres_especiales(self):
        form_data = {
            'producto': 'Producto @#$%',
            'cantidad_agregada': 10
        }
        form = CarritoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('producto', form.errors)

    def test_cantidad_agregada_con_espacios(self):
        form_data = {
            'producto': self.producto.id,
            'cantidad_agregada': '   '
        }
        form = CarritoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cantidad_agregada', form.errors)

    def test_producto_con_tipo_invalido(self):
        producto_tipo_invalido = Producto.objects.create(
            nombre='Producto Tipo Invalido',
            precio=100,
            stock=50,
            descripcion='Descripción del producto',
            vencimiento='2025-12-31',
            vigente=True,
            tipo=None  # Tipo de producto inválido
        )
        form_data = {
            'producto': producto_tipo_invalido.id,
            'cantidad_agregada': 10
        }
        form = CarritoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('tipo', form.errors)

    def test_formulario_completamente_vacio(self):
        form_data = {}
        form = CarritoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('producto', form.errors)
        self.assertIn('cantidad_agregada', form.errors)

    def test_producto_con_precio_negativo(self):
        producto_precio_negativo = Producto.objects.create(
            nombre='Producto Precio Negativo',
            precio=-100,
            stock=50,
            descripcion='Descripción del producto',
            vencimiento='2025-12-31',
            vigente=True,
            tipo=self.tipo_producto
        )
        form_data = {
            'producto': producto_precio_negativo.id,
            'cantidad_agregada': 10
        }
        form = CarritoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('producto', form.errors)

    def test_cantidad_agregada_negativa_una_unidad(self):
        form_data = {
            'producto': self.producto.id,
            'cantidad_agregada': -1
        }
        form = CarritoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cantidad_agregada', form.errors)

    def test_cantidad_agregada_letras(self):
        form_data = {
            'producto': self.producto.id,
            'cantidad_agregada': 'diez unidades'
        }
        form = CarritoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cantidad_agregada', form.errors)

    def test_producto_precio_no_numerico(self):
        producto_precio_no_numerico = Producto.objects.create(
            nombre='Producto Precio No Numerico',
            precio='cien',
            stock=50,
            descripcion='Descripción del producto',
            vencimiento='2025-12-31',
            vigente=True,
            tipo=self.tipo_producto
        )
        form_data = {
            'producto': producto_precio_no_numerico.id,
            'cantidad_agregada': 10
        }
        form = CarritoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('producto', form.errors)

    def test_cantidad_agregada_con_signo_mas(self):
        form_data = {
            'producto': self.producto.id,
            'cantidad_agregada': '+10'
        }
        form = CarritoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cantidad_agregada', form.errors)    


    