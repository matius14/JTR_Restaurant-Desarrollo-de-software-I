
from django import forms
from django.contrib.auth.models import User
from .models import Cliente, Mesa

class ClienteRegistroForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['numeroCedula', 'nombres', 'apellidos', 'telefono', 'direccion']

    password1 = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        # Crear un nuevo usuario
        user = User.objects.create_user(
            username=self.cleaned_data['numeroCedula'],  # O cualquier otro valor único
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['nombres'],
            last_name=self.cleaned_data['apellidos']
        )

        cliente = super().save(commit=False)
        cliente.user = user  # Asignar el usuario al cliente
        if commit:
            cliente.save()
        return cliente


from django import forms
from .models import Cliente



class PerfilForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombres', 'apellidos', 'telefono', 'direccion', 'correo']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
        }


# forms.py
from django import forms
from .models import Reserva
from django.contrib.auth.models import User

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha', 'hora', 'mesa']

    # Para mostrar el nombre del cliente, no es necesario que el cliente lo ingrese en el formulario
    def __init__(self, *args, **kwargs):
        super(ReservaForm, self).__init__(*args, **kwargs)
        self.fields['mesa'].queryset = Mesa.objects.all()  # Aseguramos que las mesas disponibles se carguen dinámicamente

    # Personalización de campos para asegurarse de que tengan el tipo correcto
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    hora = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
