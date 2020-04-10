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
from django.core.exceptions import ObjectDoesNotExist
from .forms import ProgForm, EstudianteForm, ProyectoForm, ItemForm, RubricaForm, ClasificacionForm, ProfileForm, GrupoForm
from .models import Programacion, Estado, Evaluacion, Proyecto, Clasificacion, Rubrica, Grupo, Item, Estudiante
from registrar_usuario.views import userRole
from registrar_usuario.models import Usuario
from datetime import datetime

# Views a los que puede accesar el/la coodinador/a

@login_required(login_url='/')
def coord_home(request):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        proyectos = Proyecto.objects.all()
        rubricas = Rubrica.objects.all()
        items = Item.objects.all()
        estudiantes = Estudiante.objects.all()
        programaciones = Programacion.objects.all()
        clasificaciones = Clasificacion.objects.all()
        usuarios = Usuario.objects.all()
        evaluaciones = Evaluacion.objects.all()

        p = proyectos.count()
        r = rubricas.count()
        i = items.count()
        e = estudiantes.count()
        pr = programaciones.count()
        c = clasificaciones.count()
        u = usuarios.count()
        ev = evaluaciones.count()
        titulo = 'Dashboard'

        context = {'titulo': titulo, 'p': p, 'r': r, 'i': i, 'e': e, 'pr': pr, 'c': c, 'u': u, 'ev': ev}
        return render(request, 'prog_home.html', context)

@login_required(login_url='/')
def programacion(request, id=0):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        try:
            rub = Rubrica.objects.get(activa=True)
        except ObjectDoesNotExist:
            rub = None
        if request.method == "GET":
            if id==0 and rub != None:
                form = ProgForm(initial={'rubrica': rub.id, 'estado': 'Programada'})
                titulo = 'Programación de presentación de proyectos'
            elif id==0 and rub == None:
                form = ProgForm()
                titulo = 'Programación de presentación de proyectos'
            else:
                programacion = Programacion.objects.get(pk=id)
                form = ProgForm(instance=programacion)
                titulo = 'Editar Programación existente'
            return render(request, "programacion.html", {'form':form, 'titulo': titulo})
        elif request.method == "POST":
            if id==0:
                form = ProgForm(request.POST)
            else:
                programacion = Programacion.objects.get(pk=id)
                form = ProgForm(request.POST, instance=programacion)
            if form.is_valid():
                form.save()
                messages.success(request, 'Programación insertada.')
                return redirect('/coord/programacion')
        else:
            form = ProgForm(initial={'rubrica': rub.id, 'estado': 'Programada'})
        return render(request, 'programacion.html', {'form': form, 'titulo': titulo})

@login_required(login_url='/')
def delete_prog(request, id):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        prog = Programacion.objects.get(pk=id)
        prog.eliminado = True
        prog.save()
        return redirect('/coord/programacion/listar')

@login_required(login_url='/')
def listar_prog(request):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        titulo = 'Listado de programaciones'
        context = {'listar_prog':Programacion.objects.all(), 'titulo': titulo}
        return render(request, "listar_prog.html", context)

@login_required(login_url='/')
def listar_eval_coord(request):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        evaluaciones = Evaluacion.objects.all()
        titulo = 'Evaluaciones realizadas'
        context = {'listar_eval': evaluaciones, 'titulo': titulo}
        return render(request, "listar_eval_coord.html", context)

@login_required(login_url='/')
def insertar_estudiante(request, id=0):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        if request.method == "GET":
            if id==0:
                form = EstudianteForm()
                titulo = 'Insetar nuevo estudiante'
            else:
                estud = Estudiante.objects.get(pk=id)
                form = EstudianteForm(instance=estud)
                titulo = 'Editar estudiante existente'
            return render(request, "insertar_estudiante.html", {'form':form, 'titulo': titulo})
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
            return redirect('/coord/estudiante')

@login_required(login_url='/')
def delete_estudiante(request, id):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        estud = Estudiante.objects.get(pk=id)
        estud.eliminado = True
        estud.save()
        return redirect('/coord/estudiante/listar')

@login_required(login_url='/')
def listar_estudiante(request):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        titulo = 'Listado de estudiantes'
        context = {'listar_estudiante': Estudiante.objects.all(), 'titulo': titulo}
        return render(request, "listar_estudiante.html", context)

@login_required(login_url='/')
def insertar_proyecto(request, id=0):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        # estudiantes = Estudiante.objects.all()
        if request.method == "GET":
            if id==0:
                form = ProyectoForm()
                titulo = 'Insertar nuevo Proyecto'
            else:
                proyect = Proyecto.objects.get(pk=id)
                form = ProyectoForm(instance=proyect)
                titulo = 'Editar Proyecto existente'
            return render(request, "insertar_proyecto.html", {'form':form, 'titulo': titulo})
        else:
            if id==0:
                form = ProyectoForm(request.POST)
            else:
                proyect = Proyecto.objects.get(pk=id)
                form = ProyectoForm(request.POST, instance=proyect)
            if form.is_valid():
                form.save()
                messages.success(request, 'Proyecto insertado.')
                return redirect('/coord/proyecto')
        return render(request, "insertar_proyecto.html", {'form':form, 'titulo': titulo})

