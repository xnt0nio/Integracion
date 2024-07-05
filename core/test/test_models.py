from django.test import TestCase
from core.models import TipoProducto, Producto, Carrito, Payment
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError

class TipoProductoModelTest(TestCase):
    # Prueba para crear un TipoProducto con una descripción válida
    def test_crear_tipoproducto(self):
        tipoproducto = TipoProducto.objects.create(descripcion='herramientas')
        self.assertEqual(tipoproducto.descripcion, 'herramientas')

    # Prueba para verificar la representación en cadena de un TipoProducto
    def test_str_tipoproducto(self):
        tipoproducto = TipoProducto.objects.create(descripcion='herramientas')
        self.assertEqual(str(tipoproducto), 'herramientas')

    # Prueba para crear un TipoProducto con una descripción vacía y esperar un ValidationError
    def test_crear_tipoproducto_descripcion_vacia(self):
        with self.assertRaises(ValidationError):
            tipoproducto = TipoProducto(descripcion='')
            tipoproducto.full_clean()

    # Prueba para actualizar la descripción de un TipoProducto
    def test_actualizar_tipoproducto(self):
        tipoproducto = TipoProducto.objects.create(descripcion='herramientas')
        tipoproducto.descripcion = 'electrónica'
        tipoproducto.save()
        self.assertEqual(tipoproducto.descripcion, 'electrónica')

    # Prueba para eliminar un TipoProducto
    def test_eliminar_tipoproducto(self):
        tipoproducto = TipoProducto.objects.create(descripcion='herramientas')
        tipoproducto_id = tipoproducto.id
        tipoproducto.delete()
        self.assertFalse(TipoProducto.objects.filter(id=tipoproducto_id).exists())

    def test_crear_multiples_tipoproducto(self):
        tipos = ['herramientas', 'electrónica', 'ropa', 'alimentos']
        for tipo in tipos:
            TipoProducto.objects.create(descripcion=tipo)
        self.assertEqual(TipoProducto.objects.count(), 4)

    # Prueba para crear un TipoProducto con descripción duplicada
    def test_crear_tipoproducto_duplicado(self):
        TipoProducto.objects.create(descripcion='herramientas')
        with self.assertRaises(ValidationError):
            tipo_duplicado = TipoProducto(descripcion='herramientas')
            tipo_duplicado.full_clean()

    # Prueba para validar que la descripción de TipoProducto no exceda los 100 caracteres
    def test_validacion_longitud_descripcion_tipoproducto(self):
        with self.assertRaises(ValidationError):
            tipoproducto = TipoProducto(
                descripcion='a' * 101
            )
            tipoproducto.full_clean()

    # Prueba para crear un TipoProducto con espacios en blanco
    def test_crear_tipoproducto_espacios_blanco(self):
        with self.assertRaises(ValidationError):
            tipoproducto = TipoProducto(
                descripcion='   '
            )
            tipoproducto.full_clean()

    # Prueba para crear un TipoProducto con caracteres especiales
    def test_crear_tipoproducto_caracteres_especiales(self):
        tipoproducto = TipoProducto.objects.create(descripcion='herramientas @#$')
        self.assertEqual(tipoproducto.descripcion, 'herramientas @#$')    

