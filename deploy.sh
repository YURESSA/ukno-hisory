#!/usr/bin/env sh

set -eu

BRANCH="${1:-branch-for-deploy}"
PROJECT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

cd "$PROJECT_DIR"

git fetch origin
git checkout "$BRANCH"
git reset --hard "origin/$BRANCH"

docker compose up --build -d --remove-orphans
docker image prune -f
docker compose ps
