from rest_framework import status
from rest_framework.test import APITestCase
from api import BASE_URL
from api.models.user import User


class UserTestCase(APITestCase):
    client_data = {
        'email': 'cliente@email.com',
        'password': 'pass',
        'name': 'Usuário Cliente',
        'role': 'cliente',
    }

    seller_data = {
        'email': 'vendedor@email.com',
        'password': 'pass',
        'name': 'Usuário Vendedor',
        'role': 'vendedor',
    }

    def test_post__on_happy_path__should_return_CREATED(self):
        User.objects.all().delete()

        response = self.client.post(BASE_URL + 'user', self.client_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            User.objects.filter(email=self.client_data['email']).exists()
        )

    def test_login__on_happy_path__should_return_token(self):
        User.objects.create_user(**self.seller_data)

        response = self.client.post(
            BASE_URL + 'token',
            {'email': self.seller_data['email'], 'password': self.seller_data['password']}
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
        User.objects.create_user(**self.seller_data)

        response = self.client.post(
            BASE_URL + 'token',
            {'email': self.seller_data['email'], 'password': self.seller_data['password']}
        )

        access = response.data['access']

        response = self.client.get(
            BASE_URL + 'user',
            headers={'Authorization': f'Bearer {access}'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.seller_data['name'])