class ProductoModelTest(TestCase):

    def setUp(self):
        self.tipoproducto = TipoProducto.objects.create(descripcion='herramientas')

    # Prueba para crear un Producto con valores válidos
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

    # Prueba para verificar la representación en cadena de un Producto
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

    # Prueba para verificar la relación entre Producto y TipoProducto
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

    # Prueba para crear un Producto con un precio negativo y esperar un ValidationError
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

    # Prueba para actualizar el precio de un Producto
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

    # Prueba para eliminar un Producto
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

    # Prueba para verificar que el vencimiento de un Producto sea la fecha actual por defecto
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

    # Prueba para crear un Producto sin nombre y esperar un ValidationError
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

    def test_crear_producto_nombre_duplicado(self):
        Producto.objects.create(
            nombre='Alguacil Electrico',
            precio=50,
            stock=10,
            descripcion='Alguacil electronico',
            tipo=self.tipoproducto,
            vigente=True
        )
        with self.assertRaises(ValidationError):
            producto_duplicado = Producto(
                nombre='Alguacil Electrico',
                precio=50,
                stock=10,
                descripcion='Alguacil electronico',
                tipo=self.tipoproducto,
                vigente=True
            )
            producto_duplicado.full_clean()

    # Prueba para crear un Producto con stock cero
    def test_crear_producto_stock_cero(self):
        producto = Producto.objects.create(
            nombre='Producto Stock Cero',
            precio=50,
            stock=0,
            descripcion='Descripción del producto',
            tipo=self.tipoproducto,
            vigente=True
        )
        self.assertEqual(producto.stock, 0)

    # Prueba para actualizar el stock de un Producto
    def test_actualizar_stock_producto(self):
        producto = Producto.objects.create(
            nombre='Alguacil Electrico',
            precio=50,
            stock=10,
            descripcion='Alguacil electronico',
            tipo=self.tipoproducto,
            vigente=True
        )
        producto.stock = 20
        producto.save()
        self.assertEqual(producto.stock, 20)

    # Prueba para crear un Producto con descripción con solo espacios
    def test_crear_producto_descripcion_espacios(self):
        with self.assertRaises(ValidationError):
            producto = Producto(
                nombre='Producto Espacios',
                precio=50,
                stock=10,
                descripcion='   ',
                tipo=self.tipoproducto,
                vigente=True
            )
            producto.full_clean()

    # Prueba para crear un Producto con precio no numérico
    def test_crear_producto_precio_no_numerico(self):
        with self.assertRaises(ValidationError):
            producto = Producto(
                nombre='Producto No Numerico',
                precio='cincuenta',
                stock=10,
                descripcion='Descripción del producto',
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

    # Prueba para crear un Carrito con valores válidos
    def test_crear_carrito(self):
        carrito = Carrito.objects.create(
            usuario=self.user,
            producto=self.producto,
            cantidad_agregada=3
        )
        self.assertEqual(carrito.cantidad_agregada, 3)

    # Prueba para actualizar la cantidad agregada en un Carrito
    def test_actualizar_carrito(self):
        carrito = Carrito.objects.create(
            usuario=self.user,
            producto=self.producto,
            cantidad_agregada=3
        )
        carrito.cantidad_agregada = 5
        carrito.save()
        self.assertEqual(carrito.cantidad_agregada, 5)

    # Prueba para eliminar un Carrito
    def test_eliminar_carrito(self):
        carrito = Carrito.objects.create(
            usuario=self.user,
            producto=self.producto,
            cantidad_agregada=3
        )
        carrito_id = carrito.id
        carrito.delete()
        self.assertFalse(Carrito.objects.filter(id=carrito_id).exists())

    # Prueba para crear un Carrito con cantidad negativa y esperar un ValidationError
    def test_crear_carrito_cantidad_negativa(self):
        with self.assertRaises(ValidationError):
            carrito = Carrito(
                usuario=self.user,
                producto=self.producto,
                cantidad_agregada=-1
            )
            carrito.full_clean()

    # Prueba para verificar la relación entre Carrito y Usuario
    def test_relacion_carrito_usuario(self):
        carrito = Carrito.objects.create(
            usuario=self.user,
            producto=self.producto,
            cantidad_agregada=3
        )
        self.assertEqual(carrito.usuario.username, 'testuser')

    # Prueba para crear un Carrito con usuario inexistente y esperar un ValidationError
    def test_crear_carrito_usuario_inexistente(self):
        with self.assertRaises(ValidationError):
            carrito = Carrito(
                usuario=None,
                producto=self.producto,
                cantidad_agregada=3
            )
            carrito.full_clean()



    def test_crear_carrito_cantidad_cero(self):
        carrito = Carrito.objects.create(
            usuario=self.user,
            producto=self.producto,
            cantidad_agregada=0
        )
        self.assertEqual(carrito.cantidad_agregada, 0)

    # Prueba para crear un Carrito con producto sin stock
    def test_crear_carrito_producto_sin_stock(self):
        producto_sin_stock = Producto.objects.create(
            nombre='Producto Sin Stock',
            precio=50,
            stock=0,
            descripcion='Descripción del producto',
            tipo=self.tipoproducto,
            vigente=True
        )
        with self.assertRaises(ValidationError):
            carrito = Carrito(
                usuario=self.user,
                producto=producto_sin_stock,
                cantidad_agregada=1
            )
            carrito.full_clean()

    # Prueba para actualizar el producto en un Carrito
    def test_actualizar_producto_carrito(self):
        producto_nuevo = Producto.objects.create(
            nombre='Producto Nuevo',
            precio=60,
            stock=15,
            descripcion='Descripción del producto nuevo',
            tipo=self.tipoproducto,
            vigente=True
        )
        carrito = Carrito.objects.create(
            usuario=self.user,
            producto=self.producto,
            cantidad_agregada=3
        )
        carrito.producto = producto_nuevo
        carrito.save()
        self.assertEqual(carrito.producto, producto_nuevo)

    # Prueba para verificar la relación entre Carrito y Producto
    def test_relacion_carrito_producto(self):
        carrito = Carrito.objects.create(
            usuario=self.user,
            producto=self.producto,
            cantidad_agregada=3
        )
        self.assertEqual(carrito.producto.nombre, 'Alguacil Electrico')

    # Prueba para crear un Carrito con cantidad decimal
    def test_crear_carrito_cantidad_decimal(self):
        with self.assertRaises(ValidationError):
            carrito = Carrito(
                usuario=self.user,
                producto=self.producto,
                cantidad_agregada=1.5
            )
            carrito.full_clean()        

class PaymentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    # Prueba para crear un Payment con valores válidos
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

    # Prueba para actualizar el monto de un Payment
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

    # Prueba para eliminar un Payment
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

    # Prueba para verificar la relación entre Payment y Usuario
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

    # Prueba para crear un Payment con un email inválido y esperar un ValidationError
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

    # Prueba para crear un Payment con un teléfono inválido y esperar un ValidationError
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

    def test_validacion_nombre_vacio_payment(self):
        with self.assertRaises(ValidationError):
            payment = Payment(
                user=self.user,
                stripe_charge_id='ch_1F2hJ0EjHbXRQy',
                amount=100.00,
                name='',
                email='test@example.com',
                address='123 Test St',
                phone='1234567890'
            )
            payment.full_clean()

    # Prueba para crear un Payment sin dirección y esperar un ValidationError
    def test_validacion_direccion_vacia_payment(self):
        with self.assertRaises(ValidationError):
            payment = Payment(
                user=self.user,
                stripe_charge_id='ch_1F2hJ0EjHbXRQy',
                amount=100.00,
                name='Test User',
                email='test@example.com',
                address='',
                phone='1234567890'
            )
            payment.full_clean()

    # Prueba para verificar que el amount de Payment sea positivo
    def test_validacion_amount_positivo_payment(self):
        with self.assertRaises(ValidationError):
            payment = Payment(
                user=self.user,
                stripe_charge_id='ch_1F2hJ0EjHbXRQy',
                amount=-100.00,
                name='Test User',
                email='test@example.com',
                address='123 Test St',
                phone='1234567890'
            )
            payment.full_clean()

    # Prueba para crear un Payment con un stripe_charge_id inválido y esperar un ValidationError
    def test_validacion_stripe_charge_id_invalido_payment(self):
        with self.assertRaises(ValidationError):
            payment = Payment(
                user=self.user,
                stripe_charge_id='',
                amount=100.00,
                name='Test User',
                email='test@example.com',
                address='123 Test St',
                phone='1234567890'
            )
            payment.full_clean()

    # Prueba para verificar que el teléfono de Payment tenga una longitud válida
    def test_validacion_longitud_telefono_payment(self):
        with self.assertRaises(ValidationError):
            payment = Payment(
                user=self.user,
                stripe_charge_id='ch_1F2hJ0EjHbXRQy',
                amount=100.00,
                name='Test User',
                email='test@example.com',
                address='123 Test St',
                phone='123'
            )
            payment.full_clean()        

class ProductoValidacionTest(TestCase):

    def setUp(self):
        self.tipoproducto = TipoProducto.objects.create(descripcion='herramientas')

    # Prueba para validar que el nombre del Producto no exceda los 50 caracteres
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

    # Prueba para validar que la descripción del Producto no exceda los 250 caracteres
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

    # Prueba para validar que el stock del Producto no sea negativo
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

    # Prueba para validar que el precio del Producto no sea negativo
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

# Prueba adicional para verificar la longitud máxima del email en Payment
class PaymentEmailLengthTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    # Prueba para validar que el email del Payment no exceda los 254 caracteres
    def test_validacion_longitud_email_payment(self):
        with self.assertRaises(ValidationError):
            email_largo = 'a' * 245 + '@example.com'
            payment = Payment(
                user=self.user,
                stripe_charge_id='ch_1F2hJ0EjHbXRQy',
                amount=100.00,
                name='Test User',
                email=email_largo,
                address='123 Test St',
                phone='1234567890'
            )
            payment.full_clean()
