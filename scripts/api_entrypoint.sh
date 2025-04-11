#!/bin/sh

wait_for_postgres() {
  # Функция ожидания полного запуска контейнера postgresql
  echo "Ожидание запуска PostgreSQL ..."
  until python scripts/check_db.py; do
    echo "DB еще не готова. Повторная проверка через 2 сек ..."
    sleep 2
  done
}

wait_for_postgres

# Применяем миграции
DJANGO_SETTINGS_MODULE="core.settings.prod" python manage.py makemigrations && \
DJANGO_SETTINGS_MODULE="core.settings.prod" python manage.py migrate

exec "$@"