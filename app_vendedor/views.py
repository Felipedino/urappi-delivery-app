from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from urappiapp.models import Product, ProductListing, Shop, ShopOwner

# Vista para mostrar la información de la tienda del usuario logeado
@login_required(login_url="/login")
def show_my_store(request):

    shop_owner = ShopOwner.objects.filter(owner=request.user).first()
    if not shop_owner:
        print("No tienes una tienda aún.")
    tienda = shop_owner.shop

    productos_listados = ProductListing.objects.filter(listedBy=tienda)
    productos = []
    for pl in productos_listados:
        productos.append(
            {
                "productID": pl.listedProduct.productID,
                "ProductName": pl.listedProduct.productName,
                "priceCLP": pl.listedProduct.priceCLP,
                "description": pl.listedProduct.description,
                "prodImage": pl.listedProduct.prodImage,
                "stock": pl.stockQuantity,
            }
        )

    info = {
        "usuario": request.user,
        "tienda_id": tienda.shopID,
        "tienda": tienda,
        "productos": productos,
    }

    return render(request, "app_vendedor/my_store.html", info)


# Lógica para agregar un producto nuevo a la tienda
@login_required(login_url="/login")
@require_POST
def addNewProduct(request):
    if request.method == "POST":
        shop_owner = ShopOwner.objects.filter(owner=request.user).first() # busca la tienda acorde al usuario registrado
        shop = shop_owner.shop

        producto = request.POST["nombre_producto"]
        precio = request.POST["valor_producto"]
        descripcion = request.POST["descr_producto"]
        foto = request.FILES.get("foto_producto", None)
        categoria = request.POST["tipo_prod"]
        stock = request.POST["stock_producto"]

        precioInt = precio.replace("$", "").replace(".", "").strip()

        product = Product.objects.create(
            productName=producto,
            category=categoria,
            description=descripcion,
            prodImage=foto,
            priceCLP=precioInt,
        )

        listing = ProductListing(
            listedBy=shop, listedProduct=product, stockQuantity=int(stock)
        )
        listing.save()

        return redirect("app_vendedor:show_my_store")


# Lógica para modificar un producto que ya está registrado
# Se puede modificar el nombre, precio, descripción y stock
@login_required(login_url="/login")
@require_POST
def editProduct(request, productID):
    if request.method == "POST":
        shop_owner = ShopOwner.objects.filter(owner=request.user).first()
        tienda = shop_owner.shop
        productos_listados = ProductListing.objects.filter(listedBy=tienda)
        producto_listado = productos_listados.filter(
            listedProduct__productID=productID
        ).first()

        producto = producto_listado.listedProduct

        productoNom = request.POST["nombre_producto_" + str(productID)]
        precioStr = request.POST["valor_producto_" + str(productID)]
        precio = precioStr.replace("$", "").replace(".", "").strip()
        descripcion = request.POST["descr_producto_" + str(productID)]
        stock = request.POST["stock_producto_" + str(productID)]

        producto.productName = productoNom
        producto.priceCLP = precio
        producto.description = descripcion
        producto_listado.stockQuantity = stock

        producto.save()
        producto_listado.save()

    return redirect("app_vendedor:show_my_store")


# Lógica para editar la información de la tienda
# Solo se permite editar la ubicación, horario de apertura y cierre y descripción
def editStore(request):
    if request.method == "POST":
        shop_owner = ShopOwner.objects.filter(owner=request.user).first()
        tienda = shop_owner.shop

        tienda.shopDescription = request.POST["descr_tienda"]
        tienda.location = request.POST["ubic_tienda"]
        tienda.openTime = request.POST["hora_apertura"]
        tienda.closingTime = request.POST["hora_cierre"]
        tienda.save()

    return redirect("app_vendedor:show_my_store")
