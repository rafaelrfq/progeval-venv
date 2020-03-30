from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from .models import Programacion, Estado, Evaluacion, Proyecto, Clasificacion, Rubrica, Item, Estudiante, Usuario


class DateInput(forms.DateInput):
    input_type = 'date'

class ProgForm(forms.ModelForm):

    class Meta:
        model = Programacion
        fields = ('fecha','estado','rubrica', 'presidenteJurado', 'jurado', 'proyecto')
        labels = {
            'fecha': "Fecha y Hora",
            'estado': "Estado",
            'rubrica': "Rúbrica",
            'jurado': "Jurado",
            'proyecto': "Proyecto",
            'presidenteJurado': "Presidente de Jurado"
        }

    def __init__(self, *args, **kwargs):
        super(ProgForm, self).__init__(*args, **kwargs)
        self.fields['rubrica'].empty_label = '--Seleccione--'
        self.fields['proyecto'].empty_label = '--Seleccione--'
        self.fields['presidenteJurado'].empty_label = '--Seleccione--'
        self.fields['jurado'].queryset = Usuario.objects.filter(rol=2)
        self.fields['presidenteJurado'].queryset = Usuario.objects.filter(rol=2)
        # to make a filed not required do this:
        # self.fields['evaluacion'].required = False
        # self.fields['evaluacion'].disabled = True

    def clean(self):
        jurado = self.cleaned_data.get('jurado')
        if len(jurado) > 2:
            raise forms.ValidationError('Máximo dos personas por jurado, excluyendo al presidente.')

        return self.cleaned_data

    # def clean_regions(self):
    #     regions = self.cleaned_data['regions']
    #     if len(regions) > 3:
    #         raise forms.ValidationError('You can add maximum 3 regions')
    #     return regions

class EstudianteForm(forms.ModelForm):

    class Meta:
        model = Estudiante
        fields = ('nombre', 'apellido', 'fechaNacimiento', 'matricula')
        labels = {
            'nombre':'Nombre',
            'apellido':'Apellido',
            'fechaNacimiento':'Fecha de Nacimiento',
            'matricula':'Matrícula'
        }
        widgets = {
            'fechaNacimiento': DateInput()
        }

class ProyectoForm(forms.ModelForm):

    class Meta:
        model = Proyecto
        fields = ('nombre', 'clasificacion', 'equipo', 'asesor')
        labels = {
            'nombre':'Nombre',
            'clasificacion':'Clasificación',
            'equipo':'Equipo',
            'asesor':'Asesor'
        }

    def __init__(self, *args, **kwargs):
        super(ProyectoForm, self).__init__(*args, **kwargs)
        self.fields['asesor'].empty_label = '--Seleccione--'
        self.fields['asesor'].queryset = Usuario.objects.filter(rol=2)
        self.fields['clasificacion'].help_text = 'Puede seleccionar más de una. <br/>Si no aparecen opciones en la lista, agregar una clasificación usando el botón.'
        self.fields['asesor'].help_text = 'Si no aparecen opciones en la lista, agregar un usuario con rol de juez/a.'
        self.fields['equipo'].help_text = 'Si no aparecen opciones en la lista, agregar nuevos estudiantes.'

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
        fields = ('activa', 'fechaCreacion', 'nombre')
        labels = {
            'activa': 'Activa',
            'fechaCreacion': 'Fecha de creación',
            'nombre': 'Nombre'
        }
        widgets = {
            'fechaCreacion' : DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(RubricaForm, self).__init__(*args, **kwargs)
        self.fields['activa'].help_text = 'Seleccione si desea que esta rúbrica se aplique por defecto a las programaciones futuras.'

    # def clean(self):
    #     _grupo = self.cleaned_data.get('grupos')
    #     if _grupo.peso != 100:
    #         raise ValidationError('La suma de la ponderación de los grupos escogidos debe sumar el 100%')
    #     return self.cleaned_data

class ClasificacionForm(forms.ModelForm):

    class Meta:
        model = Clasificacion
        fields = ('nombre',)
        labels = {
            'nombre': 'Nombre'
        }

class EvaluacionForm(forms.ModelForm):

    class Meta:
        model = Evaluacion
        fields = ('rubrica', 'programacion', 'ponderacion', 'observaciones')
        labels = {
            'rubrica': 'Rúbrica',
            'programacion': 'Programación',
            'ponderacion': 'Ponderación',
            'observaciones': 'Observaciones'
        }

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('nombre', 'apellido', 'fechaNacimiento', 'rol', 'user')
        labels = {
            'nombre':"Nombre",
            'apellido':"Apellido",
            'fechaNacimiento':"Fecha de Nacimiento",
            'rol': "Rol",
            'user': "Nombre de Usuario"
        }
        widgets = {
            'fechaNacimiento': DateInput()
            # 'password': PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].disabled=True
        self.fields['apellido'].disabled=True
        self.fields['fechaNacimiento'].disabled=True
        self.fields['rol'].disabled=True
        self.fields['user'].disabled=True
        self.fields['nombre'].required=False
        self.fields['apellido'].required=False
        self.fields['fechaNacimiento'].required=False
        self.fields['rol'].required=False
        self.fields['user'].required=False