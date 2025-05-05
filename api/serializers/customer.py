from rest_framework import serializers

from api.models.customer import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if getattr(instance, 'orders_count', None):
            representation.update({'orders_count': instance.orders_count})

        return representation
