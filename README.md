# hitalent-python-test-task
Тестовое задание на вакансию Junior python разработчика компании Hitalent

Проект представляет собой REST API для управления иерархической структурой подразделений компании и сотрудниками.

## Технологии

- **Python 3.13**
- **Django 5.1**
- **Django REST Framework**
- **PostgreSQL**
- **Poetry**
- **Docker + Docker Compose**

## Быстрый запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/AltyOfficial/hitalent-python-test-task.git
cd hitalent-python-test-task
```

### 2. Настройка окружения

Заполните файл ./environment./.env по шаблону из .env.example

### 3. Запуск через Docker

```bash
docker compose up --build -d
```

### 4. Применение миграций и создание суперпользователя
```
docker compose exec -it web python manage.py migrate
docker compose exec -it web python manage.py createsuperuser
```

### 5. Открыть проект
После успешного запуска API будет доступно по адресу:
→ http://localhost:8000
Простая API документация:

Swagger: http://localhost:8000/api/swagger/

### 6. Запуск автотестов
```
docker compose up -f docker-compose.test.yml up --build
```