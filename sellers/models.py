from django.db import models

class Seller(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=16)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    company_name = models.CharField(max_length=32)
    address = models.TextField()
    description = models.TextField()
    
    def __str__ (self):
        return self.username
        