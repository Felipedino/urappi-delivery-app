from urappiapp.models import User, Cart, CartItem

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from app_repartidor.views import repartidor_perfil

# Vista para registrar un nuevo usuario
def register_user(request):
    if request.method == "GET":
        # Si el usuario ya está autenticado, redirige al home
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        else:
            return render(request, "urappiapp/register_user.html")

    elif request.method == "POST":
        # Obtiene los datos del formulario de registro
        nombre = request.POST["nombre"]
        contraseña = request.POST["contraseña"]
        apodo = request.POST["apodo"]
        pronombre = request.POST["pronombre"]
        mail = request.POST["mail"]
        rol = request.POST.get("rol")
        # Crea el nuevo usuario con los datos proporcionados
        user = User.objects.create_user(
            username=nombre,
            password=contraseña,
            email=mail,
            apodo=apodo,
            pronombre=pronombre,
            rol=rol,
        )
        return render(request, "urappiapp/register_user.html")


# Vista para iniciar sesión de usuario
def login_user(request):
    if request.method == "GET":
        # Si el usuario ya está autenticado, redirige al home
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        else:
            return render(request, "urappiapp/login.html")

    if request.method == "POST":
        # Obtiene los datos del formulario de login
        username = request.POST["username"]
        contraseña = request.POST["contraseña"]
        usuario = authenticate(username=username, password=contraseña)
        if usuario is not None:
            # Si la autenticación es exitosa, inicia sesión y redirige al home
            login(request, usuario)
            return HttpResponseRedirect("/")
        else:
            # Si falla, muestra el formulario con un mensaje de error
            return render(request, "urappiapp/login.html", {"login_failed": True})
        

    

# Vista para cerrar sesión de usuario
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")
#-----------------------------------------redirigir según rol-----------------------------------------------
def redirect_by_role(user):
    """Redirige al usuario según su rol"""
    rol = user.rol
    
    if rol == "customer":
        return HttpResponseRedirect(reverse('comprador'))      
    elif rol == "deliver":
        return HttpResponseRedirect(reverse('repartidor'))  
    elif rol == "seller":
        return HttpResponseRedirect(reverse('vendedor'))        
    else:
        # Rol no válido, redirigir a página general con mensaje
        messages.warning(user, f"Rol no reconocido: {rol}")
        return HttpResponseRedirect(reverse('home'))
#------------------------------------------------Vistas según rol-----------------------------------------
#Vista para el comprador
def comprador(request):
    """Vista principal para clientes"""
    if not request.user.is_authenticated or request.user.rol != "customer":
        return redirect('login')
    
    context = {
        'user': request.user,
        'apodo': request.apodo,
        'Upuntos': request.puntos, 
    }
    return render(request, "app_comprador/_user_info.html", context)
#vista para el repartidor
def repartidor(request):
    if not request.user.is_authenticated or request.user.rol != "deliver":
        return redirect('login')
    
    return repartidor_perfil(request)
#Vista para el vendedor
def vendedor(request):
    if not request.user.is_authenticated or request.user.rol != "seller":
        return redirect('login')
    
    context = {
        'user': request.user,
        'apodo': request.apodo,
        'Upuntos': request.puntos, 
    }
    return render(request, "app_vendedor/my_store.html", context)