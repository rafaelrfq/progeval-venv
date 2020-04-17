from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from .models import Programacion, Estado, Proyecto, Clasificacion, Rubrica, Item, Estudiante, Usuario, Grupo, Carrera
import datetime

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class ProgForm(forms.ModelForm):

    jurado = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={
        'class': 'duallistbox',
        'multiple': 'multiple',
        'size': '8',
        'title': 'dlbox',
        'name': 'items',
    }), queryset=Usuario.objects.filter(eliminado=False).filter(rol=2))

    class Meta:
        model = Programacion
        fields = ('fecha', 'hora', 'estado', 'rubrica', 'presidenteJurado', 'jurado', 'proyecto')
        labels = {
            'fecha': "Fecha",
            'hora': "Hora",
            'estado': "Estado",
            'rubrica': "Rúbrica",
            'jurado': "Jurado",
            'proyecto': "Proyecto",
            'presidenteJurado': "Presidente de Jurado"
        }
        widgets = {
            'fecha': DateInput(),
            'hora': TimeInput()
        }

    def __init__(self, *args, **kwargs):
        super(ProgForm, self).__init__(*args, **kwargs)
        self.fields['rubrica'].empty_label = '--Seleccione--'
        self.fields['proyecto'].empty_label = '--Seleccione--'
        self.fields['presidenteJurado'].empty_label = '--Seleccione--'
        self.fields['presidenteJurado'].help_text = 'Escoger un máximo de 3 jueces incluyendo al presidente. (2 como jurado, 1 como presidente.)'
        self.fields['presidenteJurado'].queryset = Usuario.objects.filter(rol=2)
        # to make a filed not required do this:
        # self.fields['evaluacion'].required = False
        # self.fields['evaluacion'].disabled = True

    def clean(self):
        jurado = self.cleaned_data.get('jurado')
        presi = self.cleaned_data.get('presidenteJurado')
        proye = self.cleaned_data.get('proyecto')
        if len(jurado) > 2:
            raise forms.ValidationError('ERROR: Máximo dos personas por jurado, excluyendo al presidente.')
        if presi == proye.asesor:
            raise forms.ValidationError('ERROR: El asesor del proyecto no puede fungir como jurado.')
        for juez in jurado:
            if juez == proye.asesor:
                raise forms.ValidationError('ERROR: El asesor del proyecto no puede fungir como jurado.')

        return self.cleaned_data

class EstudianteForm(forms.ModelForm):

    class Meta:
        model = Estudiante
        fields = ('nombre', 'apellido', 'matricula', 'email', 'numero_clase', 'ciclo', 'carrera')
        labels = {
            'nombre':'Nombre',
            'apellido':'Apellido',
            'matricula':'Matrícula o ID',
            'email':'Correo Electrónico',
            'numero_clase':'Número de Clase',
            'ciclo':'Ciclo o Período',
            'carrera':'Carrera',
        }

    def __init__(self, *args, **kwargs):
        super(EstudianteForm, self).__init__(*args, **kwargs)
        self.fields['carrera'].empty_label = '--Seleccione--'
        self.fields['carrera'].help_text = 'Si no aparecen opciones en la lista, agregar una carrera.'
        self.fields['email'].help_text = 'El correo debe pertenecer al dominio @ce.pucmm.edu.do'

    def clean(self):
        mail = self.cleaned_data.get('email')
        dominio = mail.split('@')[1]
        dom_aceptado = ['ce.pucmm.edu.do']
        if dominio not in dom_aceptado:
            raise forms.ValidationError('ERROR: El dominio del correo debe ser @ce.pucmm.edu.do')

        return self.cleaned_data

class CarreraForm(forms.ModelForm):

    class Meta:
        model = Carrera
        fields = ('nombre', 'codigo')
        labels = {
            'nombre':'Nombre',
            'codigo':'Código'
        }

class ProyectoForm(forms.ModelForm):

    equipo = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={
        'class': 'duallistbox',
        'multiple': 'multiple',
        'size': '8',
        'title': 'dlbox',
        'name': 'items',
    }), queryset=Estudiante.objects.filter(eliminado=False).exclude(proyecto__equipo__isnull = False))

    class Meta:
        model = Proyecto
        fields = ('nombre', 'clasificacion', 'asesor', 'equipo')
        labels = {
            'nombre':'Nombre',
            'clasificacion':'Clasificación',
            'asesor':'Asesor',
            'equipo': 'Equipo'
        }

    def __init__(self, *args, **kwargs):
        super(ProyectoForm, self).__init__(*args, **kwargs)
        self.fields['asesor'].empty_label = '--Seleccione--'
        self.fields['asesor'].queryset = Usuario.objects.filter(rol=2)
        self.fields['clasificacion'].help_text = 'Puede seleccionar más de una. <br/>Si no aparecen opciones en la lista, agregar una clasificación usando el botón.'
        self.fields['asesor'].help_text = 'Si no aparecen opciones en la lista, agregar un usuario con rol de juez/a.'
        # self.fields['equipo'].help_text = 'Si no aparecen opciones en la lista, agregar nuevos estudiantes.'

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('titulo', 'descripcion')
        labels = {
            'titulo':'Título',
            'descripcion':'Descripción'
        }

class RubricaForm(forms.ModelForm):

    class Meta:
        model = Rubrica
        fields = ('activa', 'fechaCreacion', 'nombre', 'valorIndicador')
        labels = {
            'activa': 'Activa',
            'fechaCreacion': 'Fecha de creación',
            'nombre': 'Nombre',
            'valorIndicador': 'Valor para cada indicador'
        }
        widgets = {
            'fechaCreacion' : DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(RubricaForm, self).__init__(*args, **kwargs)
        self.fields['activa'].help_text = 'Seleccione si desea que esta rúbrica se aplique por defecto a las programaciones futuras.'
        self.fields['valorIndicador'].help_text = 'Este valor se tomará en cuenta a la hora de crear la ficha de evaluación para el jurado.'

    # def clean(self):
    #     _grupo = self.cleaned_data.get('grupos')
    #     if _grupo.peso != 100:
    #         raise ValidationError('La suma de la ponderación de los grupos escogidos debe sumar el 100%')
    #     return self.cleaned_data

class GrupoForm(forms.ModelForm):

    nombre = forms.CharField(max_length=75)
    peso = forms.IntegerField(min_value=0, max_value=100, help_text='La suma de los pesos debe ser 100 puntos.')
    items = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={
        'class': 'duallistbox',
        'multiple': 'multiple',
        'size': '10',
        'title': 'dlbox',
        'name': 'items',
    }), queryset=Item.objects.filter(eliminado=False))
    class Meta:
        model = Grupo
        fields = ('nombre', 'peso', 'items')
        labels = {
            'nombre': 'Nombre',
            'peso': 'Ponderación',
        }

class ClasificacionForm(forms.ModelForm):

    class Meta:
        model = Clasificacion
        fields = ('nombre',)
        labels = {
            'nombre': 'Nombre'
        }

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('nombre', 'apellido', 'email', 'rol', 'user')
        labels = {
            'nombre':"Nombre",
            'apellido':"Apellido",
            'email':"Correo Académico",
            'rol': "Rol",
            'user': "Nombre de Usuario"
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].disabled=True
        self.fields['apellido'].disabled=True
        self.fields['email'].disabled=True
        self.fields['rol'].disabled=True
        self.fields['user'].disabled=True
        self.fields['nombre'].required=False
        self.fields['apellido'].required=False
        self.fields['email'].required=False
        self.fields['rol'].required=False
        self.fields['user'].required=False