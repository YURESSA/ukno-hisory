# Развёртывание истории

Рабочая ветка: `timeweb-deploy`. Пуши в неё запускают тесты на SQLite и локальных файлах, сборку frontend и, после успешной проверки, деплой точного коммита. Остальные ветки только проверяются.

Локальный запуск не требует PostgreSQL и S3. Используйте `.env.example` с `DB_BACKEND=sqlite` и `STORAGE_BACKEND=local`, создайте `backend/data`, выполните миграции и запустите API по инструкции в основном README. Для frontend: `npm ci`, затем `npm run dev`.

## Сервер

Адрес сайта: `http://5.129.249.175`. HTTPS пока не используется. PostgreSQL: отдельная база `5history`. S3: существующий бакет с отдельным префиксом `5history/`; файлы `ukno/` не затрагиваются. В БД сохраняются стабильные `/uploads/...`; API перенаправляет на временные подписанные S3-ссылки.

Конфигурация и секреты находятся только в `/opt/history/.env.production` (права 600). Релизы — `/opt/history/releases/<commit>`, текущий — `/opt/history/current`. Production compose не запускает локальную БД и не публикует API напрямую. Сборка frontend выполняется в CI, чтобы не перегружать сервер с 1 ГБ RAM.

## GitHub Actions

Секреты репозитория: `DEPLOY_HOST`, `DEPLOY_PORT`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`, `DEPLOY_KNOWN_HOSTS`. SSH-ключ ограничен командой `/opt/history/receive-release.sh`, без PTY и forwarding. Команда принимает только `deploy <40-символьный SHA>`, получает архив через stdin и запускает Docker Compose. Настройки БД, S3 и SMTP в GitHub не передаются.

Первичная установка: загрузить файлы проверенного релиза и собранный `frontend/dist`, добавить ссылку `.env.production` на серверную конфигурацию и выполнить `sh deploy.sh`. Для CI установить `deploy/receive-release.sh` в `/opt/history/receive-release.sh` с правами 700 и добавить ограниченный публичный ключ в `authorized_keys` после разрешения владельца сервера.

## Проверка и возврат версии

```sh
cd /opt/history/current
docker compose --env-file .env.production -f deploy/compose.production.yml ps
curl -f http://127.0.0.1/healthz
curl -f http://127.0.0.1/api/v1/timeline/
```

Для возврата приложения перейдите в каталог предыдущего релиза и выполните `sh deploy.sh`, затем обновите `/opt/history/current`. Миграции БД применяются при запуске API; обратный переход через несовместимую миграцию требует отдельного плана и резервной копии БД. Деплой не удаляет Docker-тома и старые образы.
