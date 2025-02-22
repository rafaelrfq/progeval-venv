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
from .forms import ProgForm, EstudianteForm, ProyectoForm, ItemForm, RubricaForm, ClasificacionForm, ProfileForm, GrupoForm, CarreraForm, ClaseForm
from .models import Programacion, Estado, Evaluacion, Proyecto, Clasificacion, Rubrica, Grupo, Item, Estudiante, Carrera, IndicadorEvaluado, Clase
from registrar_usuario.views import userRole
from registrar_usuario.models import Usuario
import datetime

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
        clases = Clase.objects.all()
        carreras = Carrera.objects.all()
        prog_evaluadas = Programacion.objects.filter(ponderacion__lte=100)

        p = proyectos.count()
        r = rubricas.count()
        i = items.count()
        e = estudiantes.count()
        pr = programaciones.count()
        c = clasificaciones.count()
        u = usuarios.count()
        cl = clases.count()
        ca = carreras.count()
        ev = evaluaciones.count()
        pev = prog_evaluadas.count()
        titulo = 'Dashboard'

        context = {'titulo': titulo, 'p': p, 'r': r, 'i': i, 'e': e, 'pr': pr, 'c': c, 'u': u, 'ev': ev, 'cl': cl, 'ca': ca, 'pev': pev}
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
        titulo = 'Programación de presentación de proyectos'
        if request.method == "GET":
            if id==0 and rub != None:
                form = ProgForm(initial={'rubrica': rub.id, 'estado': 'Programada'})
            elif id==0 and rub == None:
                form = ProgForm()
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
        titulo = 'Insertar nuevo estudiante'
        if request.method == "GET":
            if id==0:
                form = EstudianteForm()
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
        return render(request, "insertar_estudiante.html", {'form':form, 'titulo': titulo})

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
def insertar_clase(request, id=0):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        if request.method == "GET":
            if id==0:
                form = ClaseForm()
                titulo = 'Insertar nueva clase'
            else:
                clase = Clase.objects.get(pk=id)
                form = ClaseForm(instance=clase)
                titulo = 'Editar clase existente'
            return render(request, "insertar_clase.html", {'form':form, 'titulo': titulo})
        else:
            if id==0:
                form = ClaseForm(request.POST)
            else:
                clase = Clase.objects.get(pk=id)
                form = ClaseForm(request.POST, instance=clase)
            if form.is_valid():
                form.save()
                messages.success(request, 'Clase insertada.')
            return redirect('/coord/clase')

@login_required(login_url='/')
def delete_clase(request, id):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        clase = Clase.objects.get(pk=id)
        clase.eliminado = True
        clase.save()
        return redirect('/coord/clase/listar')

@login_required(login_url='/')
def listar_clase(request):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        titulo = 'Listado de Clases'
        context = {'listar_clase': Clase.objects.all(), 'titulo': titulo}
        return render(request, "listar_clase.html", context)

@login_required(login_url='/')
def insertar_carrera(request, id=0):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        if request.method == "GET":
            if id==0:
                form = CarreraForm()
                titulo = 'Insertar nueva carrera'
            else:
                carrera = Carrera.objects.get(pk=id)
                form = CarreraForm(instance=carrera)
                titulo = 'Editar carrera existente'
            return render(request, "insertar_carrera.html", {'form':form, 'titulo': titulo})
        else:
            if id==0:
                form = CarreraForm(request.POST)
            else:
                carrera = Carrera.objects.get(pk=id)
                form = CarreraForm(request.POST, instance=carrera)
            if form.is_valid():
                form.save()
                messages.success(request, 'Carrera insertada.')
            return redirect('/coord/carrera')

@login_required(login_url='/')
def delete_carrera(request, id):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        carrera = Carrera.objects.get(pk=id)
        carrera.eliminado = True
        carrera.save()
        return redirect('/coord/carrera/listar')

