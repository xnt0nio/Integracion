
# VAMOS A CREAR UN FORMULARIO QUE SE REUTILIZA EN EL AGREGAR Y ACTUALIZAR
from django import forms
from django.forms import ModelForm
from .models import Producto, Carrito
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductoForm(ModelForm):
    nombre = forms.CharField(min_length=4, widget=forms.TextInput(attrs={"placeholder": "Ingrese Nombre"}))
    precio = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={"placeholder": "Ingrese Precio"}))
    stock = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={"placeholder": "Ingrese Stock"}))
    descripcion = forms.CharField(min_length=10, max_length=250, widget=forms.Textarea(attrs={"rows": 4}))

    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'vencimiento': forms.DateInput(attrs={'type': 'date'})
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', "first_name", "last_name", "email", "password1", "password2"]

class CarritoForm(forms.ModelForm):
    class Meta:
        model = Carrito
        fields = ['producto', 'cantidad_agregada']
