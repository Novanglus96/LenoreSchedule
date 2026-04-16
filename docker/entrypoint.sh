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

# Ensure the app user owns the logs directory, even if the volume was
# created by an older container run as root.
chown -R app:app /home/app/web/logs

python manage.py migrate --no-input

# If using SQLite, the db file is created by migrate (running as root).
# Chown it so the app user can write to it.
chown app:app /home/app/web/db.sqlite3 2>/dev/null || true

python manage.py collectstatic --no-input

if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" || true
fi

python manage.py load_version_fixture

exec supervisord -c /etc/supervisord.conf
