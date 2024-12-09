from rest_framework import generics
from rest_framework.permissions import AllowAny

from users import models, serializers


class UserRegisterView(generics.CreateAPIView):
    """
    Принимает набор учетных данных для регистрации(редактирования) пользователя
    и возвращает JSON ответ с данными успешной регистрации(редактирования).
    """

    queryset = models.User.objects.all()
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """Установка пароля при регистрации"""
        user = serializer.save()
        user.set_password(user.password)
        user.save()
