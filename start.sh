#!/bin/sh

uv run python manage.py migrate --noinput
uv run python manage.py collectstatic --noinput
uv run gunicorn checklist.wsgi:application --bind 0.0.0.0:8000 --log-level info
