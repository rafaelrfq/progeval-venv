from django.db import models
from registrar_usuario.models import Usuario, Persona
import datetime
from django.utils import timezone

ESTADO = [
    ('', '--Seleccione--'),
    ('Programada', 'Programada'),
    ('Cancelada', 'Cancelada'),
    ('Pospuesta', 'Pospuesta'),
]

class Estudiante(Persona):
    matricula = models.CharField(max_length=9, unique=True)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        nomb = self.nombre + ' ' + self.apellido
        return nomb

class Item(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(max_length=1000)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

class Rubrica(models.Model):
    activa = models.BooleanField(default=False)
    fechaCreacion = models.DateField(default=datetime.date.today)
    nombre = models.CharField(max_length=150)
    # grupos = models.ManyToManyField(Grupo)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre + ' - Fecha: {0}'.format(self.fechaCreacion)

class Grupo(models.Model):
    nombre = models.CharField(max_length=75)
    peso = models.PositiveIntegerField()
    items = models.ManyToManyField(Item)
    eliminado = models.BooleanField(default=False)
    rubrica = models.ForeignKey(Rubrica, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre + ' (' + str(self.peso) + ' puntos)'

class Clasificacion(models.Model):
    nombre = models.CharField(max_length=200)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Proyecto(models.Model):
    nombre = models.CharField(max_length=200)
    clasificacion = models.ManyToManyField(Clasificacion)
    equipo = models.ManyToManyField(Estudiante)
    asesor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Estado(models.Model):
    nombre = models.CharField(max_length=35)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Programacion(models.Model):
    fecha = models.DateField(default=datetime.date.today)
    hora = models.TimeField(default=timezone.now)
    estado = models.CharField(max_length=100, choices=ESTADO)
    rubrica = models.ForeignKey(Rubrica, on_delete=models.CASCADE)
    presidenteJurado = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='presidente')
    jurado = models.ManyToManyField(Usuario)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return self.proyecto.nombre + ' - Fecha: {0} Hora: {1}'.format(self.fecha, self.hora)

class Evaluacion(models.Model):
    rubrica = models.ForeignKey(Rubrica, on_delete=models.CASCADE)
    programacion = models.ForeignKey(Programacion, on_delete=models.CASCADE)
    ponderacion = models.PositiveIntegerField()
    observaciones = models.TextField(max_length=1000)
    eliminado = models.BooleanField(default=False)
    juez = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    @classmethod
    def create(cls, rubrica, programacion, ponderacion, observaciones, juez):
        eval = cls(rubrica=rubrica, programacion=programacion, ponderacion=ponderacion, observaciones=observaciones, juez=juez)
        # we could filter data here if necessary
        return eval