from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pronombres = [('La','La'),('El','El'), ('Le','Le'),('Otro','Otro')]
    pronombre = models.CharField(max_length=5,choices=pronombres)
    apodo = models.CharField(max_length=30)

class Deliverer(User):
    pass

class Customer(User):
    pass

class Shop(models.Model):
    shopID = models.IntegerField()
    shopDescription = models.TextField()
    isOpen = models.BooleanField()
    shopName = models.CharField(max_length = 32)
    imageURL = models.URLField()

class Product(models.Model):
    productID = models.IntegerField()
    productName = models.CharField(max_length = 32)
    category = models.CharField(max_length = 32)
    description = models.TextField()
    imageURL = models.URLField()
    priceCLP = models.IntegerField()

class ProductListing(models.Model):
    listedBy = models.ForeignKey(Shop, on_delete=models.CASCADE)
    listedProduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    stockQuantity = models.IntegerField()

class Order(models.Model):
    orderID = models.IntegerField()
    createdAt = models.DateField()
    deliveredAt = models.DateField()
    status = models.IntegerField()

class Delivery(models.Model):
    deliveryRating = models.FloatField()
    notes = models.TextField()
    status = models.IntegerField()