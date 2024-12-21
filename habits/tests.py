from django.urls import reverse
from django.utils.timezone import localtime
from django_celery_beat.models import PeriodicTask
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit, MomentHabit
from users.models import User


class NewHabitTestCase(APITestCase):
    """Тесты создания привычки и валидаторов"""

    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.url = reverse("habits:new-habit")
        self.user = User.objects.create(email="user@sky.pro", username="user")
        self.client.force_authenticate(user=self.user)
        # Создание полезной привычки
        moment = MomentHabit.objects.create(title="По утрам", time="7:00:00")
        self.useful_habit = Habit.objects.create(moment=moment, action="Бегать", owner=self.user)
        # Создание приятной привычки
        moment = MomentHabit.objects.create(title="После обеда", time="13:00:00")
        self.pleasant_habit = Habit.objects.create(moment=moment, action="Пить сок", is_pleasant=True, owner=self.user)

    def test_is_pleasant_validator(self):
        """Случай попытки указать вознаграждение для приятной привычки"""
        data = {
            "moment": {"time": "16:00:00"},
            "action": "Есть десерт",
            "is_pleasant": True,
            "award": "Можно дважды повторить",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["non_field_errors"], ["Приятная привычка не может содержать вознаграждение."])

    def test_only_one_award_validator(self):
        """Случай попытки указать и вознаграждение и связанную привычку"""
        data = {
            "moment": {"time": "09:00:00"},
            "action": "Делать гимнастику для глаз",
            "award": "Съесть яблоко",
            "related_habit": self.pleasant_habit.id,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["non_field_errors"], ["Допускается толко одно вознаграждение: related_habit или award."]
        )

    def test_related_habit_validator(self):
        """Случай попытки привязки полезной привычки"""
        data = {
            "moment": {"time": "20:00:00"},
            "action": "Учить 10 иностранных слов",
            "related_habit": self.useful_habit.id,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["non_field_errors"], ["В качестве награды допускаются только приятные привычки."]
        )

    def test_private_related_habit_validator(self):
        """Случай попытки привязки чужой приятной привычки"""
        other_user = User.objects.create(email="other_user@sky.pro", username="other_user")
        self.client.force_authenticate(user=other_user)
        data = {
            "moment": {"time": "08:30:00"},
            "action": "Делать зарядку",
            "related_habit": self.pleasant_habit.id,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["non_field_errors"], ["В качестве награды допускаются только свои или публичные привычки."]
        )

    def test_max_value_fields(self):
        """Случай попытки превысить максимальные значения полей"""
        data = {
            "moment": {"time": "19:00:00"},
            "action": "Наводить порядок",
            "duration": 121,
            "periodicity": 8,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["periodicity"], ["Ensure this value is less than or equal to 7."])
        self.assertEqual(response.json()["duration"], ["Ensure this value is less than or equal to 120."])

    def test_successful_create_habit(self):
        """Успешная проверка всех валидаторов"""
        data = {
            "moment": {"time": "14:30:00"},
            "action": "Делать разминку",
            "place": "На работе",
            "periodicity": 1,
            "duration": 120,
            "is_pleasant": False,
            "award": None,
            "is_public": True,
            "related_habit": self.pleasant_habit.id,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверка создания рассылки вместе с привычкой
        periodic_task_name = f"Mailing for habit {response.json().get('id')}"
        self.assertTrue(PeriodicTask.objects.filter(name=periodic_task_name).exists())


class HabitListTestCase(APITestCase):
    """Тесты получения списков привычек"""

    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.user = User.objects.create(email="user@sky.pro", username="user")
        self.client.force_authenticate(user=self.user)
        # Создание приватной привычки
        moment = MomentHabit.objects.create(time="12:40:00")
        self.private_habit = Habit.objects.create(moment=moment, action="Test private", owner=self.user)
        # Создание публичной привычки
        moment = MomentHabit.objects.create(time="12:40:00")
        self.public_habit = Habit.objects.create(moment=moment, action="Test public", is_public=True, owner=self.user)

    def test_my_habits(self):
        """Тест просмотра списка своих привычек"""
        response = self.client.get(reverse("habits:my-habits"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("count"), 2)

    def test_public_habits(self):
        """Тест просмотра списка публичных привычек"""
        response = self.client.get(reverse("habits:public-habits"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("count"), 1)


class EditHabitTestCase(APITestCase):
    """Тесты редактирования привычки"""

    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.user = User.objects.create(email="user@sky.pro", username="user")
        self.client.force_authenticate(user=self.user)
        # Создание полезной привычки с рассылкой
        data = {"moment": {"time": "07:00:00"}, "action": "Бегать"}
        response = self.client.post(reverse("habits:new-habit"), data, format="json")
        self.useful_habit = Habit.objects.get(pk=response.json().get("id"))
        # Создание приятной привычки
        moment = MomentHabit.objects.create(title="После обеда", time="13:00:00")
        self.pleasant_habit = Habit.objects.create(moment=moment, action="Пить сок", is_pleasant=True, owner=self.user)

    def test_update_habit(self):
        """Тест редактирования привычки"""
        url = reverse("habits:edit-habit", args=(self.useful_habit.pk,))
        data = {
            "moment": {"title": "Вечером", "time": "16:00:00"},
            "action": "Заниматься спортом",
            "is_public": True,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        edited_habit = Habit.objects.get(pk=self.useful_habit.pk)
        self.assertTrue(edited_habit.is_public)

        # Проверка изменения рассылки
        periodic_task_name = f"Mailing for habit {response.json().get('id')}"
        periodic_task = PeriodicTask.objects.get(name=periodic_task_name)
        self.assertEqual(localtime(periodic_task.start_time).time(), edited_habit.moment.time)

    def test_unpleasant_habit(self):
        """Случай отмены признака приятной привычки"""
        url = reverse("habits:edit-habit", args=(self.pleasant_habit.pk,))
        data = {"is_pleasant": False}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        edited_habit = Habit.objects.get(pk=self.pleasant_habit.pk)
        self.assertFalse(edited_habit.is_pleasant)

        # Проверка создания рассылки
        periodic_task_name = f"Mailing for habit {response.json().get('id')}"
        self.assertTrue(PeriodicTask.objects.filter(name=periodic_task_name).exists())

    def test_set_pleasant_habit(self):
        """Случай установки признака приятной привычки"""
        url = reverse("habits:edit-habit", args=(self.useful_habit.pk,))
        data = {"is_pleasant": True}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        edited_habit = Habit.objects.get(pk=self.useful_habit.pk)
        self.assertTrue(edited_habit.is_pleasant)

        # Проверка удаления рассылки
        periodic_task_name = f"Mailing for habit {response.json().get('id')}"
        self.assertFalse(PeriodicTask.objects.filter(name=periodic_task_name).exists())

    def test_permissions(self):
        """Тест прав доступа на редактирование"""
        url = reverse("habits:edit-habit", args=(self.useful_habit.pk,))
        other_user = User.objects.create(email="other_user@sky.pro", username="other_user")
        self.client.force_authenticate(user=other_user)
        data = {
            "moment": {"title": "Вечером", "time": "16:00:00"},
            "action": "Есть десерт",
            "is_public": True,
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RetrieveDestroyHabitTestCase(APITestCase):
    """Тесты просмотра и удаления привычки"""

    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.user = User.objects.create(email="user@sky.pro", username="user")
        self.client.force_authenticate(user=self.user)
        # Создание приватной привычки с рассылкой
        data = {"moment": {"time": "12:40:00"}, "action": "Test private"}
        response = self.client.post(reverse("habits:new-habit"), data, format="json")
        self.private_habit = Habit.objects.get(pk=response.json().get("id"))
        # Создание публичной привычки
        moment = MomentHabit.objects.create(time="12:40:00")
        self.public_habit = Habit.objects.create(moment=moment, action="Test public", is_public=True, owner=self.user)

    def test_retrive_habit(self):
        """Тест просмотра своей приватной привычки"""
        url = reverse("habits:retrieve-habit", args=(self.private_habit.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("id"), self.private_habit.pk)

    def test_private_retrive_habit(self):
        """Тест прав доступа на просмотр, случай с приватной првычкой"""
        url = reverse("habits:retrieve-habit", args=(self.private_habit.pk,))
        other_user = User.objects.create(email="other_user@sky.pro", username="other_user")
        self.client.force_authenticate(user=other_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_public_retrive_habit(self):
        """Тест прав доступа на просмотр, случай с публичной првычкой"""
        url = reverse("habits:retrieve-habit", args=(self.public_habit.pk,))
        other_user = User.objects.create(email="other_user@sky.pro", username="other_user")
        self.client.force_authenticate(user=other_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("id"), self.public_habit.pk)

    def test_destroy_habit(self):
        """Тест удаления привычки"""
        url = reverse("habits:destroy-habit", args=(self.private_habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(pk=self.private_habit.pk).exists())

        # Проверка удаления рассылки вместе с привычкой
        periodic_task_name = f"Mailing for habit {self.private_habit.pk}"
        self.assertFalse(PeriodicTask.objects.filter(name=periodic_task_name).exists())
