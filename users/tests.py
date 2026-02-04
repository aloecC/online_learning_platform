from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User


class UserAndPaymentTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', email='user@mail.ru', password='password')

    def test_create_user(self):
        """Тест создания пользователя"""

        data = {
            'email': 'user@mail.ru',
            'username': 'user',
            'password': 'password'
        }

        response = self.client.post(
            '/users/',
            data=data
        )

