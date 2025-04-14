# Money Flow — Django-приложение учёта финансов

Веб-приложение для учёта доходов и расходов. Реализовано с использованием **Django** и **Bootstrap**, работает на **SQLite**. Подходит для персонального или малого финансового учёта.

---

## Функционал

- Добавление записей о доходах и расходах
- Удобный интерфейс на Bootstrap
- Хранение данных в базе SQLite
- Управление справочниками
- Возможность загрузки начальных данных из fixtures
- Полностью рабочая Админ панелька (Login: Admin, Password: 200414)

## Установка и запуск проекта

### 1. Клонирование репозитория
```bash
git clone https://github.com/ваш-профиль/money-flow.git
cd money-flow
```

### 2. Создание виртуального окружения и его активация
```bash
python -m venv venv
venv\Scripts\activate          # Windows
# или
source venv/bin/activate       # Mac/Linux
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Применение миграций
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Загрузка начальных данных (fixtures)
```bash
python manage.py loaddata initial_data.json
```

### 6. Запуск сервера
```bash
python manage.py runserver
```


## Технологии

- Python 3.12
- Django 5.2
- Bootstrap 5
- SQLite (по умолчанию)

---

## Обратная связь

Если возникнут вопросы, предложения или баги, мой telegram — @luffkka.
