#!/bin/sh

set -e

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."
    while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
        sleep 0.1
    done
    echo "PostgreSQL started"
fi

cd /home/app/web

python manage.py migrate --no-input

# If using SQLite, the db file is created by migrate (running as root).
# Chown the db file and its parent directory so the app user can write to it.
# SQL_DATABASE may point to a custom path (e.g. inside a named volume directory).
DB_FILE="${SQL_DATABASE:-/home/app/web/db.sqlite3}"
chown -R app:app "$(dirname "$DB_FILE")" 2>/dev/null || true

python manage.py collectstatic --no-input

if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" || true
fi

python manage.py load_version_fixture

# Re-chown logs after management commands (they run as root and create log
# files that gunicorn's app user would otherwise be unable to write to).
chown -R app:app /home/app/web/logs

exec supervisord -c /etc/supervisord.conf
