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
        context = {'user_list':Usuario.objects.all()}
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
                user = User.objects.create_user(username=username, password=pw1)
                user.is_active = True
                user.save()
                usr = User.objects.get(username=username)
                nombre = request.POST['nombre']
                apellido = request.POST['apellido']
                fecha = request.POST['fecha']
                rol = request.POST['rol']
                usuario = Usuario.create(nombre, apellido, fecha, rol, usr)
                usuario.save()
                messages.success(request, 'Usuario registrado!')
                return redirect('/')
        else:
            messages.error(request, 'Los passwords no coinciden.')
    form = UserCreationForm()
    form1 = FirstUsuarioForm()
    return render(request, "firstUser.html", {'form': form, 'form1': form1})

@login_required(login_url='/')
def user_register(request):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        if request.method == "POST":
            username = request.POST['username']
            pw1 = request.POST['password1']
            pw2 = request.POST['password2']
            if pw1 == pw2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Nombre de usuario ya existe.')
                else:
                    user = User.objects.create_user(username=username, password=pw1)
                    user.is_active = True
                    user.save()
                    return redirect("/usuario/registrar")
            else:
                messages.error(request, 'Los passwords no coinciden.')
        form = UserCreationForm()
        return render(request, "user_form2.html", {'form': form})

@login_required(login_url='/')
def usuario_register(request, id=0):
    if userRole(request) == 2:
        return redirect('/jurado_home')
    elif userRole(request) == 1:
        user = User.objects.latest('date_joined')
        if request.method == "POST":
            if id==0:
                form = UsuarioForm(request.POST)
            else:
                usuario = Usuario.objects.get(pk=id)
                form = UsuarioForm(request.POST, instance=usuario)
            if form.is_valid():
                form.save()
                messages.success(request, 'Usuario insertado.')
                return redirect('/usuario/listar')
        else:
            if id==0:
                form = UsuarioForm(initial={'user': user.id})
            else:
                usuario = Usuario.objects.get(pk=id)
                form = UsuarioForm(instance=usuario)
        
        return render(request, "user_form.html", {'form': form})

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