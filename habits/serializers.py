from rest_framework.serializers import ModelSerializer

from habits.models import Habit, MomentHabit
from habits.validators import RelatedHabitValidator, is_pleasant_validator, only_one_award_validator


class MomentHabitSerializer(ModelSerializer):
    """Сериализатор времени привычки"""

    class Meta:
        model = MomentHabit
        fields = ("title", "time")


class HabitSerializer(ModelSerializer):
    """Сериализатор сущности привычки"""

    moment = MomentHabitSerializer(help_text="Объект момента, содержит заголовк и время.")

    def create(self, validated_data):
        """Создание объекта вложенного поля (времени привычки)"""
        moment_data = validated_data.pop("moment")
        moment = MomentHabit.objects.create(**moment_data)
        return Habit.objects.create(moment=moment, **validated_data)

    def update(self, instance, validated_data):
        """Обновление объекта вложенного поля (времени привычки)"""
        moment_data = validated_data.pop("moment")
        moment = instance.moment
        for field, value in moment_data.items():
            setattr(moment, field, value)
        moment.save()
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def get_validators(self):
        """Список валидаторов для полей is_pleasant, award и related_habit"""
        return [is_pleasant_validator, only_one_award_validator, RelatedHabitValidator(self.context)]

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("owner",)
