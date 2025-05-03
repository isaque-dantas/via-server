from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models.product import Product
from api.services.order import OrderService


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
        errors = []

        if (
                not attrs.get('quantity')
                and
                self.context.get('is_ordering')
        ):
            errors.append('A quantidade deve ser informada.')

        if not attrs.get('price'):
            errors.append('O preço deve ser informado.')
        else:
            try:
                attrs['price'] = float(attrs['price'])
            except ValueError:
                errors.append('O preço deve ser um número.')

        if errors:
            raise ValidationError(errors)

        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        order_id = self.context.get('order_id')
        if order_id:
            quantity = OrderService.get_quantity(
                product_id=instance.id,
                order_id=order_id
            )

            representation.update({"quantity": quantity})
            representation.update({"total_cost": round(quantity * instance.price, 2)})

        return representation
