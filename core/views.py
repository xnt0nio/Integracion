from django.shortcuts import render
from .forms import *
from .models import *





def index(request):
    return render(request, 'core/index.html')


def test(request):
    return render(request, 'core/test.html')


def productos(request):
    return render(request, 'core/productos.html')



def descripcion(request):
    return render(request, 'core/descripcion.html')


def carrito(request):
    return render(request, 'core/carrito.html')


def checkout(request):
    return render(request, 'core/checkout.html')

def envio(request):
    return render(request, 'core/envio.html')


def estadisticas(request):
    return render(request, 'core/estadisticas.html')


def add(request):
    data = {
        'form' : ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES) # OBTIENE LA DATA DEL FORMULARIO
        if formulario.is_valid():
            formulario.save() # INSERT INTO.....
            #data['msj'] = "Producto guardado correctamente"
            print(request, "Producto almacenado correctamente")
    return render(request, 'core/add-product.html', data)