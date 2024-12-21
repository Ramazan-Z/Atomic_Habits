from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_celery_beat.models import PeriodicTask

from users.models import User


class MomentHabit(models.Model):
    """Модель времени привычки"""

    title: models.Field = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name="Заголовок",
        help_text="Описание момента выполнения привычки. Напимер, После обеда или Перед сном.",
    )
    time: models.Field = models.TimeField(
        verbose_name="Время",
        help_text="Время, когда необходимо выполнять привычку.",
    )

    def __str__(self):
        if self.title:
            return f"{self.title} (в {self.time})"
        return f"в {self.time}"

    class Meta:
        verbose_name = "Момент пивычки"
        verbose_name_plural = "Моменты привычек"
        ordering = ("time",)


class Habit(models.Model):
    """Модель сущности привычки"""

    action: models.Field = models.CharField(
        max_length=500,
        verbose_name="Действие",
        help_text="Действие, которое представляет собой привычка.",
    )
    place: models.Field = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name="Место",
        help_text="Место, в котором необходимо выполнять привычку. Напимер, В парке или На работе.",
    )
    moment: models.Field = models.OneToOneField(
        MomentHabit,
        on_delete=models.CASCADE,
        verbose_name="Момент привычки",
        help_text="Момент выполнения привычки с заголовком и временем.",
        related_name="moment_habits",
    )
    periodicity: models.Field = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Периодичность",
        help_text="Периодичность выполнения привычки для напоминания в днях, от 1 до 7 дней. По умолчанию 1 день.",
        validators=(MinValueValidator(1), MaxValueValidator(7)),
    )
    duration: models.Field = models.PositiveSmallIntegerField(
        default=60,
        verbose_name="Продолжительность",
        help_text="Продолжительность выполнения привычки в секундах, не более 120 сек. По умолчанию 60 сек.",
        validators=(MinValueValidator(1), MaxValueValidator(120)),
    )
    is_pleasant: models.Field = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text=(
            "Привычка, которую можно привязать к выполнению полезной привычки. По умолчанию false. "
            "Недопустимо, если указан related_habit или award."
        ),
    )
    related_habit: models.Field = models.ForeignKey(
        "Habit",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        help_text=(
            "Ссылка на приятную привычку (у которой is_pleasant=true), как на вознаграждение. "
            "Недопустимо, если is_pleasant=true или указан award."
        ),
        related_name="useful_habits",
    )
    award: models.Field = models.TextField(
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
        help_text=(
            "Чем пользователь должен себя вознаградить после выполнения привычки. "
            "Недопустимо, если is_pleasant=true или указан related_habit."
        ),
    )
    owner: models.Field = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        help_text="Создатель привычки",
        related_name="user_habits",
    )
    is_public: models.Field = models.BooleanField(
        default=False,
        verbose_name="Признак публичности",
        help_text=(
            "Привычки можно публиковать в общий доступ, чтобы другие пользователи могли брать в пример чужие привычки."
        ),
    )
    periodic_task: models.Field = models.OneToOneField(
        PeriodicTask,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Периодическая рассылка",
        help_text="Оповещение о необходимости выполнения привычки.",
        related_name="task_habits",
    )

    def __str__(self):
        if self.place:
            return f"Я буду {self.action} {self.moment} {self.place}."
        return f"Я буду {self.action} {self.moment}."

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
