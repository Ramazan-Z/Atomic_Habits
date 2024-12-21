from rest_framework.serializers import ModelSerializer

from habits.models import Habit, MomentHabit
from habits.services import create_periodic_task, update_periodic_task
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
        """Создание объекта вложенного поля (времени привычки) и задачи на рассылку"""
        moment_data = validated_data.pop("moment")
        moment = MomentHabit.objects.create(**moment_data)
        habit = Habit.objects.create(moment=moment, **validated_data)

        if not habit.is_pleasant:
            # Создание рассылки только для полезной привычки
            periodic_task = create_periodic_task(habit)
            habit.periodic_task = periodic_task
            habit.save()

        return habit

    def update(self, instance, validated_data):
        """Обновление объекта вложенного поля (времени привычки) и задачи на рассылку"""
        moment_data = validated_data.pop("moment", None)
        moment = instance.moment

        if moment_data:
            for field, value in moment_data.items():
                setattr(moment, field, value)
            moment.save()

        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        update_periodic_task(instance)

        return instance

    def get_validators(self):
        """Список валидаторов для полей is_pleasant, award и related_habit"""
        return [is_pleasant_validator, only_one_award_validator, RelatedHabitValidator(self.context)]

    class Meta:
        model = Habit
        exclude = ("periodic_task",)
        read_only_fields = ("owner",)
