from rest_framework import generics
from rest_framework.permissions import AllowAny

from users import models, serializers


class UserRegisterView(generics.CreateAPIView):
    """
    Принимает набор учетных данных для регистрации пользователя
    и возвращает JSON ответ с данными успешной регистрации.
    """

    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """Установка пароля при регистрации"""
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserProfileView(generics.RetrieveAPIView):
    """
    Возвращает JSON ответ с данными своего профиля.
    """

    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_object(self):
        """Получение пользователя как объекта просмотра"""
        return self.request.user


class UserUpdateView(generics.UpdateAPIView):
    """
    Принимает набор учетных данных для редактирования профиля
    и возвращает JSON ответ с данными успешного обновления.
    """

    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_object(self):
        """Получение пользователя как объекта редактирования"""
        return self.request.user

    def perform_update(self, serializer):
        """Возможность смены пароля"""
        user = serializer.save()
        if "password" in serializer.validated_data:
            user.set_password(user.password)
            user.save()
