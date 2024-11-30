from django.urls import path
from . import views

# url a las que tiene permitido ingresar el empleado
urlpatterns = [
    path('loginEmpleado.html', views.login_view, name='empleados_login'),
    path('home/', views.home, name='dashboard'), 
    
]


