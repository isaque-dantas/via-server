from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)

    objects = models.Manager()
