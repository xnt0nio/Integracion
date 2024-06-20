from django.test import TestCase
from core.models import TipoProducto, Producto, Carrito, Payment
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError

class TipoProductoModelTest(TestCase):

    def test_crear_tipoproducto(self):
        tipoproducto = TipoProducto.objects.create(descripcion='herramientas')
        self.assertEqual(tipoproducto.descripcion, 'herramientas')

    def test_str_tipoproducto(self):
        tipoproducto = TipoProducto.objects.create(descripcion='herramientas')
        self.assertEqual(str(tipoproducto), 'herramientas')

    def test_crear_tipoproducto_descripcion_vacia(self):
        with self.assertRaises(ValidationError):
            tipoproducto = TipoProducto(descripcion='')
            tipoproducto.full_clean()

    def test_actualizar_tipoproducto(self):
        tipoproducto = TipoProducto.objects.create(descripcion='herramientas')
        tipoproducto.descripcion = 'electrónica'
        tipoproducto.save()
        self.assertEqual(tipoproducto.descripcion, 'electrónica')

    def test_eliminar_tipoproducto(self):
        tipoproducto = TipoProducto.objects.create(descripcion='herramientas')
        tipoproducto_id = tipoproducto.id
        tipoproducto.delete()
        self.assertFalse(TipoProducto.objects.filter(id=tipoproducto_id).exists())

class ProductoModelTest(TestCase):

    def setUp(self):
        self.tipoproducto = TipoProducto.objects.create(descripcion='herramientas')

    def test_crear_producto(self):
        producto = Producto.objects.create(
            nombre='Alguacil Electrico',
            precio=50,
            stock=10,
            descripcion='Alguacil electronico',
            tipo=self.tipoproducto,
            vigente=True
        )
        self.assertEqual(producto.nombre, 'Alguacil Electrico')
        self.assertEqual(producto.precio, 50)
        self.assertEqual(producto.tipo, self.tipoproducto)
        self.assertEqual(producto.descripcion, 'Alguacil electronico')

    def test_str_producto(self):
        producto = Producto.objects.create(
            nombre='Alguacil Electrico',
            precio=50,
            stock=10,
            descripcion='Alguacil electronico',
            tipo=self.tipoproducto,
            vigente=True
        )
        self.assertEqual(str(producto), 'Alguacil Electrico')

    def test_foreignkey_producto(self):
        producto = Producto.objects.create(
            nombre='Alguacil Electrico',
            precio=50,
            stock=10,
            descripcion='Alguacil electronico',
            tipo=self.tipoproducto,
            vigente=True
        )
        self.assertEqual(producto.tipo.descripcion, 'herramientas')

    def test_crear_producto_precio_negativo(self):
        with self.assertRaises(ValidationError):
            producto = Producto(
                nombre='Producto Negativo',
                precio=-10,
                stock=5,
                descripcion='Descripción',
                tipo=self.tipoproducto,
                vigente=True
            )
            producto.full_clean()

    def test_actualizar_producto(self):
        producto = Producto.objects.create(
            nombre='Alguacil Electrico',
            precio=50,
            stock=10,
            descripcion='Alguacil electronico',
            tipo=self.tipoproducto,
            vigente=True
        )
        producto.precio = 100
        producto.save()
        self.assertEqual(producto.precio, 100)

    def test_eliminar_producto(self):
        producto = Producto.objects.create(
            nombre='Alguacil Electrico',
            precio=50,
            stock=10,
            descripcion='Alguacil electronico',
            tipo=self.tipoproducto,
            vigente=True
        )
        producto_id = producto.id
        producto.delete()
        self.assertFalse(Producto.objects.filter(id=producto_id).exists())

    def test_vencimiento_por_defecto(self):
        producto = Producto.objects.create(
            nombre='Producto Nuevo',
            precio=50,
            stock=10,
            descripcion='Descripción',
            tipo=self.tipoproducto,
            vigente=True
        )
        self.assertEqual(producto.vencimiento, date.today())

    def test_crear_producto_sin_nombre(self):
        with self.assertRaises(ValidationError):
            producto = Producto(
                nombre='',
                precio=50,
                stock=10,
                descripcion='Descripción',
                tipo=self.tipoproducto,
                vigente=True
            )
            producto.full_clean()

