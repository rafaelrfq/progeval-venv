from django import forms
from django.forms import PasswordInput
from .models import Usuario, User, ROL

class DateInput(forms.DateInput):
    input_type='date'

class UsuarioForm(forms.ModelForm):

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

    # def __init__(self, *args, **kwargs):
    #     super(UsuarioForm, self).__init__(*args, **kwargs)
    #     self.fields['rol'].empty_label = '--Seleccione--'
    #     self.fields['user'].disabled=True
    #     to make a filed not required do this:
    #     self.fields['emp_code'].required = False