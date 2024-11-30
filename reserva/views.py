from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import ClienteRegistroForm
from django.contrib import messages
from django.utils import timezone

from .models import *





def registroCliente(request):
    if request.method == 'POST':
        form = ClienteRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = ClienteRegistroForm()
    return render(request, 'registro.html', {'form': form})








def login_cliente(request):
    if request.method == 'POST':
        username = request.POST.get('username')  
        password = request.POST.get('password')  
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  
            return redirect('menu')  
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')  

    return render(request, 'login.html')


# Esta vista es la que permite que el cliente autenticado pueda salir del sistema cuando ha inido sesión
def logout_cliente(request):
    logout(request)
    return redirect('index')




# esta es la vista de inico que vera el cliente un vez inicie sesión
def index(request):
    return render(request, "index.html")


@login_required
def menuDisponible(request):
    menu = Menu.objects.all()
    carrito_items = Carrito.objects.filter(cliente=request.user)
    total = sum(item.precio for item in carrito_items)

    # Obtener todos los tipos de pago disponibles
    tipos_de_pago = TipoDePago.objects.all()

    return render(request, 'menu.html', {
        'menu': menu,
        'carrito_items': carrito_items,
        'total': total,
        'tipos_de_pago': tipos_de_pago  # Pasar los tipos de pago al contexto
    })

@login_required
def actualizar_cantidad(request):
    if request.method == 'POST':
        menu_id = request.POST.get('menu_id')
        menu_item = get_object_or_404(Menu, id=menu_id)

        # Buscar el artículo en el carrito o crearlo si no existe
        carrito_item, created = Carrito.objects.get_or_create(
            cliente=request.user,
            menu=menu_item,
            defaults={'precio': menu_item.precio}  # Asignar precio inicial
        )
        
        if not created:  # Solo incrementar si no es un nuevo objeto
            carrito_item.cantidad += 1
        
        # Actualizar el precio automáticamente
        carrito_item.actualizar_precio()
        
        return redirect('menu')

    return redirect('menu')


from django.shortcuts import redirect
from django.contrib import messages

from .models import TipoDePago

@login_required
def carritoDeCompras(request):
    if request.method == 'POST':
        menu_id = request.POST.get('menu_id')
        cantidad = int(request.POST.get('cantidad', 1))
        menu = get_object_or_404(Menu, id=menu_id)

        # Intentamos obtener el carrito_item, si no existe, lo creamos.
        carrito_item, created = Carrito.objects.get_or_create(
            cliente=request.user,
            menu=menu,
            defaults={'cantidad': cantidad, 'precio': menu.precio * cantidad}
        )

        # Si el item ya existía, actualizamos la cantidad y el precio
        if not created:
            carrito_item.cantidad += cantidad
            carrito_item.actualizar_precio()  # Usamos el método para actualizar el precio
            carrito_item.save()

        messages.success(request, "Agregado al carrito con éxito")
        return redirect('menu') 


    elif request.method == 'GET':
        carrito_items = Carrito.objects.filter(cliente=request.user)
        total = sum(item.precio for item in carrito_items)

        # Obtener todos los tipos de pago disponibles
        tipos_de_pago = TipoDePago.objects.all()

        # Verificar si tipos_de_pago tiene registros
        print(tipos_de_pago)  # Esto debería imprimir los tipos de pago si hay registros

        return render(request, 'carrito.html', {
            'carrito_items': carrito_items,
            'total': total,
            'tipos_de_pago': tipos_de_pago  # Pasa los tipos de pago al contexto
        })

    return JsonResponse({'error': 'Método no permitido'}, status=405)




# @login_required
# def realizar_venta(request):
#     if request.method == 'POST':
        
#         carrito = Carrito.objects.filter(cliente=request.user).first()

#         if not carrito:
#             return JsonResponse({'error': 'No hay carrito disponible'}, status=400)

        
#         total = carrito.precio * carrito.cantidad

       
#         venta = Venta.objects.create(
#             cliente=request.user,
#             carrito_items=carrito,  
#             valorTotal=total,
#         )

       
#         carrito.delete()

#         return JsonResponse({'mensaje': 'Venta realizada con éxito', 'venta_id': venta.id})
    
#     return JsonResponse({'error': 'Método no permitido'}, status=405)


@login_required
def realizar_venta(request):
    if request.method == 'POST':
        # Obtener todos los ítems del carrito del usuario
        carrito_items = Carrito.objects.filter(cliente=request.user)
        # Verificar los precios antes de asignar
        for item in carrito_items:
            print(f"Producto: {item.menu.nombre_plato}, Precio: {item.precio}, Cantidad: {item.cantidad}")
        if not carrito_items.exists():
            return JsonResponse({'error': 'No hay ítems en el carrito'}, status=400)

        # Calcular el total
        total = sum(item.precio for item in carrito_items)

        # Crear la venta
        venta = Venta.objects.create(
            cliente=request.user,
            valorTotal=total,
        )

        # Asignar los ítems del carrito a la venta
        venta.carrito_items.set(carrito_items)

        # Vaciar el carrito
        carrito_items.delete()

        # Retornar el contexto para la plantilla
        return render(request, 'venta.html', {'mensaje': 'Venta realizada con éxito', 'venta_id': venta.id})

    return JsonResponse({'error': 'Método no permitido'}, status=405)






def ventaGenerada(request):
    ventas = Venta.objects.all()
    ventas = Venta.objects.filter(cliente=request.user).order_by('-fecha', '-hora')  
    return render(request, 'venta.html', {'ventas': ventas})



@login_required
def reservas(request):
    reservaTotal = Reserva.objects.all()
    return render(request, 'reserva.html', {'reservaTotal': reservaTotal})




