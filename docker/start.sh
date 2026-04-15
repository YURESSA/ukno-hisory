#!/bin/sh

set -e

echo "🚀 Running migrations..."
alembic upgrade head

echo "🔥 Starting app..."
gunicorn app.main:app \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --workers 2 \
  --timeout 60