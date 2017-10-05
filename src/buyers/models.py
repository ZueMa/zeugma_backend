from django.db import models

class Buyer(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=32)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    address = models.TextField()

class Cart(models.Model):
    buyer = models.ForeignKey('Buyer')
    is_purchased = models.BooleanField(default=False)
    items = models.ManyToManyField(
        'products.Product',
        through='ProductCart',
        through_fields=('cart', 'product')
    )

class ProductCart(models.Model):
    product = models.ForeignKey('products.Product')
    cart = models.ForeignKey('Cart')
    num_items = models.IntegerField(default=1)

class Purchase(models.Model):
    buyer = models.ForeignKey('Buyer')
    cart = models.ForeignKey('Cart')
    is_shipped = models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)
