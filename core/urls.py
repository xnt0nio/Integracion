from django.contrib.auth.decorators import login_required
from django.urls import include, path
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('productos', ProductoViewsets)
router.register('tipoproductos', TipoProductoViewsets)
router.register('payment', PaymentViewsets)

urlpatterns = [
    path('', index, name="index"),
    path('api/', include(router.urls)),
    path('test', test, name="test"),
    path('productos', productos, name="productos"),
    path('descripcion/<id>/', descripcion, name="descripcion"),
    path('carrito', login_required(carrito), name="carrito"),
    path('envio', envio, name="envio"),
    path('estadisticas', estadisticas, name="estadisticas"),
    path('checkout', login_required(checkout), name="checkout"),
    path('add/', add, name="add"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('eliminar_producto/<id>/', eliminar_producto, name="eliminar_producto"),
    path('update/<id>/', update, name="update"),
    path('delete/<id>/', delete, name="delete"),
    path('calcular_total/', calcular_total, name='calcular_total'),
    path('registro/', registro, name='registro'),
    path('seleccionVentas/', seleccionVentas, name='seleccionVentas'),
    path('aprobarProductos/', aprobarProductos, name='aprobarProductos'),
    path('aprobarTransferencias/', aprobarTransferencias, name='aprobarTransferencias'),
    path('indexapi', indexapi, name="indexapi"),
    path('historialPagos/', login_required(historialPagos), name='historialPagos'),
    path('success/', login_required(success), name='success'),
    path('cancel/', cancel, name='cancel'),
    path('receipt/<int:payment_id>/', login_required(receipt), name='receipt'),
]
