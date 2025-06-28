from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from urappiapp.models import (
    Cart,
    CartItem,
    Order,
    OrderItem,
    Product,
    ProductListing,
    Shop,
)


# Vista que muestra el listado de tiendas
def show_listado_tiendas(request):
    tiendas = Shop.objects.all()

    

    info = {"usuario": request.user,"tiendas": tiendas}

    return render(request, "app_comprador/stores_view.html", info)


def show_store_menu(request, id):
    tienda = get_object_or_404(
        Shop, shopID=id
    )  # si se intenta acceder a una tienda que no existe lanza error
    productos_listados = ProductListing.objects.filter(listedBy=tienda)
    productos = []
    for pl in productos_listados:
        pathFoto = "/media/" + str(pl.listedProduct.prodImage)
        productos.append(
            {
                "ProductName": pl.listedProduct.productName,
                "priceCLP": pl.listedProduct.priceCLP,
                "description": pl.listedProduct.description,
                "prodImage": pathFoto,
            }
        )


    info = {
        "tienda_id": id,
        "tienda": tienda,
        "productos": productos,
        "usuario": request.user,
    }

    return render(request, "app_comprador/store_menu.html", info)


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

    info = {

        "usuario": request.user,
    }
    return render(
        request,
        "app_comprador/cart.html",
         info,
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


login_required(login_url="/login")


# Vista para crear orden al comprar carrito
def create_order(request):
    # Obtener el carrito del usuario
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart).select_related(
        "product_listing", "product_listing__listedProduct"
    )

    # Obtener la tienda (asumimos que todos los productos son de la misma tienda)
    shop = cart_items[0].product_listing.listedBy

    # Crear la orden
    order = Order(
        customer=request.user,
        shop=shop,
        createdAt=datetime.now(),
        deliveredAt=None,  # Se establecerá cuando se entregue
        deliveryLocation=shop.location,
        status=1,  # 1 = Pendiente
    )
    order.save()

    # Crear los items de la orden
    for item in cart_items:
        product = item.product_listing.listedProduct
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item.quantity,
            price=product.priceCLP,
        )

    # Limpiar el carrito
    cart_items.delete()

    return redirect("home")
