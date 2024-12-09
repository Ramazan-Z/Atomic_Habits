from rest_framework import serializers

from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации/редактирования пользователя."""

    class Meta:
        model = User
        exclude = ("is_superuser", "is_staff", "is_active", "groups", "user_permissions")
        read_only_fields = ("date_joined", "last_login")
        extra_kwargs = {"password": {"write_only": True}}
