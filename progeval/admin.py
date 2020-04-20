from django.contrib import admin
from .models import Estudiante, Item, Rubrica, Proyecto, Evaluacion, Programacion, Estado, Grupo, IndicadorEvaluado

# Register your models here.

admin.site.register(Estudiante)
admin.site.register(Item)
admin.site.register(Rubrica)
admin.site.register(Proyecto)
admin.site.register(Evaluacion)
admin.site.register(Programacion)
admin.site.register(Estado)
admin.site.register(Grupo)
admin.site.register(IndicadorEvaluado)