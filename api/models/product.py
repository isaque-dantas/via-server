from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    description = models.CharField(max_length=256, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)

    objects = models.Manager()
