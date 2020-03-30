from django.db import models
from django.contrib.auth.models import User

# Create your models here.

ROL = [
    ('', '--Seleccione--'),
    (1, 'Coordinador/a'),
    (2, 'Juez/a'),
]

class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fechaNacimiento = models.DateField()

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
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        nomb = self.nombre + ' ' + self.apellido
        return nomb