@login_required(login_url='/')
def listar_carrera(request):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        titulo = 'Listado de Carreras'
        context = {'listar_carrera': Carrera.objects.all(), 'titulo': titulo}
        return render(request, "listar_carrera.html", context)

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
        titulo = 'Insertar nuevo Proyecto'
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
def listar_prog_eval(request):
    if userRole(request) == 2:
        return redirect('/jurado_home/')
    elif userRole(request) == 1:
        titulo = 'Listado de programaciones evaluadas'
        programaciones = Programacion.objects.all()
        for prog in programaciones:
            evaluaciones = Evaluacion.objects.filter(programacion=prog.id).filter(rubrica=prog.rubrica)
            evaluaciones_reporte = Evaluacion.objects.filter(programacion=prog.id).filter(rubrica=prog.rubrica_reporte)
            total = calificacionFinal(evaluaciones, evaluaciones_reporte)
            Programacion.objects.filter(pk=prog.id).update(ponderacion=total)
        programaciones = Programacion.objects.all()
        context = {'titulo': titulo, 'listar_prog': programaciones}
        return render(request, "listar_prog_eval.html", context)

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
        antes = datetime.datetime.now() - datetime.timedelta(hours=1)
        despues = datetime.datetime.now() + datetime.timedelta(hours=1)
        hoy = datetime.date.today()
        prog = Programacion.objects.none()
        evaluaciones = Evaluacion.objects.filter(juez=usuario)
        if evaluaciones.exists():
            for evaluacion in evaluaciones:
                prog |= Programacion.objects.filter(~Q(pk=evaluacion.programacion.id)).filter(fecha=hoy.strftime("%Y-%m-%d"), hora__lte=despues.strftime("%H:%M:%S"), hora__gte=antes.strftime("%H:%M:%S")).filter(Q(presidenteJurado=usuario.id) | Q(jurado=usuario.id)).distinct()
        else:
            prog |= Programacion.objects.filter(fecha=hoy.strftime("%Y-%m-%d"), hora__lte=despues.strftime("%H:%M:%S"), hora__gte=antes.strftime("%H:%M:%S")).filter(Q(presidenteJurado=usuario.id) | Q(jurado=usuario.id)).distinct()
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
        antes = datetime.datetime.now() - datetime.timedelta(hours=1)
        despues = datetime.datetime.now() + datetime.timedelta(hours=1)
        hoy = datetime.date.today()
        prog = Programacion.objects.none()
        evaluaciones = Evaluacion.objects.filter(juez=usuario)
        if evaluaciones.exists():
            for evaluacion in evaluaciones:
                prog |= Programacion.objects.filter(~Q(pk=evaluacion.programacion.id)).filter(fecha=hoy.strftime("%Y-%m-%d"), hora__lte=despues.strftime("%H:%M:%S"), hora__gte=antes.strftime("%H:%M:%S")).filter(Q(presidenteJurado=usuario.id) | Q(jurado=usuario.id)).distinct()
        else:
            prog |= Programacion.objects.filter(fecha=hoy.strftime("%Y-%m-%d"), hora__lte=despues.strftime("%H:%M:%S"), hora__gte=antes.strftime("%H:%M:%S")).filter(Q(presidenteJurado=usuario.id) | Q(jurado=usuario.id)).distinct()
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
        usuario = Usuario.objects.get(user=request.user.id)
        titulo = 'Ficha de Evaluación'
        context = {'evaluacion': grupos, 'proyecto': proyecto, 'prog': prog, 'usuario': usuario, 'titulo': titulo, 'valores': range(1, rub.valorIndicador+1)}
        if request.method == "POST":
            usuario = Usuario.objects.get(user=request.user.id)
            evaluacion = request.POST
            ponderacion = 0
            ind_dict = {}
            observ = evaluacion.get('observaciones')
            hora = datetime.datetime.now()
            for key in evaluacion:
                for grupo in grupos:
                    for indicador in grupo.items.all():  
                        if str(indicador.id) == key:
                            ponderacion += int(evaluacion[key])
                            ind_dict[int(key)] = int(evaluacion[key])
            e = Evaluacion.create(rub, prog, ponderacion, observ, hora, usuario)
            e.save()
            eval = Evaluacion.objects.get(pk=e.id)
            for key in ind_dict:
                item = Item.objects.get(pk=key)
                calif = int(ind_dict[key])
                i = IndicadorEvaluado.create(calif, item, eval)
                i.save()
            url = '/jurado/evaluacion_r/' + str(id)
            return redirect(url)
        return render(request, 'evaluacion.html', context)

