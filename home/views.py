from django.shortcuts import render
from urappiapp.models import Shop


# Vista principal: muestra todas las tiendas
def index(request):
    tiendas = Shop.objects.all()
    usuario = {
        "nombre": "Juan Carlos", "upuntos":1000, "profilePic": "app_comprador/svg/portrait_placeholder.png"
    }

    info = {"usuario": usuario, "tiendas": tiendas}

    return render(request, 'app_comprador/stores_view.html', info)
