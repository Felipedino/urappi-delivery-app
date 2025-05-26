from django.shortcuts import render

from urappiapp.models import Shop


# Vista principal: muestra todas las tiendas
def index(request):
    tiendas = Shop.objects.all()
    
    # Se usa un usuario falso para el header por ahora
    usuario = {
        "nombre": "Juan Carlos", "upuntos":1000, "profilePic": "pedidos/svg/portrait_placeholder.png"
    }
    
    info = {"usuario": usuario, "tiendas": tiendas}

    return render(request, 'pedidos/stores_view.html', info)
