from django.db import models

class Seller(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=16)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    company_name = models.CharField(max_length=32)
    address = models.TextField()
    description = models.TextField()

class Order(models.Model):
    seller = models.ForeignKey('Seller')
    product = models.ForeignKey('products.Product')
    num_items = models.IntegerField()
    revenue = models.FloatField()
    timestamp = models.DateField(auto_now_add=True)
