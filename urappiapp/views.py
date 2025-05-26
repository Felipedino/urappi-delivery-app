from django.shortcuts import render
from urappiapp.models import User, Cart, CartItem
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


# Create your views here.
def register_user(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
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
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            return render(request,"urappiapp/login.html")
    
    if request.method == 'POST':
        
        username = request.POST['username']
        contraseña = request.POST['contraseña']
        usuario = authenticate(username=username,password=contraseña)
        if usuario is not None:
            login(request,usuario)
            return HttpResponseRedirect('/')
        else:
            return render(request, "urappiapp/login.html", {'login_failed': True})
        
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login')
def show_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        items = CartItem.objects.filter(cart=cart).select_related('product_listing__listedProduct', 'product_listing__listedBy')
    except Cart.DoesNotExist:
        items = []

    # Añadir el subtotal a cada item
    for item in items:
        item.subtotal = item.quantity * item.product_listing.listedProduct.priceCLP

    total_price = sum(item.subtotal for item in items)

    return render(request, 'urappiapp/cart.html', {
        'cart_items': items,
        'total_price': total_price
    })
