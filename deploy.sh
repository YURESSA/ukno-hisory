#!/usr/bin/env sh

set -eu

BRANCH="${1:-branch-for-deploy}"
PROJECT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

cd "$PROJECT_DIR"

git fetch origin
git checkout "$BRANCH"
git reset --hard "origin/$BRANCH"

docker compose pull api frontend
docker compose up -d --remove-orphans
docker image prune -f
docker compose ps
