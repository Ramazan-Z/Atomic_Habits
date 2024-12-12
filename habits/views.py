from rest_framework import generics

from habits.models import Habit
from habits.serializers import HabitSerializer


class HabitNewView(generics.CreateAPIView):
    """
    Принимает набор данных для создания привычки
    и возвращает JSON ответ с данными успешно созданого объекта.
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        """Назначение владельца при создании привычки"""
        serializer.save(owner=self.request.user)
