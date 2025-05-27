from urappiapp.models import Shop, Product, ProductListing, Cart, CartItem

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


# Vista que muestra el listado de tiendas
def show_listado_tiendas(request):
    tiendas = Shop.objects.all()

    usuario = {
        "nombre": "Juan Carlos", "upuntos":1000, "profilePic": "pedidos/svg/portrait_placeholder.png"
    }

    info = {"usuario": usuario, "tiendas": tiendas}

    return render(request, "pedidos/stores_view.html", info)


def show_store_menu(request, id):
    tienda = get_object_or_404(Shop, id=id) #si se intenta acceder a una tienda que no existe lanza error
    productos_listados = ProductListing.objects.filter(listedBy=tienda)
    productos = []
    for pl in productos_listados:
        productos.append({
            "ProductName": pl.listedProduct.productName,
            "priceCLP": pl.listedProduct.priceCLP,
            "description": pl.listedProduct.description,
            "imageURL": pl.listedProduct.imageURL,
        })
        

    usuario = {
        "nombre": "Juan Carlos", "upuntos":1000, "profilePic": "pedidos/svg/portrait_placeholder.png"
    }

    info = {"tienda_id": id, "tienda": tienda, "productos": productos, "usuario": usuario}

    return render(request, 'pedidos/store_menu.html', info)


# Vista para añadir objetos al carrito
@login_required(login_url='/login')
def add_to_cart(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        quantity = int(request.POST.get("quantity", 1))

        try:
            # Busca el producto por nombre (puede ser problemático hacerlo así si hay dos productos con el mismo nombre)
            product = Product.objects.get(productName=product_name)
            # Se busca el ProductListing asociado
            product_listing = ProductListing.objects.get(listedProduct=product)
        except Product.DoesNotExist:
            return redirect(request.META.get('HTTP_REFERER', '/'))
        except ProductListing.DoesNotExist:
            return redirect(request.META.get('HTTP_REFERER', '/'))

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product_listing=product_listing,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect('/')

# Vista para mostrar el carrito
@login_required(login_url='/login')
def show_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        items = CartItem.objects.filter(cart=cart).select_related('product_listing__listedProduct', 'product_listing__listedBy')
    except Cart.DoesNotExist:
        items = []

    # Añadir el subtotal a cada item
    for item in items:
        item.subtotal = item.quantity * item.product_listing.listedProduct.priceCLP

    total_price = sum(item.subtotal for item in items)

    usuario = {
        "nombre": "Juan Carlos", "upuntos":1000, "profilePic": "pedidos/svg/portrait_placeholder.png"
    }

    return render(request, 'pedidos/cart.html', {
        'cart_items': items,
        'total_price': total_price,
        'usuario': usuario
    })
