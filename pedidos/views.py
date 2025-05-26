from django.shortcuts import get_object_or_404, render

from urappiapp.models import ProductListing, Shop


# Vista que muestra el listado de tiendas
def show_listado_tiendas(request):
    # Ejemplo de tiendas (puedes eliminar cuando uses la base de datos real)
    tiendas_ej = [
        {
            "shopID": 1,
            "shopName": "Cafeta",
            "shopDescription": "Café, pasteles, empanadas, etc.",
            "imageURL": "pedidos/svg/store-icon.png",
        },
        {
            "shopID": 2,
            "shopName": "Delta Te",
            "shopDescription": "Café de especialidad",
            "imageURL": "pedidos/svg/store-icon.png",
        },
        {
            "shopID": 3,
            "shopName": "La Sonia",
            "shopDescription": "Tacos al mejor estilo mexicano",
            "imageURL": "pedidos/svg/store-icon.png",
        },
        {
            "shopID": 4,
            "shopName": "Máquina de café industrias",
            "shopDescription": "Café",
            "imageURL": "pedidos/svg/store-icon.png",
        },
        {
            "shopID": 5,
            "shopName": "Máquina de café industrias",
            "shopDescription": "Café",
            "imageURL": "pedidos/svg/store-icon.png",
        },
        {
            "shopID": 6,
            "shopName": "Máquina de café industrias",
            "shopDescription": "Café",
            "imageURL": "pedidos/svg/store-icon.png",
        },
        {
            "shopID": 7,
            "shopName": "Máquina de café industrias",
            "shopDescription": "Café",
            "imageURL": "pedidos/svg/store-icon.png",
        },
        {
            "shopID": 8,
            "shopName": "Máquina de café industrias",
            "shopDescription": "Café",
            "imageURL": "pedidos/svg/store-icon.png",
        },
    ]

    # Obtiene todas las tiendas reales de la base de datos, actualmente usa la info estática
    tiendas = Shop.objects.all()

    usuario = {
        "nombre": "Juanin",
        "upuntos": 1000,
        "profilePic": "pedidos/svg/portrait_placeholder.png",
    }

    info = {"usuario": usuario, "tiendas": tiendas}

    return render(request, "pedidos/stores_view.html", info)


# Vista que muestra el menú de una tienda específica
def show_store_menu(request, id):
    tienda_ej = {
        "shopID": 4,
        "shopName": "Cafeta",
        "ubication": "La sobria",
        "shopDescription": "Café, shandwich, empanadas, etc.",
        "imageURL": "pedidos/svg/store-icon.png",
    }

    # Busca la tienda por id, lanza error 404 si no existe
    tienda = get_object_or_404(Shop, id=id)
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

    productos_ej = [
        {
            "ProductName": "Café Americano",
            "priceCLP": 1800,
            "description": "Café negro tradicional.",
            "imageURL": "pedidos/svg/americano.png",
        },
        {
            "ProductName": "Capuchino",
            "priceCLP": 2200,
            "description": "Café espresso con leche espumosa y un toque de cacao.",
            "imageURL": "pedidos/svg/capuchino.png",
        },
        {
            "ProductName": "Té Chai Latte",
            "priceCLP": 2500,
            "description": "Té negro con especias, leche y un suave dulzor.",
            "imageURL": "pedidos/svg/te-chai.png",
        },
        {
            "ProductName": "Croissant de Mantequilla",
            "priceCLP": 1500,
            "description": "Crujiente y dorado, perfecto para acompañar tu café.",
            "imageURL": "pedidos/svg/croissant.png",
        },
        {
            "ProductName": "Muffin de Arándanos",
            "priceCLP": 1700,
            "description": "Suave muffin casero con arándanos frescos.",
            "imageURL": "pedidos/svg/muffin.png",
        },
    ]

    # Renderiza el menú de la tienda con los productos
    return render(
        request,
        "pedidos/store_menu.html",
        {"tienda_id": id, "tienda": tienda, "productos": productos},
    )
