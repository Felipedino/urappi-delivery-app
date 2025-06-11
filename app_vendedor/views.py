from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from urappiapp.models import (
    ProductListing,
    Shop,
)

def show_my_store(request):
    #Aqui la idea es obtener el id de la tienda a partir del usuario
    id = 1
    tienda = get_object_or_404(
        Shop, id=id
    ) 

    productos_listados = ProductListing.objects.filter(listedBy=tienda)
    productos = []
    for pl in productos_listados:
        productos.append(
            {
                "ProductName": pl.listedProduct.productName,
                "priceCLP": pl.listedProduct.priceCLP,
                "description": pl.listedProduct.description,
                "imageURL": pl.listedProduct.imageURL,
            }
        )

    info = {
        "tienda_id": id,
        "tienda": tienda,
        "productos": productos,
    }

    return render(request, "app_vendedor/my_store.html", info)