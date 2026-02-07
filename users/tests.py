from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User


class UserAndPaymentTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', email='user@mail.ru', password='password')

    def test_retrieve_user(self):
        """Тест просмотр пользователя"""

        response = self.client.get(
            f'/users/{self.user.id}',

        )




