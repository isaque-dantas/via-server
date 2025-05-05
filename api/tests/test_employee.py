from rest_framework import status
from rest_framework.test import APITestCase
from api import BASE_URL
from api.models.employee import Employee
from api.tests.utils import Utils


class EmployeeTestCase(APITestCase):

    def test_post__on_happy_path__should_return_CREATED(self):
        Employee.objects.all().delete()

        response = self.client.post(BASE_URL + 'employee', Utils.employee_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Employee.objects.filter(email=Utils.employee_data['email']).exists()
        )

    def test_login__on_happy_path__should_return_token(self):
        Employee.objects.create_user(**Utils.employee_data)

        response = self.client.post(
            BASE_URL + 'token',
            {'email': Utils.employee_data['email'], 'password': Utils.employee_data['password']}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_login__wrong_credentials__should_return_UNAUTHORIZED(self):
        response = self.client.post(
            BASE_URL + 'token',
            {'email': 'random@email.com', 'password': 'incorrect password'}
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get__on_happy_path__should_return_OK(self):
        response = self.client.get(
            BASE_URL + 'employee',
            headers=Utils.get_headers_for_user()
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], Utils.employee_data['name'])
