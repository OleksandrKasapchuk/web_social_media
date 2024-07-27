# Tashkegram

**Tashkegram** - це копія Instagram, створена за допомогою Django.

## Функціональні можливості

- 📜 Реєстрація та аутентифікація
- 📝 Створення та редагування постів
- ❤️ Лайки та коментарі
- 🔔 Сповіщення про лайки, коментарі та повідомлення
- 👥 Система підписників
- 💬 Чат між користувачами

## Встановлення

### Передумови

- 🐍 Python 3.x
- 📦 pip
- 🌐 virtualenv

### Інструкція

1. Клонуйте репозиторій:
   ```bash
   git clone https://github.com/OleksandrKasapchuk/web_social_media.git

2. Створіть та активуйте віртуальне середовище:
	```bash
	python -m venv venv
	venv\Scripts\activate
	
3. Встановіть залежності:
	```bash
	pip install -r requirements.txt

4. Застосуйте міграції:
	```bash
	python manage.py migrate

5. Створіть суперкористувача:
	```bash
	python manage.py createsuperuser

6. Запустіть сервер:`
	```bash
	python manage.py runserver

7. Відкрийте http://127.0.0.1:8000/ у браузері.

## Використання 
- 🏠 Головна сторінка: перегляд всіх постів або тільки підписаних користувачів.
- 🧑‍💻 Профіль користувача: перегляд постів та інформації про підписників.
- ➕ Створення постів: кнопка "Add" у навігаційній панелі.
- ❤️ Лайки та коментарі: взаємодія з постами.
- 💬 Чат: початок чату з профілю користувача.
- 🔔 Сповіщення: отримання сповіщень про нові взаємодії.

## Контактна інформація 

Для питань та пропозицій пишіть на sasha291108@gmail.com