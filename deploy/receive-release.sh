#!/usr/bin/env sh
set -eu
# Этот файл устанавливается в /opt/history и вызывается ограниченным SSH-ключом.
case "${SSH_ORIGINAL_COMMAND:-}" in
  "deploy "*) revision=${SSH_ORIGINAL_COMMAND#deploy } ;;
  *) echo "Разрешена только команда deploy <commit>" >&2; exit 1 ;;
esac
[ "${#revision}" -eq 40 ] || exit 1
case "$revision" in *[!0-9a-f]*) exit 1 ;; esac
exec 9>/opt/history/deploy.lock
flock 9
release="/opt/history/releases/$revision"
mkdir -p "$release"
tar -xzf - --no-same-owner -C "$release"
ln -sfn /opt/history/.env.production "$release/.env.production"
cd "$release"
sh deploy.sh
ln -sfn "$release" /opt/history/current
