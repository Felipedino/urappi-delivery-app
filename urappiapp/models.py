from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    pronombres = [('La','La'),('El','El'), ('Le','Le'),('Otro','Otro')]
    pronombre = models.CharField(max_length=5,choices=pronombres)
    apodo = models.CharField(max_length=30)

class Shop(models.Model):
    shopID = models.IntegerField()
    shopDescription = models.TextField()
    openTime = models.TimeField()
    closingTime = models.TimeField()
    shopName = models.CharField(max_length = 32)
    imageURL = models.URLField()
    location = models.TextField()
    def __str__(self):
        return self.shopName

class Product(models.Model):
    productID = models.IntegerField()
    productName = models.CharField(max_length = 32)
    category = models.CharField(max_length = 32)
    description = models.TextField()
    imageURL = models.URLField()
    priceCLP = models.IntegerField()
    def __str__(self):
        return self.productName + str(self.productID)


class ProductListing(models.Model):
    listedBy = models.ForeignKey(Shop, on_delete=models.CASCADE)
    listedProduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    stockQuantity = models.IntegerField()
    def __str__(self):
        return str(self.listedBy) + " " + str(self.listedProduct)

class Order(models.Model):
    orderID = models.IntegerField()
    createdAt = models.DateField()
    deliveredAt = models.DateField()
    status = models.IntegerField()

class Delivery(models.Model):
    deliveryRating = models.FloatField()
    notes = models.TextField()
    status = models.IntegerField()


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Carrito de {self.user.apodo}'

    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def total_price(self):
        return sum(item.quantity * item.product_listing.listedProduct.priceCLP for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE,
        related_name='items'
    )
    product_listing = models.ForeignKey(
        'ProductListing', on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product_listing')

    def __str__(self):
        return f'{self.quantity} x {self.product_listing.listedProduct.productName}'
