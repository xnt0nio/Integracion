from decimal import Decimal
from email.headerregistry import Group
from pyexpat.errors import messages
from django.http import Http404
from django.shortcuts import redirect, render
from .forms import *
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, get_object_or_404




def index(request):
    return render(request, 'core/index.html')


def test(request):
    return render(request, 'core/test.html')


def productos(request):
    categorias = TipoProducto.objects.all()  # Obtén todos los tipos de productos (categorías)
    #categoria_seleccionada = request.GET.get('categoria')  # Obtiene la categoría seleccionada de la URL

    
    #if categoria_seleccionada:  # Si se seleccionó una categoría
       #productosAll = Producto.objects.filter(tipo__descripcion=categoria_seleccionada)
    #else:
    productosAll = Producto.objects.all()

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(productosAll, 5)
        productosAll = paginator.page(page)
    except:
        raise Http404

    data = {
        'listado': productosAll,
        'paginator': paginator,
        'categorias': categorias,
        #'categoria_seleccionada': categoria_seleccionada
    }
    return render(request, 'core/productos.html',data)





def descripcion(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        try:
            cantidad_agregada = int(request.POST.get('cantidad_agregada', 1))
        except ValueError:
            messages.error(request, "Por favor, introduce una cantidad válida.")
            return render(request, 'core/descripcion.html', {'Productos': producto})
        
        if cantidad_agregada < 1:
            messages.error(request, "La cantidad debe ser al menos 1.")
            return render(request, 'core/descripcion.html', {'Productos': producto})

        if producto.stock >= cantidad_agregada:
            carrito, created = Carrito.objects.get_or_create(usuario=request.user, producto=producto, defaults={'cantidad_agregada': 0})
            
            carrito.cantidad_agregada += cantidad_agregada
          
            carrito.save()

            producto.stock -= cantidad_agregada
            producto.precio
            producto.save()

            messages.success(request, "Producto agregado correctamente al carrito")
        else:
            messages.error(request, "No hay suficiente stock disponible")

    return render(request, 'core/descripcion.html', {'Productos': producto})




def carrito(request):
    carrito_items = Carrito.objects.filter(usuario=request.user)
    total_precio = 0

    productos_en_carrito = []

    for item in carrito_items:
        subtotal_producto = item.producto.precio * item.cantidad_agregada
        total_precio += subtotal_producto
        
        productos_en_carrito.append({
            'producto': item.producto,
            'cantidad_agregada': item.cantidad_agregada,
            'total_producto': subtotal_producto,
            'valor': item.producto.precio  
        })

    datos = {
        'listarproductos': productos_en_carrito,
        'total_precio': total_precio
    }
    return render(request, 'core/carrito.html', datos)




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

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            grupo = Group.objects.get(name="cliente")
            user.groups.add(grupo)
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            #redirigir al home
            return redirect(to="index")
        data["form"] = formulario    
    return render(request, 'registration/registro.html',data)


def eliminar_producto(request, id):
    carro = Carrito.objects.get(id=id)
    producto = carro.producto

    # Sumar la cantidad del carrito al stock del producto
    producto.stock += carro.cantidad_agregada
    producto.save()

    carro.delete()
    return redirect("carrito")