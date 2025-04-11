#!/bin/sh

# Применяем миграции
DJANGO_SETTINGS_MODULE="core.settings.dev" python manage.py makemigrations && \
DJANGO_SETTINGS_MODULE="core.settings.dev" python manage.py migrate

exec "$@"