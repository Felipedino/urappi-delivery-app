from django.contrib import admin

# Register your models here.
from urappiapp.models import *
 
admin.site.register(User)
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(ProductListing)
admin.site.register(Order)
admin.site.register(Delivery)