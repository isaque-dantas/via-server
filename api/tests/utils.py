from rest_framework.test import APIClient

from api import BASE_URL
from api.models import Employee
from api.models.customer import Customer
from api.models.order import Order
from api.models.product import Product
from api.serializers.order import OrderSerializer
from api.services.order import OrderService


class Utils:
    employee_data = {
        'email': 'vendedor@email.com',
        'password': 'pass',
        'name': 'Usuário Vendedor'
    }

    customer_data = {
        'email': 'cliente@email.com',
        'name': 'Cliente Genérico'
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

    @classmethod
    def add_example_data(cls):
        if Employee.objects.filter(email=cls.employee_data['email']).exists():
            e = Employee.objects.get(email=cls.employee_data['email'])
        else:
            e = Employee.objects.create_user(**cls.employee_data)

        # --- --- --- PRODUTOS --- --- --- #

        Product.objects.all().delete()

        cosmetico = Product.objects.create(**cls.product_data)

        abacates = Product.objects.create(
            name='Abacates do Francisco',
            description='Abacates fresquinhos da horta do Francisco, sem agrotóxicos!',
            price=20.75,
        )

        sapv = Product.objects.create(
            name='Motor de cálculo do SAPV',
            description='API em F# com mais de 200 testes automatizados.',
            price=100000,
        )

        coca_cola = Product.objects.create(
            name='Coca-Cola',
            description='Você já sabe.',
            price=4.50,
        )

        # --- --- --- CLIENTES --- --- --- #

        Customer.objects.all().delete()

        eletrobras = Customer.objects.create(
            email='eletrobras@email.com',
            name='Eletrobras'
        )

        logap = Customer.objects.create(
            email='logap@email.com',
            name='LogAp Sistemas'
        )

        # --- --- --- PEDIDOS --- --- --- #
        Order.objects.all().delete()

        serializer = OrderSerializer(data={
            'employee': e,
            'customer': logap.id,
            'date': '2020-01-01',
            'description': 'Almoço dos funcionários.',
            'products': [{'id': abacates.id, 'quantity': 1500}, {'id': coca_cola.id, 'quantity': 750}]
        })
        serializer.is_valid()
        print(serializer.errors)
        OrderService.create(serializer.validated_data)

        serializer = OrderSerializer(data={
            'employee': e,
            'customer': eletrobras.id,
            'date': '2020-01-01',
            'products': [{'id': sapv.id, 'quantity': 1}]
        })
        serializer.is_valid()
        OrderService.create(serializer.validated_data)

        serializer = OrderSerializer(data={
            'employee': e,
            'customer': eletrobras.id,
            'date': '2020-01-01',
            'products': [
                {'id': cosmetico.id, 'quantity': 34},
                {'id': abacates.id, 'quantity': 3000},
                {'id': coca_cola.id, 'quantity': 4052}
            ]
        })
        serializer.is_valid()
        OrderService.create(serializer.validated_data)
