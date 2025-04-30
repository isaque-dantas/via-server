from rest_framework.exceptions import ValidationError

from api.models.product import Product
from api.serializers.product import ProductSerializer


class ProductService:
    @staticmethod
    def create(product_data):
        product = Product(
            name=product_data['name'],
            description=product_data.get('description'),
            price=product_data['price']
        )
        product.save()

        return product

    @classmethod
    def get(cls, pk):
        return Product.objects.get(pk=pk)

    @staticmethod
    def get_all():
        return Product.objects.all()

    @classmethod
    def exists(cls, pk):
        return Product.objects.filter(pk=pk).exists()

    @staticmethod
    def update(new_product_data: dict, product: Product):
        name = new_product_data.get('name')
        if name:
            product.name = name

        description = new_product_data.get('description')
        if description:
            product.description = description

        price = new_product_data.get('price')
        if price:
            product.price = price

        product.save()

    @classmethod
    def delete(cls, pk):
        Product.objects.filter(pk=pk).delete()

    @classmethod
    def get_serializers_from_raw_products(cls, raw_products: list[dict]):
        errors = cls.get_errors_from_raw_products(raw_products)
        if errors:
            raise ValidationError(errors)

        return [
            ProductSerializer(
                instance=cls.get(p['id']),
                data={'quantity': p['quantity']}
            )

            for p in raw_products
        ]

    @classmethod
    def get_errors_from_raw_products(cls, raw_products: list[dict]):
        errors = {}
        for i, p in enumerate(raw_products):
            errors.update({i: {}})

            if not p.get('id'):
                errors[i]['id'] = 'Este campo é obrigatório'
            elif not cls.exists(p['id']):
                errors[i]['id'] = f'O produto de id \'{i}\' não existe'

            if not p.get('quantity'):
                errors[i]['quantity'] = 'Este campo é obrigatório'

        errors = {
            key: value

            for key, value in errors.items()
            if value != {}
        }

        return errors