@login_required(login_url='/')
def delete_proyecto(request, id):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        proj = Proyecto.objects.get(pk=id)
        proj.eliminado = True
        proj.save()
        return redirect('/coord/proyecto/listar')

@login_required(login_url='/')
def listar_proyecto(request):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        titulo = 'Listado de Proyectos'
        context = {'listar_proyecto': Proyecto.objects.all(), 'titulo': titulo}
        return render(request, "listar_proyecto.html", context)        

@login_required(login_url='/')
def insertar_item(request, id=0):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        if request.method == "GET":
            if id==0:
                form = ItemForm()
                titulo = 'Insertar nuevo indicador'
            else:
                item = Item.objects.get(pk=id)
                form = ItemForm(instance=item)
                titulo = 'Editar indicador existente'
            return render(request, "insertar_item.html", {'form':form, 'titulo': titulo})
        else:
            if id==0:
                form = ItemForm(request.POST)
            else:
                item = Item.objects.get(pk=id)
                form = ItemForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
            messages.success(request, 'Indicador insertado.')
            return redirect('/coord/rubrica/item')    

@login_required(login_url='/')
def delete_item(request, id):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        item = Item.objects.get(pk=id)
        item.eliminado = True
        item.save()
        return redirect('/coord/rubrica/item/listar')

@login_required(login_url='/')
def listar_item(request):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        titulo = 'Listado de Indicadores'
        context = {'listar_item': Item.objects.all(), 'titulo': titulo}
        return render(request, "listar_item.html", context)

@login_required(login_url='/')
def insertar_rubrica(request, id=0):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        GrupoFormSet = inlineformset_factory(Rubrica, Grupo, form=GrupoForm, fields=('nombre', 'peso', 'items'), extra=15, can_delete=False, max_num=15)

        indicadores = Item.objects.filter(eliminado=False)
        if request.method == "GET":
            if id==0:
                form = RubricaForm()
                form1 = GrupoFormSet()
                titulo = 'Insertar nueva Rúbrica'
            else:
                rub = Rubrica.objects.get(pk=id)
                form = RubricaForm(instance=rub)
                form1 = GrupoFormSet(instance=rub)
                titulo = 'Editar Rúbrica existente'
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
                            return redirect('/coord/rubrica')
                        else:
                            rub.delete()
                            messages.error(request, 'Los grupos deben sumar 100 en su peso/ponderación.')

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
        return render(request, "insertar_rubrica.html", {'form':form, 'form1': form1, 'titulo': titulo, 'indicadores': indicadores, 'indice': 0})

@login_required(login_url='/')
def delete_rub(request, id):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        rub = Rubrica.objects.get(pk=id)
        rub.eliminado = True
        rub.save()
        return redirect('/coord/rubrica/listar')

@login_required(login_url='/')
def listar_rubrica(request):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        titulo = 'Listado de Rúbricas'
        context = {'listar_rubrica': Rubrica.objects.all(), 'grupos': Grupo.objects.all(), 'titulo': titulo}
        return render(request, "listar_rubrica.html", context)

@login_required(login_url='/')
def insertar_clasificacion(request, id=0):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        if request.method == "GET":
            if id==0:
                form = ClasificacionForm()
                titulo = 'Insertar nueva clasificación'
            else:
                clasif = Clasificacion.objects.get(pk=id)
                form = ClasificacionForm(instance=clasif)
                titulo = 'Editar clasificación existente'
            return render(request, "insertar_clasif.html", {'form':form, 'titulo': titulo})
        else:
            if id==0:
                form = ClasificacionForm(request.POST)
            else:
                clasif = Clasificacion.objects.get(pk=id)
                form = ClasificacionForm(request.POST, instance=clasif)
            if form.is_valid():
                form.save()
            messages.success(request, 'Clasificación insertada.')
            return redirect('/coord/proyecto/clasificacion')    

@login_required(login_url='/')
def delete_clasif(request, id):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        clasif = Clasificacion.objects.get(pk=id)
        clasif.eliminado = True
        clasif.save()
        return redirect('/coord/proyecto/clasificacion/listar')

@login_required(login_url='/')
def listar_clasificacion(request):
    if userRole(request) == 2:
        return redirect('/jurado_home/')
    elif userRole(request) == 1:
        titulo = 'Listado de clasificaciones'
        context = {'listar_clasificacion': Clasificacion.objects.all(), 'titulo': titulo}
        return render(request, "listar_clasif.html", context)

