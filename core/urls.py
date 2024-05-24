from django.urls import include, path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('test', test, name="test"),
    path('productos', productos, name="productos"),
    path('descripcion/<id>/', descripcion, name="descripcion"),
    path('carrito', carrito, name="carrito"),
    path('envio', envio , name="envio"),
    path('estadisticas', estadisticas , name="estadisticas"),
    path('checkout', checkout , name="checkout"),
    path('add/', add, name="add"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('eliminar_producto/<id>/', eliminar_producto, name="eliminar_producto"),
    path('calcular_total/', calcular_total, name='calcular_total'),
    path('registro/', registro, name='registro'),
  
    
]