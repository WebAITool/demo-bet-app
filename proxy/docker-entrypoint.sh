#!/bin/sh
set -e

if [ "${COMPOSE_PROFILES}" = "api" ]; then
  BACKEND_SERVICE_URL="backend:8000"
else
  BACKEND_SERVICE_URL="mock:3000"
fi

echo "Entrypoint: Профиль='${COMPOSE_PROFILES}', Целевой бэкенд='${BACKEND_SERVICE_URL}'"

export BACKEND_SERVICE_URL

envsubst '${BACKEND_SERVICE_URL}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

echo "--- Финальный конфиг NGINX ---"
cat /etc/nginx/conf.d/default.conf
echo "------------------------------"

exec nginx -g 'daemon off;'
