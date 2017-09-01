from django.db import models

class Buyer(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=16)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    address = models.TextField()

    def __str__(self):
        return 'Buyer #{}'.format(self.id)
class Cart(models.Model):
    buyer = models.ForeignKey('Buyer')
    is_purchased = models.BooleanField(default=False)
    items = models.ManyToManyField(
        'products.Product',
        through='ProductCart',
        through_fields=('cart', 'product')
    )

    def __str__(self):
        return 'Cart #{}'.format(self.id)

class ProductCart(models.Model):
    product = models.ForeignKey('products.Product')
    cart = models.ForeignKey('Cart')
    num_items = models.IntegerField(default=1)

    def __str__(self):
        return 'ProductCart #{}'.format(self.id)

class Purchase(models.Model):
    buyer = models.ForeignKey('Buyer')
    cart = models.ForeignKey('Cart')
    is_shipped = models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'Purchase #{}'.format(self.id)
