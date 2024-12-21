from rest_framework.serializers import ValidationError


def is_pleasant_validator(data):
    """Валидатор признака приятной привычки"""
    is_pleasant = data.get("is_pleasant")
    related_habit = data.get("related_habit")
    award = data.get("award")
    if is_pleasant and (related_habit or award):
        raise ValidationError("Приятная привычка не может содержать вознаграждение.")


def only_one_award_validator(data):
    """Валидатор только одного вознаграждения"""
    is_pleasant = data.get("is_pleasant")
    related_habit = data.get("related_habit")
    award = data.get("award")
    if not is_pleasant and (related_habit and award):
        raise ValidationError("Допускается толко одно вознаграждение: related_habit или award.")


class RelatedHabitValidator:
    """Валидатор связанной привычки"""

    def __init__(self, context_data):
        self.request = context_data.get("request")

    def __call__(self, data):
        related_habit = data.get("related_habit")
        if related_habit:
            if related_habit.owner != self.request.user and not related_habit.is_public:
                raise ValidationError("В качестве награды допускаются только свои или публичные привычки.")
            if not related_habit.is_pleasant:
                raise ValidationError("В качестве награды допускаются только приятные привычки.")


# Валидация периодичности и продолжительности привычки реализованы на уровне модели.
