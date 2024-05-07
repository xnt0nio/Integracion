from django.shortcuts import render







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
