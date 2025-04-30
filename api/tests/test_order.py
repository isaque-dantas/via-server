from rest_framework import status
from rest_framework.test import APITestCase

from api import BASE_URL
from api.models.customer import Customer
from api.models.order import Order
from api.models.product import Product
from api.serializers.order import OrderSerializer
from api.services.order import OrderService
from api.tests.utils import Utils


class OrderTestCase(APITestCase):

    def test_post__on_happy_path__should_return_CREATED(self):
        product_1 = Product.objects.create(**Utils.product_data)
        product_2 = Product.objects.create(**Utils.product_data)

        employee, customer = Utils.create_default_employee_and_customer()
        order_data = {
            'customer': customer.id,
            'products': [{'id': product_1.id, 'quantity': 2}, {'id': product_2.id, 'quantity': 3}]
        }

        response = self.client.post(
            BASE_URL + 'order',
            order_data,
            headers=Utils.get_headers_for_user(),
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_many__on_happy_path__should_return_OK(self):
        employee, customer = Utils.create_default_employee_and_customer()
        order_data = {"employee": employee, "customer": customer}
        Order.objects.create(**order_data)

        response = self.client.get(
            BASE_URL + 'order',
            headers=Utils.get_headers_for_user()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single__on_happy_path__should_return_OK(self):
        employee, customer = Utils.create_default_employee_and_customer()
        order_data = {"employee": employee, "customer": customer}

        order_id = Order.objects.create(**order_data).id

        response = self.client.get(
            BASE_URL + f'order/{order_id}',
            headers=Utils.get_headers_for_user()
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put__on_happy_path__should_return_NO_CONTENT(self):
        product_1 = Product.objects.create(**Utils.product_data)
        product_2 = Product.objects.create(**Utils.product_data)

        employee, customer = Utils.create_default_employee_and_customer()
        order_data = {
            'employee': employee,
            'customer': customer.id,
            'products': [{'id': product_1.id, 'quantity': 2}, {'id': product_2.id, 'quantity': 3}]
        }

        serializer = OrderSerializer(data=order_data)
        serializer.is_valid()
        order_id = OrderService.create(serializer.validated_data).id

        another_costumer = Customer.objects.create(name="Another Customer", email="another@email.com")
        order_data['customer'] = another_costumer.id
        order_data['employee'] = order_data['employee'].id

        response = self.client.put(
            BASE_URL + f'order/{order_id}',
            order_data,
            headers=Utils.get_headers_for_user(),
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete__on_happy_path__should_return_NO_CONTENT(self):
        employee, customer = Utils.create_default_employee_and_customer()
        order_data = {"employee": employee, "customer": customer}

        order_id = Order.objects.create(**order_data).id

        response = self.client.delete(
            BASE_URL + f'order/{order_id}',
            headers=Utils.get_headers_for_user()
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OrderSerializerTestCase(APITestCase):

    def test_validate__without_customer__should_return_INVALID(self):
        product_1 = Product.objects.create(**Utils.product_data)
        product_2 = Product.objects.create(**Utils.product_data)

        employee, _ = Utils.create_default_employee_and_customer()
        order_data = {
            'employee': employee,
            'products': [{'id': product_1.id, 'quantity': 2}, {'id': product_2.id, 'quantity': 3}]
        }

        serializer = OrderSerializer(data=order_data)
        self.assertFalse(serializer.is_valid())

    def test_validate__without_products__should_return_INVALID(self):
        employee, customer = Utils.create_default_employee_and_customer()
        order_data = {
            'employee': employee,
            'customer': customer.id,
            'products': []
        }

        serializer = OrderSerializer(data=order_data)
        self.assertFalse(serializer.is_valid())

    def test_validate__product_without_id__should_return_INVALID(self):
        employee, customer = Utils.create_default_employee_and_customer()
        order_data = {
            'employee': employee,
            'customer': customer.id,
            'products': [{'quantity': 2}]
        }

        serializer = OrderSerializer(data=order_data)
        self.assertFalse(serializer.is_valid())
