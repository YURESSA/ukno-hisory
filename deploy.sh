#!/usr/bin/env sh
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
test -s .env.production || { echo "Не найден .env.production" >&2; exit 1; }
test -s frontend/dist/index.html || { echo "Сначала соберите frontend: npm ci && npm run build" >&2; exit 1; }
docker compose --env-file .env.production -f deploy/compose.production.yml build api
docker compose --env-file .env.production -f deploy/compose.production.yml build frontend
docker compose --env-file .env.production -f deploy/compose.production.yml up -d --wait --wait-timeout 180
docker compose --env-file .env.production -f deploy/compose.production.yml ps
