from django.shortcuts import render

from urappiapp.models import Shop


# Vista principal: muestra todas las tiendas
def index(request):
    tiendas = Shop.objects.all()  # Obtiene todas las tiendas de la base de datos
    info = {"usuario": {}, "tiendas": tiendas}
    return render(request, "pedidos/stores_view.html", info)
