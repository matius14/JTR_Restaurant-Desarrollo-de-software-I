from django.db import models
from django.contrib.auth.hashers import make_password, check_password




# Clase que permite crear la tabla de la base de datos para el registro del empleado
class Empleado(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cargoLaboral = models.CharField(max_length=100)
    fechaInicio = models.DateField()
    sueldo = models.IntegerField()
    telefono = models.IntegerField()
    correo = models.EmailField(max_length=50, unique=True)
    direccion = models.CharField(max_length=70)
    contracenia = models.CharField(max_length=255)  
    
    # Metodo que permite encriptar la contraseña 
    def set_contracenia(self, raw_password):
        self.contracenia = make_password(raw_password)
        self.save()
        
    # Metodo para verificar que la contraseña esta encriptada
    def check_contracenia(self, raw_password):
        return check_password(raw_password, self.contracenia)

