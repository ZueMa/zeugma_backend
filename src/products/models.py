from django.db import models

class Product(models.Model):
    seller = models.ForeignKey(
        'sellers.Seller',
        models.SET_NULL,
        null=True
    )
    name = models.CharField(max_length=128)
    category = models.CharField(max_length=32)
    price = models.FloatField()
    num_stocks = models.IntegerField()
    short_description = models.TextField()
    full_description = models.TextField()
    is_confirmed = models.BooleanField(default=False)
    image = models.URLField(
        null=True,
        blank=True
    )
