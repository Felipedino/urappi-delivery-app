from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


# Modelo de usuario personalizado, extiende AbstractUser para agregar campos extra
class User(AbstractUser):
    # Opciones de pronombres para el usuario
    pronombres = [("La", "La"), ("El", "El"), ("Le", "Le"), ("Otro", "Otro")]
    pronombre = models.CharField(max_length=5, choices=pronombres)
    apodo = models.CharField(max_length=30)  # Apodo o nombre visible

    rol = models.CharField(max_length=20, choices=[
        ('customer', 'Cliente'),
        ('deliver', 'Repartidor'),
        ('seller', 'Vendedor'),
    ])
    upuntos = models.IntegerField(default=0)

# Modelo que representa una tienda
class Shop(models.Model):
    shopID = models.AutoField(primary_key=True)  # ID único de la tienda
    shopDescription = models.TextField()  # Descripción de la tienda
    openTime = models.TimeField()  # Hora de apertura
    closingTime = models.TimeField()  # Hora de cierre
    shopName = models.CharField(max_length=32)  # Nombre de la tienda
    shopImage = models.ImageField(upload_to="stores/", null=True, blank=True)  # Imagen de la tienda
    location = models.TextField()  # Ubicación de la tienda
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.shopName

# Relación entre tiendas y sus dueños
class ShopOwner(models.Model):
    owner = models.ForeignKey( User, on_delete=models.CASCADE)  # Usuario dueño de la tienda
    shop = models.ForeignKey( Shop, on_delete=models.CASCADE ) 


# Modelo que representa un producto
class Product(models.Model):
    categorys = [("beb-cal", "Bebidas calientes"), ("beb-fria", "Bebidas frías"), ("pas-boll", "Pastelería y Bollería"), ("sandw", "Sandwiches"), ("otro", "Otro")]
    productID = models.AutoField(primary_key=True)
    productName = models.CharField(max_length=32)  # Nombre del producto
    category = models.CharField(max_length=32, choices=categorys)  # Categoría del producto
    description = models.TextField()  # Descripción del producto
    prodImage = models.ImageField(upload_to="products/", null=True, blank=True)  # Imagen del producto
    priceCLP = models.IntegerField()  # Precio en CLP

    def __str__(self):
        return self.productName + str(self.productID)


# Relación entre productos y tiendas (stock)
class ProductListing(models.Model):
    listedBy = models.ForeignKey(
        Shop, on_delete=models.CASCADE
    )  # Tienda que lista el producto
    listedProduct = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )  # Producto listado
    stockQuantity = models.IntegerField()  # Cantidad en stock

    def __str__(self):
        return str(self.listedBy) + " " + str(self.listedProduct)


# Modelo de orden de compra
class Order(models.Model):
    customer = models.ForeignKey(  # Cliente que hace el pedido
        User, on_delete=models.CASCADE, related_name="customer"
    )
    deliverer = models.ForeignKey(  # Repartidor que entrega el pedido
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="deliverer"
    )
    shop = models.ForeignKey(  # Tienda desde donde se pide el producto
        Shop, on_delete=models.CASCADE
    )
    orderID = models.IntegerField(blank=True, null=True)
    createdAt = models.DateTimeField()  # Fecha de creación
    deliveredAt = models.DateTimeField(null=True)  # Fecha de entrega
    deliveryLocation = models.TextField()
    status = models.IntegerField()  # Estado de la orden (puede ser un enum)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()  # Precio al momento de la compra


# Modelo de entrega (delivery)
class Delivery(models.Model):
    deliveryRating = models.FloatField()  # Calificación de la entrega
    notes = models.TextField()  # Notas adicionales
    status = models.IntegerField()  # Estado de la entrega (puede ser un enum)


# Modelo del carrito
class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.user.apodo}"

    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def total_price(self):
        return sum(
            item.quantity * item.product_listing.listedProduct.priceCLP
            for item in self.items.all()
        )


# Modelo para el contenido del carrito
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product_listing = models.ForeignKey(
        "ProductListing", on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product_listing")

    def __str__(self):
        return f"{self.quantity} x {self.product_listing.listedProduct.productName}"

class Notification(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notification"
    )
    message = models.TextField()
    type = [("entregado", "Pedido entregado"), ("cancelado", "Pedido cancelado"), ("aceptado", "Pedido aceptado")]
    status = models.CharField(max_length=20, default="unread")
    created_at = models.TimeField(null=True)