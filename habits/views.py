from rest_framework import generics

from habits.models import Habit
from habits.paginators import ListPagination
from habits.permissions import IsOwnerUser, IsPublicHabit
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


class MyHabitsView(generics.ListAPIView):
    """
    Принимает параметры пагинации, сортировки, фильтрации и поиска.
    Возвращает постраничный список привычек текущего пользователя.
    """

    serializer_class = HabitSerializer
    pagination_class = ListPagination
    ordering_fields = ("moment", "duration")
    search_fields = ("action", "place")
    filterset_fields = ("is_pleasant", "is_public", "periodicity")

    def get_queryset(self):
        """Фильтрация чужих привычек из списка"""
        return Habit.objects.filter(owner=self.request.user)


class PublicHabitsView(generics.ListAPIView):
    """
    Принимает параметры пагинации, сортировки, фильтрации и поиска.
    Возвращает постраничный список публичных привычек.
    """

    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    pagination_class = ListPagination
    ordering_fields = ("moment", "duration")
    search_fields = ("action", "place")
    filterset_fields = ("is_pleasant", "periodicity", "owner")


class HabitEditView(generics.UpdateAPIView):
    """
    Принимает набор данных для обновления привычки
    и возвращает JSON ответ с данными успешно обновленного объекта.
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwnerUser]


class HabitRetrieveView(generics.RetrieveAPIView):
    """Bозвращает JSON ответ с данными об указанной привычке."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwnerUser | IsPublicHabit]


class HabitDestroyView(generics.DestroyAPIView):
    """Удаляет указанную привычку."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwnerUser]

    def perform_destroy(self, instance):
        """Удаление связанного объекта момента"""
        instance.moment.delete()
