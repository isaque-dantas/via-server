import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models.order import Order
from api.serializers.customer import CustomerSerializer
from api.serializers.employee import EmployeeSerializer
from api.serializers.product import ProductSerializer
from api.services.customer import CustomerService
from api.services.product import ProductService


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status', 'customer', 'employee', 'products', 'description', 'date']

    products = ProductSerializer(many=True, read_only=True)

    def to_internal_value(self, data):
        # print(f'data in OrderSerializer.to_internal_value: {data}')
        customer = None
        raw_products = data.get('products')
        products_serializers = None

        customer_pk = data.get('customer')
        if customer_pk and CustomerService.exists(customer_pk):
            customer = CustomerService.get(customer_pk)

        if raw_products and isinstance(raw_products, list):
            products_serializers = ProductService.get_serializers_from_raw_products(raw_products)

        return {
            'id': data.get('id'),
            'status': data.get('status'),
            'description': data.get('description'),
            'date': data.get('date'),
            'customer': customer,
            'employee': data.get('employee'),
            'products': products_serializers or raw_products,
        }

    def validate(self, attrs):
        errors = []

        if not attrs.get('customer'):
            errors.append('O campo \'customer\' é obrigatório.')

        if not attrs.get('employee'):
            errors.append('O campo \'employee\' é obrigatório.')

        if not attrs.get('date'):
            errors.append('O campo \'date\' é obrigatório.')
        elif datetime.datetime.strptime(attrs.get('date'), '%Y-%m-%d') > datetime.datetime.now():
            errors.append('A data do pedido deve ser anterior à atual.')

        if not attrs.get('products'):
            errors.append('O campo \'products\' é obrigatório.')
        elif not isinstance(attrs.get('products'), list):
            errors.append('O campo \'products\' deve ser uma lista.')
        else:
            duplicates: list = ProductService.has_duplicates(attrs.get('products'))
            if duplicates:
                duplicates = [str(d) for d in duplicates]
                is_more_than_one_duplicate = len(duplicates) > 1
                errors.append(
                    'Não pode haver produtos duplicados ' +
                    f'(ID{"s" if is_more_than_one_duplicate else ""} ' +
                    f'duplicado{"s" if is_more_than_one_duplicate else ""}: ' +
                    f'{", ".join(duplicates)}).'
                )

        if errors:
            raise ValidationError(errors)

        return attrs

    def to_representation(self, instance):
        # print(f'{instance=}')

        return {
            'id': instance.id,
            'status': instance.status,
            'description': instance.description,
            'date': instance.date,
            'customer': CustomerSerializer(instance.customer).data,
            'employee': EmployeeSerializer(instance.employee).data,
            'products': ProductSerializer(
                instance.products,
                many=True,
                context={'order_id': instance.id}
            ).data,
        }
