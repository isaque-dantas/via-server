from django.db import models

from api.models import Employee
from api.models.customer import Customer
from api.models.product import Product


class Order(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'Em andamento'
        DONE = 'Finalizado'
        CANCELLED = 'Cancelado'

    status = models.CharField(max_length=128, choices=Status.choices, default=Status.IN_PROGRESS)
    description = models.CharField(max_length=256, blank=True, null=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct')

    objects = models.Manager()

class OrderProduct(models.Model):
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    objects = models.Manager()
