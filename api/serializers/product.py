from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models.product import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity']

    quantity = serializers.IntegerField(allow_null=True)

    def to_internal_value(self, data):
        return {
            'id': data.get('id'),
            'name': data.get('name'),
            'description': data.get('description'),
            'price': data.get('price'),
            'quantity': data.get('quantity'),
        }

    def validate(self, attrs):
        if (
                not attrs.get('quantity')
                and
                self.context.get('is_ordering')
        ):
            raise ValidationError('A quantidade do produto deve ser informada.')

        return attrs
