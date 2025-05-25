from django.shortcuts import render, get_object_or_404
from urappiapp.models import Shop, ProductListing

def show_listado_tiendas(request):
    # Aqui se debería hacer una petición a la base de datos
    # Por mientras voy a poner información de mentira
    tiendas_ej = [
        {"shopID": 1, "shopName": "Cafeta", "shopDescription": "Café, pasteles, empanadas, etc.", "imageURL": "pedidos/svg/store-icon.png"},
        {"shopID": 2, "shopName": "Delta Te", "shopDescription": "Café de especialidad", "imageURL": "pedidos/svg/store-icon.png"},
        {"shopID": 3, "shopName": "La Sonia", "shopDescription": "Tacos al mejor estilo mexicano", "imageURL": "pedidos/svg/store-icon.png"},
        {"shopID": 4, "shopName": "Máquina de café industrias", "shopDescription": "Café", "imageURL": "pedidos/svg/store-icon.png"},
        {"shopID": 5, "shopName": "Máquina de café industrias", "shopDescription": "Café", "imageURL": "pedidos/svg/store-icon.png"},
        {"shopID": 6, "shopName": "Máquina de café industrias", "shopDescription": "Café", "imageURL": "pedidos/svg/store-icon.png"},
        {"shopID": 7, "shopName": "Máquina de café industrias", "shopDescription": "Café", "imageURL": "pedidos/svg/store-icon.png"},
        {"shopID": 8, "shopName": "Máquina de café industrias", "shopDescription": "Café", "imageURL": "pedidos/svg/store-icon.png"},

    ]

    # Con esto se debería pedir la información a la base de datos, como no tienen info voy a usar la info estática
    #tiendas = Shop.objects.all()
    

    usuario = {
        "nombre": "Juanin", "upuntos":1000, "profilePic": "pedidos/svg/portrait_placeholder.png"
    }

    info = {"usuario": usuario, "tiendas": tiendas_ej}

    return render(request, 'pedidos/stores_view.html', info)


def show_store_menu(request, id):
    tienda_ej = {"shopID": 4, "shopName": "Cafeta", "ubication":"La sobria", "shopDescription": "Café, shandwich, empanadas, etc.", "imageURL": "pedidos/svg/store-icon.png"}
    
    tienda = get_object_or_404(Shop, id=id) #si se intenta acceder a una tienda que no existe lanza error
    productos_listados = ProductListing.objects.filter(listedBy=tienda)
    productos = []
    for pl in productos_listados:
        productos.append({
            "ProductName": pl.listedProduct.productName,
            "priceCLP": pl.listedProduct.priceCLP,
            "description": pl.listedProduct.description,
            "imageURL": pl.listedProduct.imageURL
        })
        

    productos_ej = [
        {
            "ProductName": "Café Americano",
            "priceCLP": 1800,
            "description": "Café negro tradicional.",
            "imageURL": "pedidos/svg/americano.png"
        },
        {
            "ProductName": "Capuchino",
            "priceCLP": 2200,
            "description": "Café espresso con leche espumosa y un toque de cacao.",
            "imageURL": "pedidos/svg/capuchino.png"
        },
        {
            "ProductName": "Té Chai Latte",
            "priceCLP": 2500,
            "description": "Té negro con especias, leche y un suave dulzor.",
            "imageURL": "pedidos/svg/te-chai.png"
        },
        {
            "ProductName": "Croissant de Mantequilla",
            "priceCLP": 1500,
            "description": "Crujiente y dorado, perfecto para acompañar tu café.",
            "imageURL": "pedidos/svg/croissant.png"
        },
        {
            "ProductName": "Muffin de Arándanos",
            "priceCLP": 1700,
            "description": "Suave muffin casero con arándanos frescos.",
            "imageURL": "pedidos/svg/muffin.png"
        }
    ]

    return render(request, 'pedidos/store_menu.html', {"tienda_id": id, "tienda": tienda, "productos": productos})
