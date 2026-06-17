#!/usr/bin/env sh

set -eu

BRANCH="${1:-branch-for-deploy}"
PROJECT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

cd "$PROJECT_DIR"

git fetch origin
git checkout "$BRANCH"
# Stop resource-heavy services to free up RAM/CPU during the pull
docker compose stop api frontend prometheus grafana cadvisor || true

docker compose pull api frontend
docker compose up --no-build -d --remove-orphans
docker image prune -f
docker compose ps
