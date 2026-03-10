from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course
from users.models import User


class UserAndPaymentTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="user", email="user@mail.ru", password="password"
        )
        self.course = Course.objects.create(
            title="Test Course", description="Test Description", owner=self.user
        )

    def test_create_payment(self):
        """Тест создания платежа"""
        self.client.force_authenticate(user=self.user)

        data = {"course": self.course.id}

        response = self.client.post("/users/payment/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
