# Create your views here.
from django.shortcuts import render
from urappiapp.models import Shop



def index(request):
    tiendas = Shop.objects.all()
    usuario = {
        "nombre": "Juan Carlos", "upuntos":1000, "profilePic": "pedidos/svg/portrait_placeholder.png"
    }
    
    info = {"usuario": usuario, "tiendas": tiendas}

    return render(request, 'pedidos/stores_view.html', info)
