from django.db.models import Count

from api.models.customer import Customer
from api.models.order import Order


class CustomerService:
    @staticmethod
    def create(customer_data: dict):
        customer = Customer(
            name=customer_data['name'],
            email=customer_data['email'],
        )
        customer.save()

        return customer

    @staticmethod
    def get(pk: int) -> Customer:
        return Customer.objects.get(pk=pk)

    @staticmethod
    def get_all():
        return Customer.objects.all()

    @staticmethod
    def exists(pk: int) -> bool:
        return Customer.objects.filter(pk=pk).exists()

    @staticmethod
    def update(customer_data: dict, customer: Customer):
        name = customer_data.get('name')
        if name:
            customer.name = name

        email = customer_data.get('email')
        if email:
            customer.email = email

        customer.save()

    @staticmethod
    def delete(pk: int):
        Customer.objects.filter(pk=pk).delete()

    @classmethod
    def get_orders_count(cls, customer: Customer):
        return (
            Order.objects
            .filter(customer=customer)
            .aggregate(orders_count=Count('id'))
        )['orders_count']
