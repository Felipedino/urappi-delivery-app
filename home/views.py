# Create your views here.
from django.shortcuts import render
from urappiapp.models import Shop



def index(request):
    tiendas = Shop.objects.all()
    
    info = {"usuario": {}, "tiendas": tiendas}

    return render(request, 'pedidos/stores_view.html', info)
