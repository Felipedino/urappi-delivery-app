from django.shortcuts import render

def show_listado_tiendas(request):
    # Aqui se debería hacer una petición a la base de datos
    # Por mientras voy a poner información de mentira
    # Esta info tampoco representa la estructura real de la base de datos
    tiendas = [
        {"shopID": 1, "shopName": "Cafeta", "description": "Café, pasteles, empanadas, etc.", "imageURL": "pedidos/svg/store-icon.png"},
        {"shopID": 2, "shopName": "Delta Te", "description": "Café de especialidad", "imageURL": "pedidos/svg/store-icon.png"},
        {"shopID": 3, "shopName": "La Sonia", "description": "Tacos al mejor estilo mexicano", "imageURL": "pedidos/svg/store-icon.png"},
        {"shopID": 4, "shopName": "Máquina de café industrias", "description": "Café", "imageURL": "pedidos/svg/store-icon.png"},
        {"shopID": 5, "shopName": "Máquina de café industrias", "description": "Café", "imageURL": "pedidos/svg/store-icon.png"},
        {"shopID": 6, "shopName": "Máquina de café industrias", "description": "Café", "imageURL": "pedidos/svg/store-icon.png"},
        {"shopID": 7, "shopName": "Máquina de café industrias", "description": "Café", "imageURL": "pedidos/svg/store-icon.png"},
        {"shopID": 8, "shopName": "Máquina de café industrias", "description": "Café", "imageURL": "pedidos/svg/store-icon.png"},

    ]
    usuario = {
        "nombre": "Juanin", "upuntos":1000, "profilePic": "pedidos/svg/portrait_placeholder.png"
    }
    return render(request, 'pedidos/stores_view.html', {"usuario": usuario, "tiendas": tiendas})


def show_store_menu(request, id):
    tienda = {"shopID": 4, "shopName": "Cafeta", "ubication":"La sobria", "shopDescription": "Café, shandwich, empanadas, etc.", "imageURL": "pedidos/svg/store-icon.png"}
    productos = [
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
