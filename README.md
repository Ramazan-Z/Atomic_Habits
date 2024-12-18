# Курсовой проект Python/Django REST Framework
## Описание
Бэкенд-часть SPA веб-приложения трекера полезных привычек,
по идеям книги Джеймса Клира «Атомные привычки».
## Задачи
1. Добавить необходимые модели привычек.
2. Реализовать эндпоинты для работы с фронтендом.
3. Создать приложение для работы с Telegram и рассылками напоминаний.
## Зависимости
* `django`
* `djangorestframework`
* `djangorestframework-simplejwt`
* `django-filter`
* `django-cors-headers`
* `drf-yasg`
* `python-dotenv`
* `psycopg2-binary`
* `pillow`
* `redis`
* `celery`
* `django-celery-beat`
* `requests`
* `ipython`
* `coverage`
## Линтеры
* `flake8`
* `black`
* `mypy`
* `isort`
* `django-stubs`
* `types-psycopg2`
* `djangorestframework-stubs`
* `django-filter-stubs`
* `types-requests`
* `drf-yasg-stubs`
* `celery-stubs`
### Эндпоинты
* Регистрация пользователя.
* Авторизация пользователя.
* Просмотр профиля.
* Изменение профиля
* Список привычек текущего пользователя с пагинацией.
* Список публичных привычек с пагинацией.
* Создание привычки.
* Просмотр привычки.
* Редактирование привычки.
* Удаление привычки.
## Установка
1. Клонировать проект
	```
	https://github.com/Ramazan-Z/Atomic_Habits.git
	```
2. Установить зависимости
	```
	poetry install
	```
3. Создать в корне проекта файл `.env` из  копии `env.example`и прописать в нем:
	* Секретный ключ и флаг дебага проекта
	* Параметры для подключения к базе данных.
	* Настройки для использования Redis.
	* Telegram bot токен
4. Создать БД и ее структуру.
	```
	python manage.py create_db
	```
5. Применить миграции.
	```
	python manage.py migrate
	```
6. Создать супер пользователя
	```
	python manage.py createsuperuser
	```
### Тестирование
Проект покрыт тестами на 93%.
* Запуск теста
    ```
    coverage run --source='.' manage.py test
    ```
* Покрытие кода
	```
	coverage report
	```
## Запуск
1. Запустить Celery
	```
	celery -A config worker -l INFO
	```
2. Запустить Celery-beat
    ```
	celery -A config beat -l INFO
	```
3. Запустить сервер
	```
	python manage.py runserver
	```
### Документация

```
http://localhost:8000/redoc/
```
