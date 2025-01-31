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
* `gunicorn`
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
* Изменение профиля.
* Список привычек текущего пользователя с пагинацией.
* Список публичных привычек с пагинацией.
* Создание привычки.
* Просмотр привычки.
* Редактирование привычки.
* Удаление привычки.
## Установка локально и на сервере
1. Клонировать проект
	```
	git clone https://github.com/Ramazan-Z/Atomic_Habits.git
	```
2. Заполнить файл `env.example` и сохранить как `.env.`
	* `cd Atomic_Habits`,
	* `nano env.example`
	* заполнить файл
	* `Ctrl+O`,
	* ввести новое имя `.env`, enter
	* `Ctrl+X`
3. Сборка и запуск
	```
	docker compose up -d --build
	```
### CI/CD
Обновления автоматически проверяются линтерами,
тестируются и деплоятся на сервер при запросе
pull request
### Документация
```
http://s191765.foxcdn.ru/redoc/
```
