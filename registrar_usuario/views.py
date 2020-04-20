from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import UsuarioForm, FirstUsuarioForm
from .models import Usuario

def userRole(request):
    usuario = Usuario.objects.get(user=request.user.id)
    if usuario.rol == 1:
        return 1
    elif usuario.rol == 2:
        return 2

@login_required(login_url='/')
def user_list(request):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        titulo = 'Listado de Usuarios'
        context = {'user_list':Usuario.objects.all(), 'titulo': titulo}
        return render(request, "user_list.html", context)

def first_user(request):
    try:
        users = Usuario.objects.all()[:1].get()
        context = {'condicion': users}
    except ObjectDoesNotExist:
        users = None
        context = {'condicion': users}
    if users != None:
        return redirect('/')
    if request.method == "POST":
        username = request.POST['username']
        pw1 = request.POST['password1']
        pw2 = request.POST['password2']
        if pw1 == pw2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Nombre de usuario ya existe.')
            else:
                nombre = request.POST['nombre']
                apellido = request.POST['apellido']
                email = request.POST['email']
                rol = request.POST['rol']
                dept = request.POST['dept']
                dominio = email.split('@')[1]
                if dominio == 'ce.pucmm.edu.do':
                    user = User.objects.create_user(username=username, password=pw1)
                    user.is_active = True
                    user.save()
                    usr = User.objects.get(username=username)
                    usuario = Usuario.create(nombre, apellido, email, rol, dept, usr)
                    usuario.save()
                    messages.success(request, 'Usuario registrado')
                    return redirect('/')
                else:
                    messages.error(request, 'ERROR: El dominio del correo debe ser @ce.pucmm.edu.do')
                    return redirect('/registro')
        else:
            messages.error(request, 'Los passwords no coinciden.')
    form = UserCreationForm()
    form1 = FirstUsuarioForm()
    return render(request, "firstUser.html", {'form': form, 'form1': form1})

@login_required(login_url='/')
def usuario_register(request):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        form = UsuarioForm()
        titulo = 'Insertar Nuevo Usuario'
        if request.method == "POST":
            username = request.POST['username']
            pw1 = request.POST['password1']
            pw2 = request.POST['password2']
            if pw1 == pw2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'ERROR: Nombre de usuario ya existe.')
                else:
                    nombre = request.POST['nombre']
                    apellido = request.POST['apellido']
                    email = request.POST['email']
                    rol = request.POST['rol']
                    dept = request.POST['dept']
                    dominio = email.split('@')[1]
                    if dominio == 'ce.pucmm.edu.do':
                        user = User.objects.create_user(username=username, password=pw1)
                        user.is_active = True
                        user.save()
                        usr = User.objects.get(username=username)
                        usuario = Usuario.create(nombre, apellido, email, rol, dept, usr)
                        usuario.save()
                        messages.success(request, 'Usuario registrado')
                        return redirect('/usuario/registrar')
                    else:
                        messages.error(request, 'ERROR: El dominio del correo debe ser @ce.pucmm.edu.do')
                        return redirect('/usuario/registrar')
            else:
                messages.error(request, 'ERROR: Las contraseñas no coinciden.')
        context = {'form': form, 'titulo': titulo}
        return render(request, "user_form.html", context)

@login_required(login_url='/')
def usuario_update(request, id=0):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        if request.method == "POST":
            usuario = Usuario.objects.get(pk=id)
            form = UsuarioForm(request.POST, instance=usuario)
            if form.is_valid():
                form.save()
                messages.success(request, 'Usuario actualizado.')
                return redirect('/usuario/listar')
        else:
            titulo = 'Editar Usuario Existente'
            usuario = Usuario.objects.get(pk=id)
            form = UsuarioForm(instance=usuario)
        
        return render(request, "user_form2.html", {'form': form, 'titulo': titulo}) 

@login_required(login_url='/')
def user_delete(request, id):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        usuario = Usuario.objects.get(pk=id)
        user = usuario.user
        usuario.eliminado = True
        usuario.save()
        user.is_active = False
        user.save()
        return redirect('/usuario/listar/')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/coord_home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            passw = request.POST.get('password')

            user = authenticate(request, username=username, password=passw)

            if user is not None and user.is_active == True:
                login(request, user)
                if userRole(request) == 1:
                    return redirect('coord_home/')
                elif userRole(request) == 2:
                    return redirect('jurado_home/')
            else:
                messages.error(request, 'Usuario o contraseña incorrecta.')
    try:
        users = Usuario.objects.all()[:1].get()
        context = {'condicion': users}
    except ObjectDoesNotExist:
        users = None
        context = {'condicion': users}

    return render(request, "login.html", context)
    

@login_required(login_url='/')
def user_logout(request):
    logout(request)
    return redirect('/')