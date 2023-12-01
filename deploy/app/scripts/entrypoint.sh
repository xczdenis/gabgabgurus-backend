#!/bin/sh
set -e

. ./scripts/logger.sh

./scripts/wait-dependencies.sh

. ./.venv/bin/activate

log_info "Upgrade database"
python src/gabgabgurus/manage.py migrate --noinput
echo ""

log_info "Collect static"
python src/gabgabgurus/manage.py collectstatic --noinput
echo ""

log_info "Create superuser"
python src/gabgabgurus/manage.py create_superuser
echo ""

log_info "Create languages"
python src/gabgabgurus/manage.py create_languages
echo ""

log_info "Create countries"
python src/gabgabgurus/manage.py create_countries
echo ""

./scripts/start.sh

exec "$@"
