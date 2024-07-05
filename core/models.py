from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class TipoProducto(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion
    



class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    stock = models.IntegerField()
    descripcion = models.CharField(max_length=250)
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    vencimiento = models.DateField(default=date.today)
    imagen = models.ImageField(null=True, blank=True)
    vigente = models.BooleanField()

    def clean(self):
        if self.precio is None or self.precio < 0:
            raise ValidationError('El precio no puede ser negativo o nulo')
        if self.stock is None or self.stock < 0:
            raise ValidationError('El stock no puede ser negativo o nulo')
        if not self.nombre:
            raise ValidationError('El nombre no puede estar vacío')
        if len(self.nombre) > 50:
            raise ValidationError('El nombre no puede tener más de 50 caracteres')
        if len(self.descripcion) > 250:
            raise ValidationError('La descripción no puede tener más de 250 caracteres')

    def __str__(self):
        return self.nombre


class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_agregada = models.IntegerField(default=0)

    class Meta:
        db_table = 'db_carrito'

    def clean(self):
        if self.cantidad_agregada < 0:
            raise ValidationError('La cantidad agregada no puede ser negativa')

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_charge_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    # New fields for product details
    product_name = models.CharField(max_length=50, null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product_quantity = models.IntegerField(null=True, blank=True)
    product_image = models.ImageField(null=True, blank=True)

    def clean(self):
        if self.email and '@' not in self.email:
            raise ValidationError('Email inválido')
        if self.phone and not self.phone.isdigit():
            raise ValidationError('Teléfono inválido')

    def __str__(self):
        return f'Pago de {self.user.username} por {self.amount} USD'