@login_required(login_url='/')
def profile(request):
    usr = request.user
    queryset = Usuario.objects.filter(user=usr.id)
    titulo = 'Perfil de usuario'
    for item in queryset:
        usuario = item
    form = ProfileForm(instance=usuario)
    if usuario.rol == 1:
        page = "profile_coord.html"
    else:
        page = "profile_jurado.html"
    return render(request, page, {'form': form, 'titulo': titulo})

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
# =======================================================   JURADO   ========================================================

@login_required(login_url='/')
def jurado_home(request):
    if userRole(request) == 1:
        return redirect('/coord_home')
    elif userRole(request) == 2:
        titulo = 'Dashboard'
        usuario = Usuario.objects.get(user=request.user)
        try:
            evaluacion = Evaluacion.objects.get(juez=usuario)
            prog = Programacion.objects.exclude(pk=evaluacion.programacion.id).filter(Q(presidenteJurado=usuario.id) | Q(jurado=usuario.id)).distinct()
        except ObjectDoesNotExist:
            prog = Programacion.objects.filter(Q(presidenteJurado=usuario.id) | Q(jurado=usuario.id)).distinct()
        evaluaciones = Evaluacion.objects.filter(juez=usuario)
        e = evaluaciones.count()
        p = prog.count()
        return render(request, "jurado_home.html", {'prog': p, 'eval': e, 'titulo': titulo})

@login_required(login_url='/')
def evaluaciones_disp(request):
    if userRole(request) == 1:
        return redirect('/coord_home')
    elif userRole(request) == 2:
        user = request.user
        usuario = Usuario.objects.get(user=user.id)
        try:
            evaluacion = Evaluacion.objects.get(juez=usuario)
            prog = Programacion.objects.exclude(pk=evaluacion.programacion.id).filter(Q(presidenteJurado=usuario.id) | Q(jurado=usuario.id)).distinct()
        except ObjectDoesNotExist:
            prog = Programacion.objects.filter(Q(presidenteJurado=usuario.id) | Q(jurado=usuario.id)).distinct()
        titulo = 'Evaluaciones disponibles'
        return render(request, "eval_disp.html", {'listar_prog': prog, 'titulo': titulo})

@login_required(login_url='/')
def evaluacion(request, id):
    if userRole(request) == 1:
        return redirect('/coord_home')
    elif userRole(request) == 2:
        prog = Programacion.objects.get(pk=id)
        proyecto = Proyecto.objects.get(pk=prog.proyecto.id)
        rub = prog.rubrica
        grupos = Grupo.objects.filter(rubrica=rub.id)
        titulo = 'Ficha de Evaluación'
        context = {'evaluacion': grupos, 'proyecto': proyecto, 'prog': prog, 'titulo': titulo}
        if request.method == "POST":
            usuario = Usuario.objects.get(user=request.user.id)
            evaluacion = request.POST
            ponderacion = 0
            observ = evaluacion.get('observaciones')
            for key in evaluacion:
                if 'rad' in key:
                    ponderacion += int(evaluacion[key])
            e = Evaluacion.create(rub, prog, ponderacion, observ, usuario)
            e.save()
            return redirect('/jurado/evaluacion/listar')
        
        return render(request, 'evaluacion.html', context)

@login_required(login_url='/')
def listar_evaluacion(request):
    if userRole(request) == 1:
        return redirect('/coord_home')
    elif userRole(request) == 2:
        juez = Usuario.objects.get(user=request.user)
        evaluaciones = Evaluacion.objects.filter(juez=juez)
        titulo = 'Evaluaciones realizadas'
        context = {'listar_eval': evaluaciones, 'titulo': titulo}
        return render(request, "listar_eval.html", context)

def calificacionFinal(evaluaciones):
    n = len(evaluaciones)
    total = 0
    for eval in evaluaciones:
        total += eval.ponderacion
    division = total/n
    modulo = division % 10
    total = int(division) if modulo < 5 else int(division+1) #redondeo cuando la parte decimal es mayor o igual a 5
    return total

def letra(total):
        if 90 <= total <= 100:
            return 'A'
        elif 80 <= total < 90:
            return 'B'
        elif 70 <= total < 80:
            return 'C'
        elif 60 <= total < 70:
            return 'D'
        elif total < 60:
            return 'F'

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        ev = Evaluacion.objects.get(pk=id)
        programacion = Programacion.objects.get(pk=ev.programacion.id)
        evaluaciones = Evaluacion.objects.filter(programacion=programacion.id)
        proyecto = Proyecto.objects.get(pk=programacion.proyecto.id)
        total = calificacionFinal(evaluaciones)
        ltr = letra(total)
        context = {'eval': evaluaciones, 'prog': programacion, 'proyecto': proyecto, 'total': total, 'letra': ltr}
        pdf = render_to_pdf('pdf_template.html', context)
        return HttpResponse(pdf, content_type='application/pdf')