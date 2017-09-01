from django.db import models
from products.models import Product

class Buyer(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=16)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    address = models.TextField()

    def __str__(self):
        return self.username

class Cart(models.Model):
    is_purchased = models.BooleanField(default=False)
    buyer = models.ForeignKey(Buyer)
    items = models.ManyToManyField(
        Product,
        through='ProductCart',
        through_fields=('cart', 'product')
    )

    def __str__(self):
        return 'Cart #{}'.format(self.id)

class ProductCart(models.Model):
    num_items = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart)
    product = models.ForeignKey(Product)

    def __str__(self):
        return 'Product #{} in Cart #{}'.format(self.product.id, self.cart.id)

class Purchase(models.Model):
    cart = models.ForeignKey(Cart)
    buyer = models.ForeignKey(Buyer)
    is_shipped = models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'Purchase #{}'.format(self.id)
