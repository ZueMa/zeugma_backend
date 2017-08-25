from django.db import models
from sellers.models import Seller

def upload_location(instance, filename):
    return 'products/images/%s/%s' %(instance.name, filename)

class Product(models.Model):
    name = models.CharField(max_length=32)
    category = models.CharField(max_length=16)
    price = models.FloatField()
    num_stocks = models.IntegerField()
    short_description = models.TextField()
    full_description = models.TextField()
    image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True
    )
    seller = models.ForeignKey(
        Seller,
        models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.name
