from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class CourseAndLessonTest(APITestCase):
    """Тесты проверки курсов и уроков"""

    def setUp(self):
        # Создаем группы
        self.moderator_group = Group.objects.create(name="Модераторы")
        self.redact_manager_group = Group.objects.create(name="Редакт-менеджер")

        # Создаем пользователей и добавляем их в группы
        self.user = User.objects.create_user(
            username="user", email="user@mail.ru", password="password"
        )
        self.moderator = User.objects.create_user(
            username="moderator", email="moderator@mail.ru", password="password"
        )
        self.redact_manager = User.objects.create_user(
            username="redact_manager",
            email="redactmanager@mail.ru",
            password="password",
        )

        self.moderator_group.user_set.add(self.moderator)
        self.redact_manager_group.user_set.add(self.redact_manager)

        # Создаем курс и урок для тестирования
        self.course = Course.objects.create(
            title="Test Course",
            description="Test Description",
            owner=self.redact_manager,
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Test Lesson 1",
            description="Test L Description",
            owner=self.redact_manager,
        )

    def test_create_course(self):
        """Тест создания курса"""
        self.client.force_authenticate(user=self.redact_manager)
        data = {"title": "Test", "description": "Test"}
        response = self.client.post("/courses/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_course(self):
        """Тест обновления курса"""
        self.client.force_authenticate(user=self.moderator)

        data = {
            "title": "U Test",
        }
        # Используем ID курса, который был создан в setUp
        response = self.client.patch(f"/courses/{self.course.id}/", data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_course(self):
        """Тест вывода списка курсов"""
        self.client.force_authenticate(user=self.moderator)

        response = self.client.get(
            "/courses/",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.json(), dict)

        self.assertIn("results", response.json())
        self.assertIsInstance(response.json()["results"], list)

        results = response.json()["results"]
        self.assertGreater(len(results), 0)  # Проверяем, что список не пуст
        self.assertEqual(results[0]["title"], "Test Course")  # Проверяем название курса

    def test_retrieve_course(self):
        """Тест просмотра курса"""
        self.client.force_authenticate(user=self.moderator)

        # Используем ID курса, который был создан в setUp
        response = self.client.get(
            f"/courses/{self.course.id}/",  # Используем self.course.id вместо 1
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_course(self):
        """Тест удаления курса"""
        self.client.force_authenticate(user=self.redact_manager)

        self.assertIsNotNone(Course.objects.filter(id=self.course.id).first())

        response = self.client.delete(
            f"/courses/{self.course.id}/",
        )

        # Проверяем статус ответа на удаление
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что курс действительно удален
        self.assertIsNone(Course.objects.filter(id=self.course.id).first())

    def test_create_lesson(self):
        """Тест создания урока"""
        self.client.force_authenticate(user=self.redact_manager)

        data = {
            "course": self.course.id,
            "title": "Test Lesson A",
            "description": "Test Lesson A",
        }
        response = self.client.post("/lesson/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_lesson(self):
        """Тест обновления урока"""
        self.client.force_authenticate(user=self.moderator)

        data = {
            "title": "UL Test",
        }
        # Используем ID курса, который был создан в setUp
        response = self.client.patch(f"/lesson/update/{self.lesson.id}/", data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_lessons(self):
        """Тест вывода списка уроков"""
        self.client.force_authenticate(user=self.moderator)

        response = self.client.get(
            "/lessons/",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.json(), dict)

        self.assertIn("results", response.json())
        self.assertIsInstance(response.json()["results"], list)

        results = response.json()["results"]
        self.assertGreater(len(results), 0)  # Проверяем, что список не пуст
        self.assertEqual(
            results[0]["title"], "Test Lesson 1"
        )  # Проверяем название курса

    def test_retrieve_lesson(self):
        """Тест просмотра урока"""
        self.client.force_authenticate(user=self.moderator)

        response = self.client.get(
            f"/lesson/{self.lesson.id}/",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        """Тест удаления урока"""
        self.client.force_authenticate(user=self.moderator)

        self.assertIsNotNone(Lesson.objects.filter(id=self.lesson.id).first())

        response = self.client.delete(
            f"/lesson/delete/{self.lesson.id}/",
        )

        # Проверяем статус ответа на удаление
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что курс действительно удален
        self.assertIsNone(Lesson.objects.filter(id=self.lesson.id).first())


class SubscriptionTest(APITestCase):
    """Тесты проверки подписки"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="user", email="user@mail.ru", password="password"
        )
        self.course = Course.objects.create(
            title="Test Course", description="Test Description", owner=self.user
        )

    def test_create_subscription(self):
        """Тест подключения и удаления подписки"""
        self.client.force_authenticate(user=self.user)
        data = {"course_id": self.course.id}

        response = self.client.post("/subscription/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post("/subscription/", data=data)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
