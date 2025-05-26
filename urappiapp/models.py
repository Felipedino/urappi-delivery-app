from django.contrib.auth.models import AbstractUser
from django.db import models


# Modelo de usuario personalizado, extiende AbstractUser para agregar campos extra
class User(AbstractUser):
    # Opciones de pronombres para el usuario
    pronombres = [("La", "La"), ("El", "El"), ("Le", "Le"), ("Otro", "Otro")]
    pronombre = models.CharField(max_length=5, choices=pronombres)
    apodo = models.CharField(max_length=30)  # Apodo o nombre visible


# Modelo que representa una tienda
class Shop(models.Model):
    shopID = models.IntegerField()  # ID único de la tienda
    shopDescription = models.TextField()  # Descripción de la tienda
    openTime = models.TimeField()  # Hora de apertura
    closingTime = models.TimeField()  # Hora de cierre
    shopName = models.CharField(max_length=32)  # Nombre de la tienda
    imageURL = models.URLField()  # Imagen de la tienda
    location = models.TextField()  # Ubicación de la tienda

    def __str__(self):
        return self.shopName


# Modelo que representa un producto
class Product(models.Model):
    productID = models.IntegerField()  # ID único del producto
    productName = models.CharField(max_length=32)  # Nombre del producto
    category = models.CharField(max_length=32)  # Categoría del producto
    description = models.TextField()  # Descripción del producto
    imageURL = models.URLField()  # Imagen del producto
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
    orderID = models.IntegerField()  # ID único de la orden
    createdAt = models.DateField()  # Fecha de creación
    deliveredAt = models.DateField()  # Fecha de entrega
    status = models.IntegerField()  # Estado de la orden (puede ser un enum)


# Modelo de entrega (delivery)
class Delivery(models.Model):
    deliveryRating = models.FloatField()  # Calificación de la entrega
    notes = models.TextField()  # Notas adicionales
    status = models.IntegerField()  # Estado de la entrega (puede ser un enum)
