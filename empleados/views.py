from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from .models import Empleado
from reserva.models import Menu





# Funcion que permite hacer login a el Empleado 
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contracenia = form.cleaned_data['contracenia']
            
            try:
                empleado = Empleado.objects.get(correo=correo)
                if empleado.check_contracenia(contracenia):
                    # obtenemos el ID de empleado para quepueda iniciar sesion
                    request.session['user_id'] = empleado.id
                    return redirect('dashboard')  
                else:
                    messages.error(request, 'Contraseña incorrecta')
            except Empleado.DoesNotExist:
                messages.error(request, 'Correo no registrado, verifique nuevamente')
    else:
        form = LoginForm()

    return render(request, 'loginEmpleado.html', {'form': form})



# Funcion que permite a el empleado salir del sistema 
def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('empleados_login')






def home(request):
    user_id = request.session.get('user_id')  # Obtén el ID del usuario desde la sesión
    if not user_id:
        return redirect('empleados_login')  # Redirige al login si no está autenticado

    empleado = Empleado.objects.get(id=user_id)  # Obtén los datos del empleado
    menu = Menu.objects.all()
    return render(request, 'home.html', {'menu': menu, 'user': empleado})
