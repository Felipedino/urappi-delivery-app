from datetime import datetime
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction

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
                "id": pl.listedProduct.productID,
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
        print(request.POST)
    if request.method == "POST":
        product_id = request.POST.get("product_id")  # <-- CAMBIA "product_name" por "product_id"
        quantity = int(request.POST.get("quantity", 1))

        try:
            product = Product.objects.get(productID=product_id)  # <-- BÚSQUEDA POR ID
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

    # Se agrupa por tienda
    tiendas = defaultdict(list)
    for item in items:
        tiendas[item.product_listing.listedBy].append(item)

    # Info del carrito
    info = {
        "usuario": request.user,
        "cart_items": items,
        "cart_items_by_shop": dict(tiendas),
        "total_price": total_price,
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

# Vista para crear orden al comprar carrito
@login_required(login_url="/login") # Se requiere estar logueado para crear una orden
@transaction.atomic # create_order se define como una transaccion atomica, es decir que si falla, se deshacen todos los cambios hechos en la base de datos.
def create_order(request):
    if request.method == "POST":
        # Obtener el carrito del usuario
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart).select_related(
            "product_listing", "product_listing__listedProduct"
        )

        # Se agrupan los ítems por tienda
        tiendas = {}
        for item in cart_items:
            shop = item.product_listing.listedBy
            if shop.shopID not in tiendas:
                tiendas[shop.shopID] = {"shop": shop, "items": []}
            tiendas[shop.shopID]["items"].append(item)

        # Se crea una orden para los productos de cada tienda
        for idx, (shop_id, data) in enumerate(tiendas.items()):
            # Se obtiene el texto de instrucciones de entrega ingresado para esta tienda
            instructions = request.POST.get(f"instructions_{idx}", "")
            shop = data["shop"]

            # Se crea la orden en la base de datos
            order = Order.objects.create(
                customer=request.user,  # El usuario que hace la compra
                shop=shop,  # La tienda
                createdAt=datetime.now(),  # Fecha actual
                deliveredAt=None,  # Estado inicial
                deliveryLocation=shop.location,  # Ubicación por defecto de la tienda
                status=1,  # Estado inicial
                deliveryInstructions=instructions,  # Instrucciones de entrega
            )

            # Se ingresan los ítems individuales a la orden
            for item in data["items"]:
                product = item.product_listing.listedProduct  # Obtiene el producto asociado a ese item del carrito
                OrderItem.objects.create(
                    order=order,  # Relaciona este OrderItem con la orden creada (para la tienda actual)
                    product=product,  # Producto solicitado
                    quantity=item.quantity,  # Cantidad que el usuario agregó al carrito de este producto
                    price=product.priceCLP,  # Precio del producto
                )

        # Se limpia el carrito
        cart_items.delete()

        # Se redirecciona al home luego de haber ingresado todo a la base de datos
        return redirect("home")

    else:
        return redirect("cart") # Si por alguna razon no se realiza un post y se accede a esta función, no pasa nada y el usuario permanece en el carrito
