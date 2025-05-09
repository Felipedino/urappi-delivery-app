from django.shortcuts import render
from urappiapp.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

def home_view(request):
    return render(request, "urappiapp/index.html")

# Create your views here.
def register_user(request):
    if request.method == 'GET':
        return render(request, "urappiapp/register_user.html")

    elif request.method == 'POST':
        nombre = request.POST['nombre']
        contraseña = request.POST['contraseña']
        apodo = request.POST['apodo']
        pronombre = request.POST['pronombre']
        mail = request.POST['mail']

        #Crear el nuevo usuario
        user = User.objects.create_user(username=nombre, password=contraseña, email=mail, apodo=apodo, pronombre=pronombre)
        return render(request, "urappiapp/register_user.html")
    
def login_user(request):
    if request.method == 'GET':
        return render(request,"urappiapp/login.html")
    
    if request.method == 'POST':
        username = request.POST['username']
        contraseña = request.POST['contraseña']
        usuario = authenticate(username=username,password=contraseña)
        if usuario is not None:
            login(request,usuario)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/register')
        
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')