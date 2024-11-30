from django.contrib.auth.models import User
from django.db import models

# implementacion del digrama de clases, el cual va a servir tambien como base de datos usando db.sqlite3


# clase Persona 
class Persona(models.Model):
    numeroCedula = models.IntegerField()
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)


    class Meta:
        abstract = True 


# clase para que los hagan el respectivo registro
class ClienteManager(models.Manager):
    def create_cliente(self, user, numeroCedula, nombres, apellidos, telefono, direccion):
        cliente = self.model(
            user=user,
            numeroCedula=numeroCedula,
            nombres=nombres,
            apellidos=apellidos,
            telefono=telefono,
            direccion=direccion
        )
        cliente.save(using=self._db)
        return cliente

# clase Cliente, la cual hereda de la clase perna y se le pasa como parametro el objeto ClienteManager(), para instanciar el registro
class Cliente(Persona):
    user = models.OneToOneField(User, on_delete=models.CASCADE )
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=70)
    correo = models.EmailField(max_length=255)  # Agregar este campo

    objects = ClienteManager()

    def __str__(self):
        return f'{self.nombres} {self.apellidos} ({self.numeroCedula})'







# clase Empleado la cual tambien hereda de la clase Persona 
class Empleado(Persona):
    cargoLaboral = models.CharField(max_length=100)
    fechaInicio = models.DateField()
    sueldo = models.IntegerField()
    telefono = models.IntegerField()
    correo = models.EmailField(max_length=50, unique=True)
    direccion = models.CharField(max_length=70)



# clase Proveedor, que tambien hereda de la clase Pernona 
class Proveedor(Persona):
    telefono = models.IntegerField()
    correo = models.EmailField(max_length=50)
    direccion = models.CharField(max_length=70)




class Categorias(models.Model):
    nombre = models.CharField(max_length=30)
    
    def __str__(self):
        return self.nombre

# clase Producto, esta tiene una relacion 1 a muchos con proveedor 
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    categorias = models.OneToOneField(Categorias, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)



# Clase Menu
class Menu(models.Model):
    imagen = models.ImageField(upload_to='jtrRestaurant/images/')
    nombre_plato = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.BigIntegerField()

    def __str__(self):
        return self.nombre_plato


# Clase TipoDePago
class TipoDePago(models.Model):
    metodoPado = models.CharField(max_length=20)
   



# Clase Carrito
class Carrito(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    cantidad = models.BigIntegerField(default=1)
    precio = models.BigIntegerField(null=True, blank=True)  # Permite nulos
    tipodePago = models.OneToOneField(TipoDePago, on_delete=models.CASCADE, null=True, blank=True)
    

    def __str__(self):
        return f"Carrito de {self.cliente.username} - {self.menu.nombre_plato}"

    def actualizar_precio(self):
        """Calcula el precio basado en el precio del menú y la cantidad"""
        self.precio = self.cantidad * self.menu.precio
        self.save()





# Clase Venta 
class Venta(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    estado = models.BooleanField(default=False)
    carrito_items = models.ManyToManyField(Carrito)   ### Aqui realice un cambio
    valorTotal = models.BigIntegerField(default=0)

    
    def __str__(self):
        return f"Venta de {self.cliente.username} - {self.fecha}" 



# clase Mesa
class Mesa(models.Model):
    numeroMesa = models.IntegerField()
    capacidad = models.IntegerField()
    ubicacion = models.CharField(max_length=30)
    estado = models.BooleanField(default=False)




# clase Reserva, esta es la clse principal
class Reserva(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)


class PQRS(models.Model): 
    nombre= models.CharField(max_length=30) 
    celular= models.IntegerField() 
    correo= models.EmailField(max_length=50) 
    numero_reserva= models.IntegerField() 
    detalles= models.TextField() 

class Contactanos(models.Model): 
    nombre= models.CharField(max_length=30)
    celular= models.IntegerField()
    correo= models.EmailField(max_length=50) 
    asunto= models.TextField() 
