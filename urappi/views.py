from django.shortcuts import render


# Vista de perfil para repartidor
def repartidor_perfil(request):
    return render(request, "urappi/repartidor.html")
