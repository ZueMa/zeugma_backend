from django.db import models

class Product(models.Model):
    seller = models.ForeignKey(
        'sellers.Seller',
        models.SET_NULL,
        null=True
    )
    name = models.CharField(max_length=32)
    category = models.CharField(max_length=16)
    price = models.FloatField()
    num_stocks = models.IntegerField()
    short_description = models.TextField()
    full_description = models.TextField()
    image = models.URLField(
        null=True,
        blank=True
    )
