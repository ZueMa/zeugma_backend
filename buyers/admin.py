from django.contrib import admin
from .models import Buyer, Cart, ProductCart

admin.site.register(Buyer)
admin.site.register(Cart)
admin.site.register(ProductCart)
