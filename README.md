# WorkPlanner — Система планирования графика сотрудников

## Стек
- Python 3.x
- Django 6.x
- SQLite (встроена, ничего устанавливать не нужно)

## Структура проекта
```
WorkPlanner/
├── config/          # Настройки проекта (settings, urls)
├── workplanner/     # Основное приложение
│   ├── models.py    # Модели БД
│   ├── views.py     # Логика
│   ├── admin.py     # Панель администратора
│   └── templates/   # HTML шаблоны
├── manage.py
└── .env
```

---

## Запуск проекта

### 1. Клонировать репозиторий
```bash
git clone https://github.com/mesrop2008/teamwork
cd WorkPlanner
```

### 2. Создать и активировать виртуальное окружение
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Установить зависимости
```bash
pip install django
```

### 4. Применить миграции
```bash
python manage.py migrate
```

### 5. Создать суперпользователя (для Django Admin)
```bash
python manage.py createsuperuser
```

### 6. Создать аккаунт руководителя
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
User.objects.create_user(username='manager', password='manager123', is_staff=True)
exit()
```

### 7. Запустить сервер
```bash
python manage.py runserver
```

Приложение доступно по адресу: **http://127.0.0.1:8000**

---

## Первоначальная настройка данных

Зайди в Django Admin: **http://127.0.0.1:8000/admin/**

Добавляй данные в таком порядке:

1. **Alliance** — создай альянсы (например: `Альянс Пупкина`)
2. **Group** — создай группы и привяжи к альянсам (например: `Группа Сизых → Альянс Пупкина`)
3. **Employee** — создай сотрудников и привяжи к группам

---

## Роли пользователей

| Роль | Как создать | Возможности |
|------|-------------|-------------|
| Обычный пользователь | Любой, без входа | Выбрать сотрудника, добавить/удалить смены |
| Руководитель | `is_staff=True` | Подтверждать смены сотрудников |

### Вход как руководитель
На главной странице внизу есть кнопка **"Войти как руководитель"**.
После входа появится синяя панель сверху и кнопки **"Подтвердить"** напротив каждой смены.

---

## Основные URL

| URL | Описание |
|-----|----------|
| `/` | Главная страница — график сотрудников |
| `/admin/` | Django Admin — управление данными |
| `/login/` | Вход для руководителя |
| `/logout/` | Выход |
| `/add-shift/` | Добавление смены (POST) |
| `/delete-shift/<id>/` | Удаление смены (POST) |
| `/confirm-shift/<id>/` | Подтверждение смены (POST, только руководитель) |

---

## Настройки (config/settings.py)

```python
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Irkutsk'  # Поменяй на свой часовой пояс
USE_TZ = False
```
