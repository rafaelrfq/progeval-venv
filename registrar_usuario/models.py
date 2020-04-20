from django.db import models
from django.contrib.auth.models import User

# Create your models here.

ROL = [
    ('', '--Seleccione--'),
    (1, 'Coordinador/a'),
    (2, 'Jurado e Invitado'),
]

class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)

    class Meta:
        abstract = True

# class Rol(models.Model):
#     nombre = models.CharField(max_length=50)
#     eliminado = models.BooleanField(default=False)

#     def __str__(self):
#         return self.nombre

class Usuario(Persona):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.IntegerField(choices=ROL)
    email = models.EmailField(unique=True)
    dept = models.CharField(max_length=100)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        nomb = self.nombre + ' ' + self.apellido
        return nomb

    @classmethod
    def create(cls, nombre, apellido, email, rol, dept, user):
        usuario = cls(nombre=nombre, apellido=apellido, email=email, rol=rol, dept=dept, user=user)
        # we could filter data here if necessary
        return usuario