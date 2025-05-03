import json

from rest_framework import status
from rest_framework.test import APITestCase

from api import BASE_URL
from api.models.customer import Customer
from api.models.order import Order, OrderProduct
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
            'date': '2020-01-01',
            'customer': customer.id,
            'products': [{'id': product_1.id, 'quantity': 2}, {'id': product_2.id, 'quantity': 3}],
            'description': 'Descrição do pedido!'
        }

        response = self.client.post(
            BASE_URL + 'order',
            order_data,
            headers=Utils.get_headers_for_user(),
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(json.dumps(response.data, indent=4))

    def test_get_many__on_happy_path__should_return_OK(self):
        employee, customer = Utils.create_default_employee_and_customer()
        order_data = {
            'date': '2020-01-01', "employee": employee, "customer": customer}
        Order.objects.create(**order_data)

        response = self.client.get(
            BASE_URL + 'order',
            headers=Utils.get_headers_for_user()
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single__on_happy_path__should_return_OK(self):
        employee, customer = Utils.create_default_employee_and_customer()
        order_data = {
            'date': '2020-01-01', "employee": employee, "customer": customer}

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
            'date': '2020-01-01',
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

    def test_put__products_edited__should_return_NO_CONTENT(self):
        product_1 = Product.objects.create(**Utils.product_data)
        product_2 = Product.objects.create(**Utils.product_data)
        product_3 = Product.objects.create(**Utils.product_data)

        employee, customer = Utils.create_default_employee_and_customer()
        order_data = {
            'date': '2020-01-01',
            'employee': employee,
            'customer': customer.id,
            'products': [{'id': product_1.id, 'quantity': 2}, {'id': product_2.id, 'quantity': 3}]
        }

        serializer = OrderSerializer(data=order_data)
        serializer.is_valid()
        order_id = OrderService.create(serializer.validated_data).id

        edited_quantity = 1000
        order_data = {
            'date': '2020-01-01',
            'employee': employee.id,
            'customer': customer.id,
            'products': [{'id': product_3.id, 'quantity': edited_quantity}],
        }

        response = self.client.put(
            BASE_URL + f'order/{order_id}',
            order_data,
            headers=Utils.get_headers_for_user(),
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # print(Order.objects.get(pk=order_id).products.all())
        # print(Order.objects.get(pk=order_id).products.filter(pk=product_1.id).exists())
        self.assertTrue(Order.objects.get(pk=order_id).products.filter(pk=product_3.id).exists())
        # self.assertEqual(Order.objects.get(pk=order_id).products.get(pk=product_3.id).quantity, edited_quantity)
        self.assertEqual(OrderProduct.objects.get(order__pk=order_id, product__pk=product_3.id).quantity,
                         edited_quantity)

    def test_delete__on_happy_path__should_return_NO_CONTENT(self):
        employee, customer = Utils.create_default_employee_and_customer()
        order_data = {
            'date': '2020-01-01', "employee": employee, "customer": customer}

        order_id = Order.objects.create(**order_data).id

        response = self.client.delete(
            BASE_URL + f'order/{order_id}',
            headers=Utils.get_headers_for_user()
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_patch__on_happy_path__should_return_NO_CONTENT(self):
        product_1 = Product.objects.create(**Utils.product_data)

        employee, customer = Utils.create_default_employee_and_customer()
        order_data = {
            'date': '2020-01-01',
            'employee': employee,
            'customer': customer.id,
            'products': [{'id': product_1.id, 'quantity': 2}]
        }

        serializer = OrderSerializer(data=order_data)
        serializer.is_valid()
        order_id = OrderService.create(serializer.validated_data).id

        response = self.client.patch(
            BASE_URL + f'order/{order_id}',
            {"status": "Cancelado"},
            headers=Utils.get_headers_for_user(),
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.get(pk=order_id).status, "Cancelado")


class OrderSerializerTestCase(APITestCase):

    def test_validate__without_customer__should_return_INVALID(self):
        product_1 = Product.objects.create(**Utils.product_data)
        product_2 = Product.objects.create(**Utils.product_data)

        employee, _ = Utils.create_default_employee_and_customer()
        order_data = {
            'date': '2020-01-01',
            'employee': employee,
            'products': [{'id': product_1.id, 'quantity': 2}, {'id': product_2.id, 'quantity': 3}]
        }

        serializer = OrderSerializer(data=order_data)
        self.assertFalse(serializer.is_valid())

    def test_validate__without_products__should_return_INVALID(self):
        employee, customer = Utils.create_default_employee_and_customer()
        order_data = {
            'date': '2020-01-01',
            'employee': employee,
            'customer': customer.id,
            'products': []
        }

        serializer = OrderSerializer(data=order_data)
        self.assertFalse(serializer.is_valid())

    def test_validate__product_without_id__should_return_INVALID(self):
        employee, customer = Utils.create_default_employee_and_customer()
        order_data = {
            'date': '2020-01-01',
            'employee': employee,
            'customer': customer.id,
            'products': [{'quantity': 2}]
        }

        serializer = OrderSerializer(data=order_data)
        self.assertFalse(serializer.is_valid())

    def test_validate__products_not_a_list__should_return_INVALID(self):
        product = Product.objects.create(**Utils.product_data)
        employee, customer = Utils.create_default_employee_and_customer()
        order_data = {
            'date': '2020-01-01',
            'employee': employee,
            'customer': customer.id,
            'products': {'id': product.id, 'quantity': 2}
        }

        serializer = OrderSerializer(data=order_data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)

    def test_validate__date_after_current__should_return_INVALID(self):
        product = Product.objects.create(**Utils.product_data)
        employee, customer = Utils.create_default_employee_and_customer()
        order_data = {
            'date': '2030-01-01',
            'employee': employee,
            'customer': customer.id,
            'products': [{'id': product.id, 'quantity': 2}]
        }

        serializer = OrderSerializer(data=order_data)
        self.assertFalse(serializer.is_valid())

    def test_validate__duplicated_products__should_return_INVALID(self):
        product = Product.objects.create(**Utils.product_data)
        employee, customer = Utils.create_default_employee_and_customer()
        order_data = {
            'date': '2020-01-01',
            'employee': employee,
            'customer': customer.id,
            'products': [{'id': product.id, 'quantity': 2}, {'id': product.id, 'quantity': 5}]
        }

        serializer = OrderSerializer(data=order_data)
        self.assertFalse(serializer.is_valid())
