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
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import *

class ProductoViewsets(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    #queryset = Producto.objects.filter()

    serializer_class = ProductoSerializer

class TipoProductoViewsets(viewsets.ModelViewSet):
    queryset = TipoProducto.objects.all()
    #queryset = Producto.objects.filter()

    serializer_class = TipoProductoSerializer


def indexapi(request):
    # Obtiene los datos del API
    respuesta = requests.get('http://127.0.0.1:8000/api/productos/')
    productos = respuesta.json()
    data = {
        'listado': productos,
    }
    return render(request, 'core/indexapi.html', data)    



def index(request):
    categorias = TipoProducto.objects.all()  # Obtiene todos los tipos de productos (categorías)
    productosAll = Producto.objects.all()  # Obtiene todos los productos

    page = request.GET.get('page', 1)  # Obtiene el número de página actual

    try:
        paginator = Paginator(productosAll, 5)  # Pagina los productos, 5 por página
        productosAll = paginator.page(page)
    except:
        raise Http404  # Si la página no es válida, muestra un error 404

    data = {
        'listado': productosAll,
        'paginator': paginator,
        'categorias': categorias,
    }
    return render(request, 'core/index.html', data)


def test(request):
    return render(request, 'core/test.html')



def seleccionVentas(request):
    return render(request, 'core/seleccionVentas.html')


def aprobarProductos(request):
    return render(request, 'core/aprobarProductos.html')


def aprobarTransferencias(request):
    return render(request, 'core/aprobarTransferencias.html')

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
    categorias = TipoProducto.objects.all()  # Obtiene todas las categorías
    productosAll = Producto.objects.all()  # Obtiene todos los productos

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(productosAll, 5)  # Pagina los productos, 5 por página
        productosAll = paginator.page(page)
    except:
        raise Http404  # Si la página no es válida, muestra un error 404

    if request.method == 'POST':
        try:
            cantidad_agregada = int(request.POST.get('cantidad_agregada', 1))
        except ValueError:
            messages.error(request, "Por favor, introduce una cantidad válida.")
            return render(request, 'core/descripcion.html', {
                'Productos': producto,
                'listado': productosAll,
                'paginator': paginator,
                'categorias': categorias,
            })

        if cantidad_agregada < 1:
            messages.error(request, "La cantidad debe ser al menos 1.")
            return render(request, 'core/descripcion.html', {
                'Productos': producto,
                'listado': productosAll,
                'paginator': paginator,
                'categorias': categorias,
            })

        if producto.stock >= cantidad_agregada:
            carrito, created = Carrito.objects.get_or_create(usuario=request.user, producto=producto, defaults={'cantidad_agregada': 0})

            carrito.cantidad_agregada += cantidad_agregada

            carrito.save()

            producto.stock -= cantidad_agregada
            producto.save()

            messages.success(request, "Producto agregado correctamente al carrito")
        else:
            messages.error(request, "No hay suficiente stock disponible")

    return render(request, 'core/descripcion.html', {
        'Productos': producto,
        'listado': productosAll,
        'paginator': paginator,
        'categorias': categorias,
    })



def carrito(request):
    carrito_items = Carrito.objects.filter(usuario=request.user)
    total_precio = 0
    despacho = 1000

    productos_en_carrito = []

    for item in carrito_items:
        subtotal_producto = item.producto.precio * item.cantidad_agregada
        total_precio += subtotal_producto
        
        productos_en_carrito.append({
            'id': item.id,  # Asegúrate de que el id del objeto Carrito se incluye aquí
            'producto': item.producto,
            'cantidad_agregada': item.cantidad_agregada,
            'total_producto': subtotal_producto,
            'valor': item.producto.precio  
        })

    datos = {
        'listarproductos': productos_en_carrito,
        'total_precio': total_precio,
        
    }
    return render(request, 'core/carrito.html', datos)



import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

# views.py

def checkout(request):
    carrito_items = Carrito.objects.filter(usuario=request.user)
    total_precio = sum(item.producto.precio * item.cantidad_agregada for item in carrito_items)
    productos_en_carrito = [{
        'producto': item.producto,
        'cantidad_agregada': item.cantidad_agregada,
        'subtotal_producto': item.producto.precio * item.cantidad_agregada
    } for item in carrito_items]

    costo_envio = 0

    if request.method == 'POST':
        tipo_entrega = request.POST.get('tipo_entrega')
        if tipo_entrega == 'envio':
            costo_envio = 50  # Asigna el costo de envío aquí

        total_final = total_precio + costo_envio

        # Crear una sesión de pago con Stripe
        YOUR_DOMAIN = "http://localhost:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Compra en Ferretería',
                        },
                        'unit_amount': int(total_final * 100),  # Monto en centavos
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )

        return redirect(checkout_session.url, code=303)

    data = {
        'productos_en_carrito': productos_en_carrito,
        'total_precio': total_precio,
        'costo_envio': costo_envio,
        'total_final': total_precio + costo_envio,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, 'core/checkout.html', data)


