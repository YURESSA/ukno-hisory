#!/usr/bin/env sh
# Выполняется вручную на сервере из каталога с этим скриптом и конфигурацией nginx.
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
test "$(id -u)" = 0
command -v nginx >/dev/null
command -v certbot >/dev/null
test -f /opt/history/.env.production
test -f host-nginx-https.conf
mkdir -p /var/www/history-acme /opt/history/backups
stamp=$(date +%Y%m%d-%H%M%S)
cp -p /opt/history/.env.production "/opt/history/backups/env-before-https-$stamp"
cp -a /etc/nginx "/opt/history/backups/nginx-before-https-$stamp"

# Значения остаются в общем env-файле, который использует каждый следующий релиз.
python3 - <<'PY'
from pathlib import Path
path = Path('/opt/history/.env.production')
lines = path.read_text().splitlines()
lines = [line for line in lines if not line.startswith(('HISTORY_HTTP_BIND=', 'HISTORY_HTTP_PORT='))]
lines.extend(['HISTORY_HTTP_BIND=127.0.0.1', 'HISTORY_HTTP_PORT=8080'])
path.write_text('\n'.join(lines) + '\n')
PY

if [ ! -s /etc/letsencrypt/live/vtorchik.ru/fullchain.pem ]; then
    cat > /etc/nginx/sites-available/history <<'NGINX'
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name vtorchik.ru www.vtorchik.ru;
    client_max_body_size 10M;
    location ^~ /.well-known/acme-challenge/ { root /var/www/history-acme; }
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
NGINX
else
    cp host-nginx-https.conf /etc/nginx/sites-available/history
fi
if [ -L /etc/nginx/sites-enabled/default ]; then
    unlink /etc/nginx/sites-enabled/default
fi
ln -sfn /etc/nginx/sites-available/history /etc/nginx/sites-enabled/history
nginx -t
cd /opt/history/current
docker compose --env-file .env.production -f deploy/compose.production.yml up -d --no-deps --wait frontend
systemctl enable --now nginx
systemctl reload nginx

certbot certonly --webroot -w /var/www/history-acme \
    --cert-name vtorchik.ru -d vtorchik.ru -d www.vtorchik.ru \
    --non-interactive --agree-tos --keep-until-expiring

cd - >/dev/null
cp host-nginx-https.conf /etc/nginx/sites-available/history
nginx -t
systemctl reload nginx
mkdir -p /etc/letsencrypt/renewal-hooks/deploy
cat > /etc/letsencrypt/renewal-hooks/deploy/history-nginx <<'HOOK'
#!/usr/bin/env sh
set -eu
nginx -t
systemctl reload nginx
HOOK
chmod 755 /etc/letsencrypt/renewal-hooks/deploy/history-nginx
systemctl enable --now certbot.timer
