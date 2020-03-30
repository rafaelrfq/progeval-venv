from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UsuarioForm
from .models import Usuario

@login_required(login_url='/')
def user_list(request):
    context = {'user_list':Usuario.objects.all()}
    return render(request, "user_list.html", context)

@login_required(login_url='/')
def user_register(request):
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
                coord = Usuario.objects.all().filter(rol=1)
                jurado = Usuario.objects.all().filter(rol=2)
                if coord.filter(user = user.pk).exists():
                    return redirect('coord_home/')
                elif jurado.filter(user = user.pk).exists():
                    return redirect('jurado_home/')
            else:
                messages.error(request, 'Usuario o contraseña incorrecta.')

    return render(request, "login.html")

@login_required(login_url='/')
def user_logout(request):
    logout(request)
    return redirect('/')