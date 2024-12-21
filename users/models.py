from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель сущности пользователя"""

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Укажите электронную почту",
    )
    phone: models.Field = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        verbose_name="Телефон",
        help_text="Укажите номер телефона",
    )
    telegram_id: models.Field = models.CharField(
        blank=True,
        null=True,
        max_length=10,
        verbose_name="Телеграм id",
        help_text="Укажите идентификатор телеграм",
    )
    city: models.Field = models.CharField(
        blank=True,
        null=True,
        max_length=60,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        blank=True,
        null=True,
        upload_to="avatars/",
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
