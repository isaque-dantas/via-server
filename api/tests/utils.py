from rest_framework.test import APIClient

from api import BASE_URL
from api.models import Employee
from api.models.customer import Customer


class Utils:
    employee_data = {
        'email': 'vendedor@email.com',
        'password': 'pass',
        'name': 'Usuário Vendedor'
    }

    customer_data = {
        'email': 'cliente@email.com',
        'name': 'Usuário Cliente'
    }

    product_data = {
        "name": "Caro cosmético",
        "description": 'Descrição do caro cosmético',
        "price": 100,
    }

    @classmethod
    def get_headers_for_user(cls):
        client = APIClient()

        if not Employee.objects.exists():
            Employee.objects.create_user(**cls.employee_data)

        response = client.post(
            BASE_URL + 'token',
            data={
                'email': cls.employee_data['email'],
                'password': cls.employee_data['password']
            }
        )

        return {'Authorization': f'Bearer {response.data["access"]}'}

    @classmethod
    def create_default_employee_and_customer(cls):
        employee = Employee.objects.create_user(**cls.employee_data)
        customer = Customer.objects.create(**cls.customer_data)

        return employee, customer
