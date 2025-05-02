from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models.order import Order
from api.serializers.customer import CustomerSerializer
from api.serializers.employee import EmployeeSerializer
from api.serializers.product import ProductSerializer
from api.services.customer import CustomerService
from api.services.employee import EmployeeService
from api.services.product import ProductService


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status', 'customer', 'employee', 'products', 'description']

    products = ProductSerializer(many=True, read_only=True)

    def to_internal_value(self, data):
        # print(f'data in OrderSerializer.to_internal_value: {data}')
        customer = None

        customer_pk = data.get('customer')
        if customer_pk and CustomerService.exists(customer_pk):
            customer = CustomerService.get(customer_pk)

        if not data.get('products'):
            raise ValidationError('O campo \'products\' é obrigatório.')

        if not isinstance(data.get('products'), list):
            raise ValidationError('O campo \'products\' deve ser uma lista.')

        products = ProductService.get_serializers_from_raw_products(data['products'])

        return {
            'id': data.get('id'),
            'status': data.get('status'),
            'description': data.get('description'),
            'customer': customer,
            'employee': data.get('employee'),
            'products': products,
        }

    def validate(self, attrs):
        errors = []

        if not attrs.get('customer'):
            errors.append('O cliente é uma informação obrigatória')

        if not attrs.get('employee'):
            errors.append('O vendedor que cadastrou o pedido é uma informação obrigatória')

        if errors:
            raise ValidationError(errors)

        return attrs

    def to_representation(self, instance):
        # print(f'{instance=}')

        return {
            'id': instance.id,
            'status': instance.status,
            'customer': CustomerSerializer(instance.customer).data,
            'employee': EmployeeSerializer(instance.employee).data,
            'products': ProductSerializer(instance.products, many=True).data,
        }
