# History API

Короткий backend на **FastAPI** для:

- авторизации и админов;
- таймлайна;
- студенческих проектов;
- загрузки файлов в `uploads/`.

## Быстрые ссылки

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- Все роуты: `/api/v1`

## Стек

- FastAPI
- SQLAlchemy + Alembic
- SQLite для простого локального запуска
- PostgreSQL для Docker
- JWT
- SMTP для писем администраторам и сброса пароля

## `.env`

Минимальный пример:

```env
DATABASE_URL=sqlite+aiosqlite:///./app.db

# Для Docker:
# DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/app_db

MAIL_PASSWORD=change_me
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=user@example.com
MAIL_DEFAULT_SENDER=no-reply@example.com

UPLOAD_DIR=uploads
UPLOAD_URL_PREFIX=/uploads
```

Важно:

- для `docker compose` нужен `DATABASE_URL` c Postgres и хостом `db`;
- создание `admin` и `superadmin` отправляет email, поэтому `MAIL_*` должны быть рабочими.

## Локальный запуск

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

После запуска открывайте `http://localhost:8000/docs`.

## Запуск через Docker

Сначала переключите `.env` на Postgres:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/app_db
```

Потом:

```powershell
docker compose up --build
```

Что поднимется:

- API на `localhost:8000`
- PostgreSQL на `localhost:5433`

Остановка:

```powershell
docker compose down
```

Полная очистка базы:

```powershell
docker compose down -v
```

## Первый superadmin

Локально:

```powershell
python -m app.common.scripts.create_superadmin --email admin@example.com --password StrongPassword123
```

В Docker:

```powershell
docker compose exec api python -m app.common.scripts.create_superadmin --email admin@example.com --password StrongPassword123
```

Успех:

```text
Superadmin created
```

Если уже существует:

```text
User already exists
```

## Логин

```bash
curl -X POST "http://localhost:8000/api/v1/users/login" ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"admin@example.com\",\"password\":\"StrongPassword123\"}"
```

Ответ:

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

Дальше передавайте токен так:

```text
Authorization: Bearer <access_token>
```

## Создание admin

Под `superadmin`:

```bash
curl -X POST "http://localhost:8000/api/v1/users/create-admin" ^
  -H "Authorization: Bearer <access_token>" ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"editor@example.com\"}"
```

Пароль для нового `admin` генерируется автоматически и уходит на почту.

## Роли

- `superadmin` — может создавать админов, менять чужие пароли и передавать роль супер-админа
- `admin` — может работать с контентом и менять свой пароль

## Полезные команды

Миграции:

```powershell
alembic upgrade head
alembic downgrade -1
```

Тесты:

```powershell
pytest
```

## Главное про проект

- Swagger использует `http://localhost:8000/docs`
- OAuth2-логин в проекте смотрит на `POST /api/v1/auth/login`
- JSON-логин есть на `POST /api/v1/users/login`
- загруженные файлы раздаются из `/uploads`