@login_required(login_url='/')
def evaluacion_reporte(request, id):
    if userRole(request) == 1:
        return redirect('/coord_home')
    elif userRole(request) == 2:
        prog = Programacion.objects.get(pk=id)
        proyecto = Proyecto.objects.get(pk=prog.proyecto.id)
        rub = prog.rubrica_reporte
        grupos = Grupo.objects.filter(rubrica=rub.id)
        usuario = Usuario.objects.get(user=request.user.id)
        titulo = 'Ficha de Evaluación Reporte Final'
        context = {'evaluacion': grupos, 'proyecto': proyecto, 'prog': prog, 'usuario': usuario, 'titulo': titulo, 'valores': range(1, rub.valorIndicador+1)}
        if request.method == "POST":
            usuario = Usuario.objects.get(user=request.user.id)
            evaluacion = request.POST
            ponderacion = 0
            ind_dict = {}
            observ = evaluacion.get('observaciones')
            hora = datetime.datetime.now()
            for key in evaluacion:
                for grupo in grupos:
                    for indicador in grupo.items.all():  
                        if str(indicador.id) == key:
                            ponderacion += int(evaluacion[key])
                            ind_dict[int(key)] = int(evaluacion[key])
            e = Evaluacion.create(rub, prog, ponderacion, observ, hora, usuario)
            e.save()
            eval = Evaluacion.objects.get(pk=e.id)
            for key in ind_dict:
                item = Item.objects.get(pk=key)
                calif = int(ind_dict[key])
                i = IndicadorEvaluado.create(calif, item, eval)
                i.save()
            return redirect('/jurado/evaluacion/listar')
        return render(request, 'evaluacion_reporte.html', context)

@login_required(login_url='/')
def ficha_evaluacion(request, id):
    evaluacion = Evaluacion.objects.get(pk=id)
    rubrica = Rubrica.objects.get(pk=evaluacion.rubrica.id)
    grupos = Grupo.objects.filter(rubrica=rubrica.id)
    prog = Programacion.objects.get(pk=evaluacion.programacion.id)
    proyecto = Proyecto.objects.get(pk=prog.proyecto.id)
    indicadores = IndicadorEvaluado.objects.filter(evaluacion=evaluacion)
    jurado = Usuario.objects.get(pk=evaluacion.juez.id)
    titulo = 'Ficha de Evaluación'
    context = {'eval': evaluacion, 'grupos': grupos, 'proyecto': proyecto, 'prog': prog, 'jurado': jurado, 'titulo': titulo, 'indicadores': indicadores, 'valores': range(1, rubrica.valorIndicador+1)}
    if userRole(request) == 1:
        return render(request, 'ficha_evaluada_coord.html', context)
    elif userRole(request) == 2:
        return render(request, 'ficha_evaluada_jurado.html', context)


@login_required(login_url='/')
def listar_evaluacion(request):
    if userRole(request) == 1:
        return redirect('/coord_home')
    elif userRole(request) == 2:
        jurado = Usuario.objects.get(user=request.user)
        evaluaciones = Evaluacion.objects.filter(juez=jurado)
        titulo = 'Evaluaciones realizadas'
        context = {'listar_eval': evaluaciones, 'titulo': titulo}
        return render(request, "listar_eval.html", context)

def calificacionFinal(evaluaciones, evaluaciones_reporte):
    n1 = len(evaluaciones)
    n2 = len(evaluaciones_reporte)
    n = n1 + n2
    total = 0
    for eval in evaluaciones:
        total += eval.ponderacion
    for eval in evaluaciones_reporte:
        total += eval.ponderacion
    division = total/n
    modulo = division % 10
    total = int(division) if modulo < 5 else int(division+1) #round up when the decimal part is 5 or higher
    return total

# def calificativo(total):
#         if 90 <= total <= 100:
#             return 'Excelente'
#         elif 80 <= total < 90:
#             return 'Muy Bueno'
#         elif 70 <= total < 80:
#             return 'Bueno'
#         elif 60 <= total < 70:
#             return 'Suficiente'
#         elif total < 60:
#             return 'Insuficiente'
# Movido a template filters en template_tags

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        programacion = Programacion.objects.get(pk=id)
        evaluaciones = Evaluacion.objects.filter(programacion=programacion.id).filter(rubrica=programacion.rubrica)
        evaluaciones_reporte = Evaluacion.objects.filter(programacion=programacion.id).filter(rubrica=programacion.rubrica_reporte)
        proyecto = Proyecto.objects.get(pk=programacion.proyecto.id)
        indicadores = IndicadorEvaluado.objects.all()
        grupos = Grupo.objects.filter(rubrica=programacion.rubrica)
        grupos_r = Grupo.objects.filter(rubrica=programacion.rubrica_reporte)
        total = calificacionFinal(evaluaciones, evaluaciones_reporte)
        valores = range(1, programacion.rubrica.valorIndicador+1)
        valores_r = range(1, programacion.rubrica_reporte.valorIndicador+1)
        context = {'eval': evaluaciones, 'eval_r': evaluaciones_reporte, 'prog': programacion, 'proyecto': proyecto, 'total': total, 'indicadores': indicadores, 'grupos': grupos, 'grupos_r': grupos_r, 'valores': valores, 'valores_r': valores_r}
        pdf = render_to_pdf('pdf_template.html', context)
        return HttpResponse(pdf, content_type='application/pdf')