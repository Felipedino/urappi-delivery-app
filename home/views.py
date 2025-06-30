from django.shortcuts import render

from urappiapp.models import Shop


# Vista principal: muestra todas las tiendas
def index(request):
    tiendas = Shop.objects.all()

    info = {"usuario": request.user, "tiendas": tiendas}

    return render(request, "app_comprador/stores_view.html", info)
