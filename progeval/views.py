from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms import inlineformset_factory
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ProgForm, EstudianteForm, ProyectoForm, ItemForm, RubricaForm, ClasificacionForm, ProfileForm
from .models import Programacion, Estado, Evaluacion, Proyecto, Clasificacion, Rubrica, Grupo, Item, Estudiante
from registrar_usuario.models import Usuario
from datetime import datetime

# Views a los que puede accesar el/la coodinador/a

@login_required(login_url='/')
def coord_home(request):
    proyectos = Proyecto.objects.all()
    rubricas = Rubrica.objects.all()
    items = Item.objects.all()
    estudiantes = Estudiante.objects.all()
    programaciones = Programacion.objects.all()
    clasificaciones = Clasificacion.objects.all()
    usuarios = Usuario.objects.all()

    p = proyectos.count()
    r = rubricas.count()
    i = items.count()
    e = estudiantes.count()
    pr = programaciones.count()
    c = clasificaciones.count()
    u = usuarios.count()

    context = {'p': p, 'r': r, 'i': i, 'e': e, 'pr': pr, 'c': c, 'u': u}
    return render(request, 'prog_home.html', context)

def programacion(request, id=0):
    rub = Rubrica.objects.get(activa=True)
    # estado = Estado.objects.get(nombre='Programada')
    if request.method == "GET":
        if id==0:
            form = ProgForm(initial={'rubrica': rub.id, 'estado': 'Programada', 'fecha': datetime.now()})
        else:
            programacion = Programacion.objects.get(pk=id)
            form = ProgForm(instance=programacion)
        return render(request, "programacion.html", {'form':form})
    elif request.method == "POST":
        if id==0:
            form = ProgForm(request.POST)
        else:
            programacion = Programacion.objects.get(pk=id)
            form = ProgForm(request.POST, instance=programacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Programación insertada.')
            return redirect('/coord/programacion/listar')
    else:
        form = ProgForm(initial={'rubrica': rub.id, 'estado': 'Programada', 'fecha': datetime.now()})
    return render(request, 'programacion.html', {'form': form})

def delete_prog(request, id):
    prog = Programacion.objects.get(pk=id)
    prog.eliminado = True
    prog.save()
    return redirect('/coord/programacion/listar')

def listar_prog(request):
    context = {'listar_prog':Programacion.objects.all()}
    return render(request, "listar_prog.html", context)

def insertar_estudiante(request, id=0):
    if request.method == "GET":
        if id==0:
            form = EstudianteForm()
        else:
            estud = Estudiante.objects.get(pk=id)
            form = EstudianteForm(instance=estud)
        return render(request, "insertar_estudiante.html", {'form':form})
    else:
        if id==0:
            form = EstudianteForm(request.POST)
        else:
            estud = Estudiante.objects.get(pk=id)
            form = EstudianteForm(request.POST, instance=estud)
        if form.is_valid():
            form.save()
        nomb = form.cleaned_data.get('nombre')
        messages.success(request, 'Estudiante ' + nomb + ' insertado.')
        return redirect('/coord/estudiante/listar')

def delete_estudiante(request, id):
    estud = Estudiante.objects.get(pk=id)
    estud.eliminado = True
    estud.save()
    return redirect('/coord/estudiante/listar')

def listar_estudiante(request):
    context = {'listar_estudiante': Estudiante.objects.all()}
    return render(request, "listar_estudiante.html", context)

def insertar_proyecto(request, id=0):
    if request.method == "GET":
        if id==0:
            form = ProyectoForm()
        else:
            proyect = Proyecto.objects.get(pk=id)
            form = ProyectoForm(instance=proyect)
        return render(request, "insertar_proyecto.html", {'form':form})
    else:
        if id==0:
            form = ProyectoForm(request.POST)
        else:
            proyect = Proyecto.objects.get(pk=id)
            form = ProyectoForm(request.POST, instance=proyect)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proyecto insertado.')
            return redirect('/coord/proyecto/listar')
    return render(request, "insertar_proyecto.html", {'form':form})

def delete_proyecto(request, id):
    proj = Proyecto.objects.get(pk=id)
    proj.eliminado = True
    proj.save()
    return redirect('/coord/proyecto/listar')

def listar_proyecto(request):
    context = {'listar_proyecto': Proyecto.objects.all()}
    return render(request, "listar_proyecto.html", context)        

def insertar_item(request, id=0):
    if request.method == "GET":
        if id==0:
            form = ItemForm()
        else:
            item = Item.objects.get(pk=id)
            form = ItemForm(instance=item)
        return render(request, "insertar_item.html", {'form':form})
    else:
        if id==0:
            form = ItemForm(request.POST)
        else:
            item = Item.objects.get(pk=id)
            form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
        messages.success(request, 'Ítem insertado.')
        return redirect('/coord/rubrica/item/listar')    

def delete_item(request, id):
    item = Item.objects.get(pk=id)
    item.eliminado = True
    item.save()
    return redirect('/coord/rubrica/item/listar')

def listar_item(request):
    context = {'listar_item': Item.objects.all()}
    return render(request, "listar_item.html", context)

def insertar_rubrica(request, id=0):
    GrupoFormSet = inlineformset_factory(Rubrica, Grupo, fields=('nombre', 'peso', 'items'), extra=3, can_delete=False, max_num=5)
    if request.method == "GET":
        if id==0:
            form = RubricaForm()
            form1 = GrupoFormSet()
        else:
            rub = Rubrica.objects.get(pk=id)
            form = RubricaForm(instance=rub)
            form1 = GrupoFormSet(instance=rub)
    else:
        if id==0:
            form = RubricaForm(request.POST)
            if form.is_valid():
                form.save()
                rub = Rubrica.objects.latest('id')
                if rub.activa == True:
                    Rubrica.objects.exclude(id=rub.id).update(activa=False)
                
                form1 = GrupoFormSet(request.POST, instance=rub)
            
                if form1.is_valid():
                    suma = 0
                    formas = form1.save(commit=False)
                    for grupos in formas:
                        suma += grupos.peso
                    if suma == 100:
                        form1.save()
                        
                        messages.success(request, 'Rúbrica insertada.')
                        return redirect('/coord/rubrica/listar') 
                    else:
                        rub.delete()
                        messages.error(request, 'Los grupos deben sumar 100 en su peso/ponderación.')

            else:
                return redirect('/coord/rubrica')

        else:
            rub = Rubrica.objects.get(pk=id)
            form = RubricaForm(request.POST, instance=rub)
            form1 = GrupoFormSet(request.POST, instance=rub)
            if form1.is_valid():
                form.save()
                form1.save()
                messages.success(request, 'Rúbrica actualizada.')
                return redirect('/coord/rubrica/listar') 
            else: 
                return redirect('/coord/rubrica')
        
        form = RubricaForm()
        form1 = GrupoFormSet()
    return render(request, "insertar_rubrica.html", {'form':form, 'form1': form1})

def delete_rub(request, id):
    rub = Rubrica.objects.get(pk=id)
    rub.eliminado = True
    rub.save()
    return redirect('/coord/rubrica/listar')

def listar_rubrica(request):
    context = {'listar_rubrica': Rubrica.objects.all(), 'grupos': Grupo.objects.all()}
    return render(request, "listar_rubrica.html", context)

def insertar_clasificacion(request, id=0):
    if request.method == "GET":
        if id==0:
            form = ClasificacionForm()
        else:
            clasif = Clasificacion.objects.get(pk=id)
            form = ClasificacionForm(instance=clasif)
        return render(request, "insertar_clasif.html", {'form':form})
    else:
        if id==0:
            form = ClasificacionForm(request.POST)
        else:
            clasif = Clasificacion.objects.get(pk=id)
            form = ClasificacionForm(request.POST, instance=clasif)
        if form.is_valid():
            form.save()
        messages.success(request, 'Clasificación insertada.')
        return redirect('/coord/proyecto/clasificacion/listar')    

def delete_clasif(request, id):
    clasif = Clasificacion.objects.get(pk=id)
    clasif.eliminado = True
    clasif.save()
    return redirect('/coord/proyecto/clasificacion/listar')

def listar_clasificacion(request):
    context = {'listar_clasificacion': Clasificacion.objects.all()}
    return render(request, "listar_clasif.html", context)

def profile(request):
    usr = request.user
    queryset = Usuario.objects.filter(user=usr.id)
    for item in queryset:
        usuario = item
    form = ProfileForm(instance=usuario)
    if usuario.rol == 1:
        page = "profile_coord.html"
    else:
        page = "profile_jurado.html"
    return render(request, page, {'form': form})

#PDF rendering

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

# Views a los que tendrá acceso el jurado

def jurado_home(request):
    usuario = Usuario.objects.get(user=request.user.id)
    prog = Programacion.objects.filter(Q(presidenteJurado=usuario.id) | Q(jurado=usuario.id)).distinct()
    evaluaciones = Evaluacion.objects.all()
    e = evaluaciones.count()
    p = prog.count()
    return render(request, "jurado_home.html", {'prog': p, 'eval': e})

def evaluaciones_disp(request):
    user = request.user
    queryset = Usuario.objects.filter(user=user.id)
    for item in queryset:
        usuario = item
    prog = Programacion.objects.filter(Q(presidenteJurado=usuario.id) | Q(jurado=usuario.id)).distinct()
    return render(request, "eval_disp.html", {'listar_prog': prog})

def evaluacion(request, id):
    prog = Programacion.objects.get(pk=id)
    rub = prog.rubrica
    grupos = Grupo.objects.filter(rubrica=rub.id)
    context = {'evaluacion': grupos}
    if request.method == "POST":
        evaluacion = request.POST
        ponderacion = 0
        observ = evaluacion.get('observaciones')
        for key in evaluacion:
            if 'rad' in key:
                ponderacion += int(evaluacion[key])
        e = Evaluacion.create(rub, prog, ponderacion, observ)
        e.save()
    
    return render(request, 'evaluacion.html', context)

def listar_evaluacion(request):
    evaluaciones = Evaluacion.objects.all()
    context = {'listar_eval': evaluaciones}
    return render(request, "listar_eval.html", context)

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        evaluaciones = Evaluacion.objects.all()
        context = {'listar_eval': evaluaciones}
        pdf = render_to_pdf('pdf_template.html', context)
        return HttpResponse(pdf, content_type='application/pdf')