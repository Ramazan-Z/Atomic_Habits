from celery import shared_task


@shared_task
def send_mailing(telegram_id, message):
    print(message)
