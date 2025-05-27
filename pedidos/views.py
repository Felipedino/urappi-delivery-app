from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from urappiapp.models import Cart, CartItem, Product, ProductListing, Shop


# Vista que muestra el listado de tiendas
def show_listado_tiendas(request):
    tiendas = Shop.objects.all()

    usuario = {
        "nombre": "Juan Carlos",
        "upuntos": 1000,
        "profilePic": "pedidos/svg/portrait_placeholder.png",
    }

    info = {"usuario": usuario, "tiendas": tiendas}

    return render(request, "pedidos/stores_view.html", info)


def show_store_menu(request, id):
    tienda = get_object_or_404(
        Shop, id=id
    )  # si se intenta acceder a una tienda que no existe lanza error
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

    usuario = {
        "nombre": "Juan Carlos",
        "upuntos": 1000,
        "profilePic": "pedidos/svg/portrait_placeholder.png",
    }

    info = {
        "tienda_id": id,
        "tienda": tienda,
        "productos": productos,
        "usuario": usuario,
    }

    return render(request, "pedidos/store_menu.html", info)


# Vista para añadir objetos al carrito
@login_required(login_url="/login")
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
            return redirect(request.META.get("HTTP_REFERER", "/"))
        except ProductListing.DoesNotExist:
            return redirect(request.META.get("HTTP_REFERER", "/"))

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product_listing=product_listing, defaults={"quantity": quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        return redirect("/")


# Vista para mostrar el carrito
@login_required(login_url="/login")
def show_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        items = CartItem.objects.filter(cart=cart).select_related(
            "product_listing__listedProduct", "product_listing__listedBy"
        )
    except Cart.DoesNotExist:
        items = []

    # Añadir el subtotal a cada item
    for item in items:
        item.subtotal = item.quantity * item.product_listing.listedProduct.priceCLP

    total_price = sum(item.subtotal for item in items)

    usuario = {
        "nombre": "Juan Carlos",
        "upuntos": 1000,
        "profilePic": "pedidos/svg/portrait_placeholder.png",
    }

    return render(
        request,
        "pedidos/cart.html",
        {"cart_items": items, "total_price": total_price, "usuario": usuario},
    )


# Vista para eliminar un item del carrito
@login_required(login_url="/login")
def remove_from_cart(request, item_id):
    # Obtener el item o devolver 404 si no existe
    cart_item = get_object_or_404(CartItem, id=item_id)

    # Verificar que el item pertenezca al usuario actual
    if cart_item.cart.user == request.user:
        cart_item.delete()

    return redirect("cart")


# Vista para actualizar la cantidad de un artículo del carrito
@login_required(login_url="/login")
def update_cart(request, item_id, action):
    cart_item = get_object_or_404(CartItem, id=item_id)

    # Verificar que el item pertenezca al usuario actual
    if cart_item.cart.user == request.user:
        if action == "increase":
            cart_item.quantity += 1
            cart_item.save()
        elif action == "decrease":
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                # Si la cantidad llega a 0, eliminar el item
                cart_item.delete()

    # Redireccionar de vuelta al carrito
    return redirect("cart")
