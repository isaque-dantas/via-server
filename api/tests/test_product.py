from rest_framework import status
from rest_framework.test import APITestCase

from api import BASE_URL
from api.serializers.product import ProductSerializer
from api.services.product import ProductService
from api.tests.utils import Utils

class ProductTestCase(APITestCase):

    def test_post__on_happy_path__should_return_CREATED(self):
        response = self.client.post(
            BASE_URL + 'product',
            Utils.product_data,
            headers=Utils.get_headers_for_user()
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_many__on_happy_path__should_return_OK(self):
        ProductService.create(Utils.product_data)

        response = self.client.get(
            BASE_URL + 'product',
            headers=Utils.get_headers_for_user()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single__on_happy_path__should_return_OK(self):
        product_id = ProductService.create(Utils.product_data).id

        response = self.client.get(
            BASE_URL + f'product/{product_id}',
            headers=Utils.get_headers_for_user()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put__on_happy_path__should_return_NO_CONTENT(self):
        product = ProductService.create(Utils.product_data)

        edited = Utils.product_data.copy()
        edited['name'] = 'Edited name'

        response = self.client.put(
            BASE_URL + f'product/{product.id}',
            edited,
            headers=Utils.get_headers_for_user()
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ProductService.get(product.id).name, edited['name'])

    def test_delete__on_happy_path__should_return_NO_CONTENT(self):
        product_id = ProductService.create(Utils.product_data).id

        response = self.client.delete(
            BASE_URL + f'product/{product_id}',
            headers=Utils.get_headers_for_user()
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProductSerializerTestCase(APITestCase):

    def test_validate__without_description__should_return_VALID(self):
        product_data_copy = Utils.product_data.copy()
        product_data_copy.pop('description')

        serializer = ProductSerializer(data=product_data_copy)
        self.assertTrue(serializer.is_valid())

    def test_validate__without_quantity_in_ordering__should_return_INVALID(self):
        product_data_copy = Utils.product_data.copy()
        product_data_copy.pop('description')

        serializer = ProductSerializer(data=product_data_copy, context={'is_ordering': True})
        self.assertFalse(serializer.is_valid())
