#!/bin/sh
. ./scripts/logger.sh


if [ "x$ENVIRONMENT" = 'xdevelopment' ]; then
    log_info "Run in development mode"
    python src/gabgabgurus/manage.py runserver "${APP_HOST}":"${APP_PORT}"
else
    log_info "Run in production mode"
    daphne -b "${APP_HOST}" -p "${APP_PORT}" src.gabgabgurus.config.asgi:application
fi
