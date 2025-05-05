from rest_framework import serializers

from api.models.customer import Customer
from api.services.customer import CustomerService


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation.update({
            'orders_count': CustomerService.get_orders_count(instance)
        })

        return representation
