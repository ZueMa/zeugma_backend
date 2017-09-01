from django.db import models

class Seller(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=16)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    company_name = models.CharField(max_length=32)
    address = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.username

class Order(models.Model):
    product = models.ForeignKey('products.Product')
    seller = models.ForeignKey(Seller)
    num_items = models.IntegerField()
    revenue = models.FloatField()
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'Order #{}'.format(self.id)
