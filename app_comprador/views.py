from collections import defaultdict
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from urappiapp.models import (
    Cart,
    CartItem,
    Notification,
    Order,
    OrderItem,
    Product,
    ProductListing,
    Shop,
    User,
)


# Vista que muestra el listado de tiendas
def show_listado_tiendas(request):
    tiendas = Shop.objects.all()
    shopsPerPage = 3
    paginator = Paginator(tiendas, shopsPerPage)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    info = {"usuario": request.user, "tiendas": page_obj}
    print(page_obj.object_list)

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
                "ProductID": pl.listedProduct.productID,
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
        product_id = request.POST.get("product_id")
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

    # Cálculo de costos
    total_price = sum(item.subtotal for item in items)
    delivery_fee = 1500  # Cargo fijo de envío
    final_total = total_price + delivery_fee

    # Verificar si el usuario tiene suficientes UPuntos
    sufficient_funds = request.user.upuntos >= final_total

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
        "delivery_fee": delivery_fee,
        "final_total": final_total,
        "sufficient_funds": sufficient_funds,
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
@login_required(login_url="/login")
@transaction.atomic  # Garantiza que todas las operaciones se realicen o ninguna
def create_order(request):
    if request.method == "POST":
        try:
            # Obtener el carrito del usuario
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart).select_related(
                "product_listing",
                "product_listing__listedProduct",
                "product_listing__listedBy",
            )

            if not cart_items:
                messages.error(request, "Tu carrito está vacío.")
                return redirect("cart")

            # Agrupar los ítems por tienda
            tiendas = {}
            total_price = 0
            for item in cart_items:
                shop = item.product_listing.listedBy
                if shop.shopID not in tiendas:
                    tiendas[shop.shopID] = {"shop": shop, "items": [], "total": 0}

                item_price = item.quantity * item.product_listing.listedProduct.priceCLP
                tiendas[shop.shopID]["items"].append(item)
                tiendas[shop.shopID]["total"] += item_price
                total_price += item_price

            # Cálculo de costos totales
            delivery_fee = 1500 * len(tiendas)  # Cargo fijo por cada tienda
            final_total = total_price + delivery_fee

            # Verificar si el usuario tiene suficientes UPuntos
            if request.user.upuntos < final_total:
                messages.error(
                    request, "No tienes suficientes UPuntos para completar esta compra."
                )
                return redirect("cart")

            # Deducir UPuntos del cliente
            request.user.upuntos -= final_total
            request.user.save()

            # Crear una orden para cada tienda
            for idx, (shop_id, data) in enumerate(tiendas.items()):
                # Obtener instrucciones de entrega para esta tienda
                instructions = request.POST.get(f"instructions_{idx}", "")
                shop = data["shop"]
                shop_total = data["total"]

                # Crear la orden
                order = Order.objects.create(
                    customer=request.user,
                    shop=shop,
                    createdAt=datetime.now(),
                    deliveredAt=None,
                    deliveryLocation=shop.location,
                    status=1,  # 1 = Pendiente
                    products_total=shop_total,
                    delivery_fee=1500,  # Cargo fijo por tienda
                    total_amount=shop_total + 1500,
                    deliveryInstructions=instructions,  # Instrucciones de entrega
                    shop_paid=False,
                    deliverer_paid=False,
                )

                # Crear los items de la orden
                for item in data["items"]:
                    product = item.product_listing.listedProduct
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item.quantity,
                        price=product.priceCLP,
                    )

            # Limpiar el carrito
            cart_items.delete()

            if len(tiendas) > 1:
                messages.success(
                    request,
                    f"¡Se han creado {len(tiendas)} órdenes para diferentes tiendas!",
                )
            else:
                messages.success(request, "¡Tu orden ha sido enviada correctamente!")

            return redirect("home")

        except Cart.DoesNotExist:
            messages.error(request, "No se pudo encontrar tu carrito.")
            return redirect("cart")
        except Exception as e:
            messages.error(request, f"Error al procesar la orden: {str(e)}")
            return redirect("cart")
    else:
        return redirect("cart")


# Vista para mostrar notificaciones
@login_required(login_url="/login")
def show_notifications(request):
    notifications = []
    try:
        notifications = Notification.objects.filter(user=request.user).order_by(
            "-created_at"
        )
    except Notification.DoesNotExist:
        print("notification does not exist!")

    context = {"notifications": notifications}
    return render(request, "app_comprador/notification_menu.html", context)


@login_required(login_url="/login")
def delete_notification(request, notification_id):
    print("delete_notification called")
    if request.method == "POST":
        notification = get_object_or_404(
            Notification, id=notification_id, user=request.user
        )
        notification.delete()
        return redirect("show_notifications")


@login_required(login_url="/login")
def rate(request, deliverer_id, shop_id):
    if request.method == "POST":
        rating_deliverer = int(request.POST.get("rating_deliverer"))
        rating_shop = int(request.POST.get("rating_shop"))
        order_id = request.POST.get("order_id")

        if rating_deliverer < 1 or rating_deliverer > 5:
            return
        
        if rating_shop < 1 or rating_shop > 5:
            return

        # objects
        deliverer = get_object_or_404(User, id=deliverer_id)
        order = get_object_or_404(Order, id=order_id)
        shop = get_object_or_404(Shop, shopID=shop_id)

        # update deliverer rating
        sum = deliverer.rating * deliverer.votes
        sum += rating_deliverer
        deliverer.votes += 1
        deliverer.rating = sum / deliverer.votes
        deliverer.save()

        # update shop rating
        sum = shop.rating * shop.votes
        sum += rating_shop
        shop.votes += 1
        shop.rating = sum / shop.votes
        shop.save()

        # mark order as rated
        order.rated = True
        order.save()

        print("new rating: ", deliverer.rating)
        return redirect("/")