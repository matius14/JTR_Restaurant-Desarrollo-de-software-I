"""
URL configuration for JTR_RESTAURANT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('reservas/', reservas, name="reserva"),
    path('registro/', registroCliente, name="registro"),
    path('login/', login_cliente, name="login"),
    path('logout/', logout_cliente, name="logout"),
    path('menu/', menuDisponible, name="menu"),
    path('carrito/', carritoDeCompras, name="carrito"),
    path('realizar_venta/', realizar_venta, name='realizar_venta'),
    path('venta/', ventaGenerada, name="venta"),
    path('perfil/', editar_perfil, name='perfil'),  # Esta es la ruta para editar perfil
    path('reserva/', realizar_reserva, name='reserva'),  # Esta es para la reserva
    path('actualizar_cantidad/', actualizar_cantidad, name='actualizar_cantidad'),
    path('reserva/exito/', reserva_exito, name='reserva_exito'),
    path('factura/<int:venta_id>/', generar_factura, name='generar_factura'),
    path('ventas/<int:venta_id>/factura/', generar_factura, name='generar_factura'),
    path('ventas/', listar_ventas, name='listar_ventas'),
    path('reserva/', reserva_view, name='reserva_view'),  
    path('soporte_cliente/', soporte_cliente, name='soporte_cliente'),
    path('quienes-somos/', quienes_somos, name='quienes_somos'),
    path('pqrs/', pqrs_view, name='pqrs'),
    path('contactanos/', contactanos_view, name='contactanos'),
    path('terminos/', terminos_view, name='terminos'),
    path('privacidad/', privacidad_view, name='privacidad'),
    path('ayuda/', ayuda_view, name='ayuda'),
    path('producto/<int:menu_id>/', detalle_producto, name='detalle_producto'),
]