def success(request):
    session_id = request.GET.get('session_id')
    if session_id is None:
        messages.error(request, "El ID de sesión no se proporcionó.")
        return redirect('checkout')

    session = stripe.checkout.Session.retrieve(session_id)
    amount = session.amount_total / 100  # Convertir de centavos a dólares

    # Guardar los detalles del pago en la base de datos
    payment = Payment.objects.create(
        user=request.user,
        stripe_charge_id=session.payment_intent,
        amount=amount
    )

    # Redirigir a la vista del comprobante
    return redirect('receipt', payment_id=payment.id)

def cancel(request):
    messages.error(request, "El pago ha sido cancelado.")
    return redirect('checkout')

def receipt(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    return render(request, 'core/receipt.html', {'payment': payment})

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



def eliminar_producto(request, id):
    try:
        carro = Carrito.objects.get(id=id)
        producto = carro.producto

        # Sumar la cantidad del carrito al stock del producto
        producto.stock += carro.cantidad_agregada
        producto.save()

        carro.delete()
        messages.success(request, "Producto eliminado del carrito")
    except Carrito.DoesNotExist:
        messages.error(request, "El producto no existe en el carrito")
    return redirect("carrito")



def calcular_total(request):
    tipo_entrega = request.GET.get('tipo_entrega', 'retiro')
    carrito_items = Carrito.objects.filter(usuario=request.user)
    total_precio = sum(item.producto.precio * item.cantidad_agregada for item in carrito_items)
    costo_envio = 50 if tipo_entrega == 'envio' else 0
    total_final = total_precio + costo_envio
    return JsonResponse({'total_final': total_final})



import requests

def generate_password():
    length = '16'
    api_url = 'https://api.api-ninjas.com/v1/passwordgenerator?length={}'.format(length)
    response = requests.get(api_url, headers={'X-Api-Key': 'XMZLg6E/i/Erh5gI9Fwcjg==VenIHyGeJ7AjTfDo'})
    if response.status_code == 200:
        return response.json()['random_password']  # Asegúrate de que 'random_password' sea el campo correcto
    else:
        raise Exception("Error al generar contraseña: {} {}".format(response.status_code, response.text))




def registro(request):
    password = generate_password()  # Generar contraseña automáticamente
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.save(commit=False)
            user.set_password(password)  # Establecer la contraseña generada
            user.save()
            grupo = Group.objects.get(name="cliente")
            user.groups.add(grupo)
            user = authenticate(username=formulario.cleaned_data["username"], password=password)
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            return redirect(to="index")
    else:
        formulario = CustomUserCreationForm(initial={'password1': password, 'password2': password})

    data = {
        'form': formulario,
        'generated_password': password  # Pasar la contraseña generada al contexto
    }
    return render(request, 'registration/registro.html', data)


def update(request, id):
    producto = Producto.objects.get(id=id) # OBTIENE UN PRODUCTO POR EL ID
    data = {
        'form' : ProductoForm(instance=producto) # CARGAMOS EL PRODUCTO EN EL FORMULARIO
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES) # NUEVA INFORMACION
        if formulario.is_valid():
            formulario.save() # INSERT INTO.....
            #data['msj'] = "Producto actualizado correctamente"
            messages.success(request, "Producto modificado correctamente")
            data['form'] = formulario # CARGA LA NUEVA INFOR EN EL FORMULARIO

    return render(request, 'core/update-product.html', data)



def delete(request, id):
    producto = Producto.objects.get(id=id) # OBTIENE UN PRODUCTO POR EL ID
    producto.delete()

    return redirect(to="index")