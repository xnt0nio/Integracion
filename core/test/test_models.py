from django.test import TestCase
from core.models import *

class TipoProductoModelTest(TestCase):

        def test_crear_tipoproducto(self):
                tipoproducto = TipoProducto.objects.create(nombre='Construcción')
                self.assertEqual(tipoproducto.nombre,'Construcción')

        def test_str_tipoproducto(self):
                tipoproducto = TipoProducto.objects.create(nombre='Construcción')
                self.assertEqual(str(tipoproducto),'Construcción')

class ProductoModelTest(TestCase):

        def setUp(self):
                self.tipoproducto = TipoProducto.objects.create(nombre='Construcción')


        def test_crear_producto(self):
                producto = Producto.objects.create(
                        nombre ='Alguacil Electrico',
                        precio = 50,
                        tipo = self.tipoproducto,
                        descripcion = 'Alguacil electronico'

                )
                self.assertEqual(producto.nombre,'Alguacil Electrico')
                self.assertEqual(producto.precio, 50)
                self.assertEqual(producto.tipo, self.tipoproducto)
                self.assertEqual(producto.descripcion,'Alguacil electronico')

        def test_str_producto(self):
                producto = Producto.objects.create(
                        nombre ='Alguacil Electrico',
                        precio = 50,
                        tipo = self.tipoproducto,
                        descripcion = 'Alguacil electronico'
                )
                self.assertEqual(str(producto), 'Alguacil Electrico' )

        def test_foreignket_producto(self):
                producto = Producto.objects.create(
                        nombre ='Alguacil Electrico',
                        precio = 50,
                        tipo = self.tipoproducto,
                        descripcion = 'Alguacil electronico'
                )
                self.assertEqual(producto.tipo.nombre, 'Construcción' )