from django.shortcuts import render, redirect
from .forms import PerfilForm

def editar_perfil(request):
    cliente = request.user.cliente  

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=cliente)  
        if form.is_valid():
            form.save()
            return redirect('perfil')  
    else:
        form = PerfilForm(instance=cliente)  

    return render(request, 'profile.html', {'form': form})



# views.py
from .forms import ReservaForm



@login_required
def realizar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            
            # Obtener el cliente asociado al usuario autenticado
            cliente = Cliente.objects.get(user=request.user)
            reserva.cliente = cliente  # Asignar el cliente a la reserva
            
            reserva.save()  # Guardar la reserva
            return redirect('reserva_exito')  # Redirigir a una página de éxito (puedes personalizarla)
    else:
        form = ReservaForm()

    return render(request, 'reserva.html', {'form': form})

def reserva_exito(request):
    return render(request, 'reserva_exito.html')




from django.shortcuts import render
from .models import Venta

@login_required
def listar_ventas(request):
    # Obtener todas las ventas del cliente actual
    ventas = Venta.objects.filter(cliente=request.user)
    return render(request, 'venta.html', {'venta': ventas})



from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.contrib.sites.shortcuts import get_current_site
from django.templatetags.static import static
from urllib.parse import urljoin


@login_required
def generar_factura(request, venta_id):
    # Obtener la venta y sus detalles
    venta = get_object_or_404(Venta, id=venta_id, cliente=request.user)
    carrito_items = []

    # Calcular subtotal para cada item
    for item in venta.carrito_items.all():
        carrito_items.append({
            "nombre_plato": item.menu.nombre_plato,
            "cantidad": item.cantidad,
            "precio_unitario": item.menu.precio,
            "subtotal": item.cantidad * item.menu.precio
        })

    # Obtener la ruta absoluta de la imagen
    logo_path = static('img/JTR-cop.png')
    current_site = get_current_site(request)
    logo_url = urljoin(f"http://{current_site.domain}", logo_path)

    # Renderizar la plantilla HTML
    html = render_to_string('factura.html', {
        'venta': venta,
        'carrito_items': carrito_items,
        'cliente': request.user,
        'logo_url': logo_url
    })

    # Generar el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Factura_{venta.id}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar la factura.', status=500)

    return response


@login_required
def procesar_compra(request):
    if request.method == 'POST':
        carrito_items = Carrito.objects.filter(cliente=request.user)
        if not carrito_items:
            messages.error(request, "El carrito está vacío.")
            return redirect('menu')
        
        # Crear la venta
        nueva_venta = Venta.objects.create(cliente=request.user, estado=True)
        total = 0
        
        for item in carrito_items:
            nueva_venta.carrito_items.add(item)
            total += item.precio
        
        nueva_venta.valorTotal = total
        nueva_venta.save()
        
        # Vaciar el carrito
        carrito_items.delete()

        messages.success(request, "Compra realizada con éxito. Descarga tu factura.")
        return redirect('menu')  # O a una página con enlace al PDF
    
    return redirect('menu')


# En tu archivo views.py
from .forms import ReservaForm

def reserva_view(request):
    form = ReservaForm(request.POST or None)
    
    form.fields['fecha'].widget.attrs.update({'class': 'form-control'})
    form.fields['hora'].widget.attrs.update({'class': 'form-control'})
    form.fields['mesa'].widget.attrs.update({'class': 'form-control'})
    
    return render(request, 'reserva.html', {'form': form})
# views.py


def soporte_cliente(request):
    return render(request, 'soporte_cliente.html')


def quienes_somos(request):
    return render(request, 'quienes_somos.html')


from .models import PQRS

def pqrs_view(request):
    if request.method == "POST":
        # Obtener los datos del formulario
        nombre = request.POST.get('nombre')
        celular = request.POST.get('celular')
        correo = request.POST.get('correo')
        numero_reserva = request.POST.get('numero_reserva')
        detalles = request.POST.get('detalles')

        # Guardar los datos en el modelo PQRS
        PQRS.objects.create(
            nombre=nombre,
            celular=celular,
            correo=correo,
            numero_reserva=numero_reserva,
            detalles=detalles
        )

    return render(request, 'pqrs.html')



from .models import Contactanos

def contactanos_view(request):
    mensaje_enviado = False  # Inicializamos el indicador en False

    if request.method == "POST":
        # Capturar datos del formulario
        nombre = request.POST.get('nombre')
        celular = request.POST.get('celular')
        correo = request.POST.get('correo')
        asunto = request.POST.get('asunto')

        # Guardar en la base de datos
        Contactanos.objects.create(
            nombre=nombre,
            celular=celular,
            correo=correo,
            asunto=asunto
        )

        # Cambiar el indicador a True cuando se guarde el mensaje
        mensaje_enviado = True

    return render(request, 'contactanos.html', {'mensaje_enviado': mensaje_enviado})


from django.shortcuts import render

def terminos_view(request):
    return render(request, 'terminos.html')


def privacidad_view(request):
    return render(request, 'privacidad.html')



def terminos_view(request):
    return render(request, 'terminos.html')

from django.shortcuts import render

def ayuda_view(request):
    return render(request, 'ayuda.html')





import random

def detalle_producto(request, menu_id):
    producto = get_object_or_404(Menu, id=menu_id)

    productos_relacionados = Menu.objects.exclude(id=producto.id)
    productos_relacionados = random.sample(list(productos_relacionados), min(len(productos_relacionados), 6))

    return render(request, 'detalle_producto.html', {
        'producto': producto,
        'productos_relacionados': productos_relacionados
    })
