from django import views,forms
from django.urls import path, include
from .views import *



urlpatterns = [
    path('', index, name="index"),
    path('test', test, name="test"),
    path('productos', productos, name="productos"),
    path('descripcion', descripcion, name="descripcion"),
    path('carrito', carrito, name="carrito"),
    path('envio', envio , name="envio"),
    path('estadisticas', estadisticas , name="estadisticas"),
    path('checkout', checkout , name="checkout"),
    path('add/', add, name="add"),
]
