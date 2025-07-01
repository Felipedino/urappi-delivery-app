from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from app_comprador.views import show_listado_tiendas
from app_repartidor.views import repartidor_perfil
from app_vendedor.views import show_my_store
from urappiapp.models import Cart, CartItem, Shop, ShopOwner, User


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
        nombre = request.POST["nombre_usuario"]
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
        print(f"Usuario creado exitosamente:")
        print(f"- ID: {user.id}")
        print(f"- Username: {user.username}")
        print(f"- Rol asignado: {user.rol}")
        print(f"- Apodo: {user.apodo}")

        if rol == "seller":
            shopName = request.POST["nombre_tienda"]
            openTime = request.POST["hora_apertura"]
            closeTime = request.POST["hora_cierre"]
            ubication = request.POST["ubicacion_tienda"]
            description = request.POST["descr_tienda"]
            foto = request.FILES.get("foto_tienda", None)

            shop = Shop.objects.create(
                shopName=shopName,
                shopDescription=description,
                openTime=openTime,
                closingTime=closeTime,
                shopImage=foto,
                location=ubication,
            )

            owner = ShopOwner.objects.create(
                owner=user, shop=shop
            )  # Se asigna como dueño de la tienda creada

        return login_user(request)


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
        username = request.POST["nombre_usuario"]
        contraseña = request.POST["contraseña"]
        usuario = authenticate(username=username, password=contraseña)
        if usuario is not None:
            # Si la autenticación es exitosa, inicia sesión y redirige al home
            login(request, usuario)
            return redirect_by_role(request, usuario)
        else:
            # Si falla, muestra el formulario con un mensaje de error
            return render(request, "urappiapp/login.html", {"login_failed": True})


# Vista para cerrar sesión de usuario
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


# -----------------------------------------redirigir según rol-----------------------------------------------
def redirect_by_role(request, user):
    """Redirige al usuario según su rol"""
    rol = user.rol
    print(f"Redirigiendo usuario {user.username} con rol: {rol}")
    if rol == "customer":
        return HttpResponseRedirect(reverse("comprador"))
    elif rol == "deliver":
        return HttpResponseRedirect(reverse("repartidor"))
    elif rol == "seller":
        return HttpResponseRedirect(reverse("vendedor"))
    else:
        # Rol no válido, redirigir a página general con mensaje
        messages.warning(request, f"Rol no reconocido: {rol}")
        return HttpResponseRedirect(reverse("home"))


# ------------------------------------------------Vistas según rol-----------------------------------------
# Vista para el comprador
def comprador(request):
    """Vista principal para clientes"""
    if not request.user.is_authenticated or request.user.rol != "customer":
        return redirect("login")

    return show_listado_tiendas(request)


# Vista para el repartidor
def repartidor(request):
    if not request.user.is_authenticated or request.user.rol != "deliver":
        return redirect("login")

    return repartidor_perfil(request)


# Vista para el vendedor
def vendedor(request):
    if not request.user.is_authenticated or request.user.rol != "seller":
        return redirect("login")

    return show_my_store(request)


# Vista para el perfil para todos los usuarios
@login_required(login_url="/login")
def profile(request):
    """Vista de perfil"""
    context = {
        "usuario": request.user,
    }

    if request.user.rol == "seller":
        try:
            shop_owner = ShopOwner.objects.get(owner=request.user)
            context["tienda"] = shop_owner.shop
        except ShopOwner.DoesNotExist:
            context["tienda"] = None
    elif request.user.rol == "deliver":
        None

    elif request.user.rol == "customer":
        try:
            cart = Cart.objects.get(user=request.user)
            context["cart"] = cart
            context["cart_items"] = CartItem.objects.filter(cart=cart)
        except Cart.DoesNotExist:
            context["cart"] = None
            context["cart_items"] = []

    return render(request, "urappiapp/profile.html", context)


# Vista para recargar UPuntos
@login_required(login_url="/login")
def recharge_upuntos(request):
    """Vista para recargar UPuntos del usuario"""
    if request.method == "POST":
        amount = request.POST.get("amount")

        try:
            amount = int(amount)
            if amount > 0 and amount <= 100000:  # Límite máximo de recarga
                request.user.upuntos += amount
                request.user.save()
                messages.success(
                    request,
                    f"¡Recarga exitosa! Se agregaron ${amount} UPuntos a tu cuenta.",
                )
            else:
                messages.error(request, "El monto debe ser entre $1 y $100,000.")
        except (ValueError, TypeError):
            messages.error(request, "Por favor ingresa un monto válido.")

    return redirect("profile")
