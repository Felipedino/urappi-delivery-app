from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST
from urappiapp.models import (
    ProductListing,
    Shop,
    Product,
    ShopOwner
)

@login_required(login_url="/login")
def show_my_store(request):

    # Verificar si es un vendedor
    #if not usuario.is_authenticated or usuario.rol != 'seller':
    #    return HttpResponseForbidden("Solo los vendedores pueden acceder a esto.")

    shop_owner = ShopOwner.objects.filter(owner=request.user).first()
    if not shop_owner:
        print("No tienes una tienda aún.")
    tienda = shop_owner.shop

    productos_listados = ProductListing.objects.filter(listedBy=tienda)
    productos = []
    for pl in productos_listados:
        pathFoto = "/media/" + str(pl.listedProduct.prodImage)
        productos.append(
            {
                "productID": pl.listedProduct.productID,
                "ProductName": pl.listedProduct.productName,
                "priceCLP": pl.listedProduct.priceCLP,
                "description": pl.listedProduct.description,
                "prodImage": pathFoto,
                "stock": pl.stockQuantity,
            }
        )
        print(pl.listedProduct.prodImage)

    info = {
        "tienda_id": tienda.shopID,
        "tienda": tienda,
        "productos": productos,
    }

    return render(request, "app_vendedor/my_store.html", info)

@login_required(login_url="/login")
@require_POST
def addNewProduct(request):
    if request.method== "POST":
        shop_owner = ShopOwner.objects.filter(owner=request.user).first()
        shop = shop_owner.shop

        producto = request.POST["nombre_producto"]
        precio = request.POST["valor_producto"]
        descripcion = request.POST["descr_producto"]
        foto = request.FILES.get('foto_producto', None)
        categoria = request.POST["tipo_prod"]
        stock = request.POST["stock_producto"]

        precioInt = precio.replace('$', '').replace('.', '').strip()
        

        product = Product.objects.create(productName=producto,
                               category=categoria,
                               description=descripcion,
                               prodImage=foto,
                               priceCLP=precioInt,)
        
        
        listing = ProductListing(
            listedBy=shop,
            listedProduct=product,
            stockQuantity=int(stock)
        )
        listing.save()
        
        return redirect("app_vendedor:show_my_store")
        

@login_required(login_url="/login")
@require_POST
def editProduct(request, productID):
    if request.method== "POST":
        print("modificar el producto", productID)
        shop_owner = ShopOwner.objects.filter(owner=request.user).first()
        tienda = shop_owner.shop
        productos_listados = ProductListing.objects.filter(listedBy=tienda)
        producto_listado = productos_listados.filter(listedProduct__productID=productID).first()

        producto = producto_listado.listedProduct

        productoNom = request.POST["nombre_producto_" + str(productID)]
        precioStr = request.POST["valor_producto_" + str(productID)]
        precio = precioStr.replace('$', '').replace('.', '').strip()
        descripcion = request.POST["descr_producto_" + str(productID)]
        stock = request.POST["stock_producto_" + str(productID)]
        
        producto.productName = productoNom
        producto.priceCLP = precio
        producto.description = descripcion
        producto_listado.stockQuantity = stock

        producto.save()
        producto_listado.save()

    return redirect("app_vendedor:show_my_store")
        