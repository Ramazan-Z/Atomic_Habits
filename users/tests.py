from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):

    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.user = User.objects.create(email="user@sky.pro", username="user")
        self.user.set_password("user")
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_user_register(self):
        """Тест регистрации пользователя"""
        url = reverse("users:register")
        data = {
            "email": "user2@sky.pro",
            "username": "user2",
            "password": "user2",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_user_login(self):
        """Тест получения токена"""
        url = reverse("users:login")
        data = {
            "email": "user@sky.pro",
            "password": "user",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json().get("access"))

    def test_user_profile(self):
        """Тест просмотра профиля пользователя"""
        url = reverse("users:profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("id"), self.user.pk)

    def test_user_update(self):
        """Тест редактирования профиля"""
        url = reverse("users:update")
        data = {
            "username": "new_username",
            "first_name": "new_first_name",
            "last_name": "new_last_name",
            "phone": "12345678",
            "telegram_id": "12345",
            "city": "city",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.username, data["username"])
        self.assertEqual(self.user.last_name, data["last_name"])
        self.assertEqual(self.user.first_name, data["first_name"])
        self.assertEqual(self.user.phone, data["phone"])
        self.assertEqual(self.user.telegram_id, data["telegram_id"])
        self.assertEqual(self.user.city, data["city"])
