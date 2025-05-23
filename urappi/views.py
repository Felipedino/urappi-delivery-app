from django.shortcuts import render


def repartidor_perfil(request):
    return render(request, 'urappi/repartidor.html')
