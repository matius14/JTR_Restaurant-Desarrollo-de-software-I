from django import forms
from .models import Empleado

# Formulario que captura los datos para el login en el sistema 
class LoginForm(forms.Form):
    correo = forms.EmailField()
    contracenia = forms.CharField(widget=forms.PasswordInput())









