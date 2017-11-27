from django.db import models

class Admin(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=32)
