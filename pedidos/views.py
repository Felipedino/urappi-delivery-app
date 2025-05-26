from django.shortcuts import get_object_or_404, render

from urappiapp.models import ProductListing, Shop


# Vista que muestra el listado de tiendas
def show_listado_tiendas(request):
    tiendas = Shop.objects.all()

    #por ahora se usa un usuario falso para mostrar en el header
    usuario = {
        "nombre": "Juan Carlos", "upuntos":1000, "profilePic": "pedidos/svg/portrait_placeholder.png"
    }

    info = {"usuario": usuario, "tiendas": tiendas}

    return render(request, "pedidos/stores_view.html", info)

# Muestra los productos disponibles en la tienda seleccionada
# Se obtiene el id de la tienda en el url
# Se muestran los productos acorde al id de la tienda
def show_store_menu(request, id):    
    tienda = get_object_or_404(Shop, id=id) #si se intenta acceder a una tienda que no existe lanza error
    productos_listados = ProductListing.objects.filter(listedBy=tienda)

    # se extrae cada producto
    productos = []
    for pl in productos_listados:
        productos.append({
            "ProductName": pl.listedProduct.productName,
            "priceCLP": pl.listedProduct.priceCLP,
            "description": pl.listedProduct.description,
            "imageURL": pl.listedProduct.imageURL
        })
        
    #por ahora se usa un usuario falso para mostrar en el header
    usuario = {
        "nombre": "Juan Carlos", "upuntos":1000, "profilePic": "pedidos/svg/portrait_placeholder.png"
    }
    
    info = {"tienda_id": id, "tienda": tienda, "productos": productos, "usuario": usuario}

    return render(request, 'pedidos/store_menu.html', info)
