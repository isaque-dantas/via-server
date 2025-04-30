from rest_framework import status
from rest_framework.test import APITestCase
from api import BASE_URL
from api.models.customer import Customer
from api.tests.utils import Utils


class CustomerTestCase(APITestCase):
    customer_data = {
        'name': 'LogAp Sistemas',
        'email': 'contato@logap.com.br',
    }

    def test_post__on_happy_path__should_return_CREATED(self):
        Customer.objects.all().delete()

        response = self.client.post(
            BASE_URL + 'customer',
            self.customer_data,
            headers=Utils.get_headers_for_user()
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Customer.objects.filter(email=self.customer_data['email']).exists()
        )

    def test_get_many__on_happy_path__should_return_OK(self):
        Customer.objects.all().delete()

        Customer.objects.create(**self.customer_data)

        response = self.client.get(
            BASE_URL + f'customer',
            headers=Utils.get_headers_for_user()
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_single__on_happy_path__should_return_OK(self):
        Customer.objects.all().delete()
        customer = Customer.objects.create(**self.customer_data)

        response = self.client.get(
            BASE_URL + f'customer/{customer.id}',
            headers=Utils.get_headers_for_user()
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.customer_data['name'])

    def test_put__on_happy_path__should_return_NO_CONTENT(self):
        Customer.objects.all().delete()
        customer = Customer.objects.create(**self.customer_data)

        edited_data = self.customer_data.copy()
        edited_data['email'] = 'novo.email@logap.com.br'

        response = self.client.put(
            BASE_URL + f'customer/{customer.id}',
            edited_data,
            headers=Utils.get_headers_for_user()
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            Customer.objects.get(pk=customer.id).email,
            edited_data['email']
        )

    def test_put__repeated_email__should_return_BAD_REQUEST(self):
        Customer.objects.all().delete()
        gov_customer_data = {
            "name": "Governo Federal",
            "email": "gov@gov.br"
        }

        gov_customer = Customer.objects.create(**gov_customer_data)
        Customer.objects.create(**self.customer_data)

        edited_data = gov_customer_data.copy()
        edited_data['email'] = self.customer_data["email"]

        response = self.client.put(
            BASE_URL + f'customer/{gov_customer.id}',
            edited_data,
            headers=Utils.get_headers_for_user()
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete__on_happy_path__should_return_NO_CONTENT(self):
        Customer.objects.all().delete()
        customer = Customer.objects.create(**self.customer_data)

        response = self.client.delete(
            BASE_URL + f'customer/{customer.id}',
            headers=Utils.get_headers_for_user()
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Customer.objects.filter(pk=customer.id).exists())