class CarritoModelTest(TestCase):

    def setUp(self):
        self.tipoproducto = TipoProducto.objects.create(descripcion='herramientas')
        self.producto = Producto.objects.create(
            nombre='Alguacil Electrico',
            precio=50,
            stock=10,
            descripcion='Alguacil electronico',
            tipo=self.tipoproducto,
            vigente=True
        )
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_crear_carrito(self):
        carrito = Carrito.objects.create(
            usuario=self.user,
            producto=self.producto,
            cantidad_agregada=3
        )
        self.assertEqual(carrito.cantidad_agregada, 3)

    def test_actualizar_carrito(self):
        carrito = Carrito.objects.create(
            usuario=self.user,
            producto=self.producto,
            cantidad_agregada=3
        )
        carrito.cantidad_agregada = 5
        carrito.save()
        self.assertEqual(carrito.cantidad_agregada, 5)

    def test_eliminar_carrito(self):
        carrito = Carrito.objects.create(
            usuario=self.user,
            producto=self.producto,
            cantidad_agregada=3
        )
        carrito_id = carrito.id
        carrito.delete()
        self.assertFalse(Carrito.objects.filter(id=carrito_id).exists())

    def test_crear_carrito_cantidad_negativa(self):
        with self.assertRaises(ValidationError):
            carrito = Carrito(
                usuario=self.user,
                producto=self.producto,
                cantidad_agregada=-1
            )
            carrito.full_clean()

    def test_relacion_carrito_usuario(self):
        carrito = Carrito.objects.create(
            usuario=self.user,
            producto=self.producto,
            cantidad_agregada=3
        )
        self.assertEqual(carrito.usuario.username, 'testuser')

    def test_crear_carrito_usuario_inexistente(self):
        with self.assertRaises(ValidationError):
            carrito = Carrito(
                usuario=None,
                producto=self.producto,
                cantidad_agregada=3
            )
            carrito.full_clean()

class PaymentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_crear_payment(self):
        payment = Payment.objects.create(
            user=self.user,
            stripe_charge_id='ch_1F2hJ0EjHbXRQy',
            amount=100.00,
            name='Test User',
            email='test@example.com',
            address='123 Test St',
            phone='1234567890'
        )
        self.assertEqual(payment.amount, 100.00)

    def test_actualizar_payment(self):
        payment = Payment.objects.create(
            user=self.user,
            stripe_charge_id='ch_1F2hJ0EjHbXRQy',
            amount=100.00,
            name='Test User',
            email='test@example.com',
            address='123 Test St',
            phone='1234567890'
        )
        payment.amount = 200.00
        payment.save()
        self.assertEqual(payment.amount, 200.00)

    def test_eliminar_payment(self):
        payment = Payment.objects.create(
            user=self.user,
            stripe_charge_id='ch_1F2hJ0EjHbXRQy',
            amount=100.00,
            name='Test User',
            email='test@example.com',
            address='123 Test St',
            phone='1234567890'
        )
        payment_id = payment.id
        payment.delete()
        self.assertFalse(Payment.objects.filter(id=payment_id).exists())

    def test_relacion_payment_usuario(self):
        payment = Payment.objects.create(
            user=self.user,
            stripe_charge_id='ch_1F2hJ0EjHbXRQy',
            amount=100.00,
            name='Test User',
            email='test@example.com',
            address='123 Test St',
            phone='1234567890'
        )
        self.assertEqual(payment.user.username, 'testuser')

    def test_validacion_email_payment(self):
        with self.assertRaises(ValidationError):
            payment = Payment(
                user=self.user,
                stripe_charge_id='ch_1F2hJ0EjHbXRQy',
                amount=100.00,
                name='Test User',
                email='invalid_email',
                address='123 Test St',
                phone='1234567890'
            )
            payment.full_clean()

    def test_validacion_phone_payment(self):
        with self.assertRaises(ValidationError):
            payment = Payment(
                user=self.user,
                stripe_charge_id='ch_1F2hJ0EjHbXRQy',
                amount=100.00,
                name='Test User',
                email='test@example.com',
                address='123 Test St',
                phone='invalid_phone'
            )
            payment.full_clean()

class ProductoValidacionTest(TestCase):

    def setUp(self):
        self.tipoproducto = TipoProducto.objects.create(descripcion='herramientas')

    def test_validacion_longitud_nombre_producto(self):
        with self.assertRaises(ValidationError):
            producto = Producto(
                nombre='A'*51,
                precio=50,
                stock=10,
                descripcion='Descripción',
                tipo=self.tipoproducto,
                vigente=True
            )
            producto.full_clean()

    def test_validacion_longitud_descripcion_producto(self):
        with self.assertRaises(ValidationError):
            producto = Producto(
                nombre='Producto',
                precio=50,
                stock=10,
                descripcion='D'*251,
                tipo=self.tipoproducto,
                vigente=True
            )
            producto.full_clean()

    def test_validacion_cantidad_minima_stock_producto(self):
        with self.assertRaises(ValidationError):
            producto = Producto(
                nombre='Producto',
                precio=50,
                stock=-1,
                descripcion='Descripción',
                tipo=self.tipoproducto,
                vigente=True
            )
            producto.full_clean()

    def test_validacion_cantidad_minima_precio_producto(self):
        with self.assertRaises(ValidationError):
            producto = Producto(
                nombre='Producto',
                precio=-1,
                stock=10,
                descripcion='Descripción',
                tipo=self.tipoproducto,
                vigente=True
            )
            producto.full_clean()
