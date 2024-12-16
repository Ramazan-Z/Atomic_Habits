import requests
from celery import shared_task

from config.settings import TELEGRAM_TOKEN


@shared_task
def send_mailing(telegram_id, message):
    """Отправка напоминания о привычке"""
    if not telegram_id:
        return

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": telegram_id, "text": message}
    response = requests.post(telegram_url, data=data)
    if response.status_code == 200:
        print("Сообщение отправлено")
    else:
        print("Ошибка отравки сообщения")
