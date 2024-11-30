from django.contrib import admin
from .models import *

from django.contrib import admin
from .models import Empleado

# clase que permite al adminiostrador poder registrar empleados 
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('correo', 'nombres', 'apellidos', 'cargoLaboral', 'telefono', 'sueldo')

    def save_model(self, request, obj, form, change):
        if not change: 
            obj.set_contracenia(obj.contracenia)  
        obj.save()

# registro del modelo empleado
admin.site.register(Empleado, EmpleadoAdmin)


