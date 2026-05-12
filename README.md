# History API

Backend на **FastAPI** для:

- авторизации и администрирования пользователей;
- таймлайна;
- студенческих проектов;
- загрузки файлов в `backend/uploads/`.

## Быстрые ссылки

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- Базовый префикс роутов: `/api/v1`

## Стек

- FastAPI
- SQLAlchemy + Alembic
- SQLite для простой локальной разработки
- PostgreSQL для Docker и integration smoke tests
- JWT
- SMTP для писем администраторам и сброса пароля

## Конфигурация

Проект использует **один основной файл**: `.env`.

В git хранится только шаблон [`.env.example`](</C:/Users/goshr/PycharmProjects/ukno-hisory/.env.example:1>).
Локально создайте свой `.env` на его основе.

Минимальный пример:

```env
DB_BACKEND=sqlite
SQLITE_DB_PATH=backend/data/app.db

UPLOAD_DIR=backend/uploads
UPLOAD_URL_PREFIX=/uploads

LOG_LEVEL=INFO
LOG_JSON=true
LOG_INCLUDE_QUERY_STRING=false
LOG_SQL_QUERIES=false

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=app_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=change_me

DOCKER_POSTGRES_PORT=5433
DOCKER_DB_BACKEND=postgres
DOCKER_POSTGRES_HOST=db

MAIL_PASSWORD=change_me
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=user@example.com
MAIL_DEFAULT_SENDER=no-reply@example.com
```

Как это работает:

- при обычном локальном запуске используется `.env`;
- если `DB_BACKEND=sqlite`, приложение работает с SQLite в `backend/data/`;
- при `docker compose up --build` контейнер API берёт docker-значения из `DOCKER_*` переменных в `.env`;
- integration smoke tests на Postgres используют те же `POSTGRES_*` и `DOCKER_POSTGRES_PORT` из `.env`.

## Локальный запуск

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic -c backend/alembic.ini upgrade head
uvicorn --app-dir backend app.main:app --reload
```

После запуска откройте `http://localhost:8000/docs`.

## Bootstrap для новой машины

Есть готовый скрипт:

```powershell
.\backend\scripts\dev-setup.ps1
```

Он:

- создаёт `.venv`, если его ещё нет;
- ставит зависимости;
- создаёт `.env` из `.env.example`, если файла ещё нет;
- прогоняет миграции.

## Запуск через Docker

Ничего в `.env` переключать не нужно.

```powershell
docker compose up --build
```

Поднимется:

- API на `localhost:8000`
- PostgreSQL на `localhost:5433`

Остановка:

```powershell
docker compose down
```

Полная очистка тома базы:

```powershell
docker compose down -v
```

## Тесты

Быстрый основной набор:

```powershell
pytest
```

Smoke-тесты на реальном Postgres:

```powershell
docker compose up -d db
pytest -c backend/pytest.ini -m postgres_integration
docker compose down
```

Если Postgres не поднят, эти тесты будут пропущены, а не уронят весь прогон.

## Логирование

Приложение пишет структурированные request logs.

В логах есть:

- `request_id`
- HTTP method
- request path / route
- response status
- request duration in milliseconds

Каждый HTTP-ответ также содержит заголовок `X-Request-ID`, чтобы можно было связать ошибку на клиенте с серверным логом.

## Первый superadmin

Локально:

```powershell
$env:PYTHONPATH="backend"
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

Если пользователь уже существует:

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

Пароль для нового `admin` генерируется автоматически и отправляется на почту.

## Роли

- `superadmin` может создавать админов, менять чужие пароли и передавать роль супер-админа
- `admin` может работать с контентом и менять свой пароль

## Полезные команды

Миграции:

```powershell
alembic -c backend/alembic.ini upgrade head
alembic -c backend/alembic.ini downgrade -1
```

Тесты:

```powershell
pytest -c backend/pytest.ini
```

## Важные замечания

- Swagger использует `http://localhost:8000/docs`
- OAuth2-логин в проекте смотрит на `POST /api/v1/auth/login`
- JSON-логин есть на `POST /api/v1/users/login`
- загруженные файлы хранятся в `backend/uploads/` и раздаются из `/uploads`
