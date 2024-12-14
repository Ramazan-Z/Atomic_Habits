import json

from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask


def get_start_time(time):
    """Возвращает datetime c текущей датой и указанным временем"""
    today = timezone.now()
    start_time = today.replace(hour=time.hour, minute=time.minute, second=time.second, microsecond=time.microsecond)
    return start_time


def get_message(habit):
    """Генерация сообщения рассылки на основе сущности привычки"""
    return f"Напоминание о прививаемой привычке:\n{habit}"


def create_periodic_task(habit):
    """Создание периодической задачи для рассылки"""
    schedule, _ = IntervalSchedule.objects.get_or_create(every=habit.periodicity, period=IntervalSchedule.DAYS)
    periodic_task = PeriodicTask.objects.create(
        interval=schedule,
        name=f"Mailing for habit {habit.pk}",
        task="habits.tasks.send_mailing",
        start_time=get_start_time(habit.moment.time),
        args=json.dumps([habit.owner.telegram_id, get_message(habit)]),
    )
    return periodic_task


def update_periodic_task(habit):
    """Обновление периодической задачи для рассылки"""
    periodic_task = habit.periodic_task
    # Удалить рассылку, если привычка стала приятной
    if periodic_task and habit.is_pleasant:
        periodic_task.delete()
    # Создать рассылку, если привычка больше не приятная
    elif not periodic_task and not habit.is_pleasant:
        habit.periodic_task = create_periodic_task(habit)
        habit.save()
    # Изменить рассылку, если она есть
    elif periodic_task:
        schedule, _ = IntervalSchedule.objects.get_or_create(every=habit.periodicity, period=IntervalSchedule.DAYS)
        periodic_task.interval = schedule
        periodic_task.start_time = get_start_time(habit.moment.time)
        periodic_task.args = json.dumps([habit.owner.telegram_id, get_message(habit)])
        periodic_task.last_run_at = None
        periodic_task.save()
