#!/bin/sh

python manage.py collectstatic --no-input --clear
gunicorn vika_app.wsgi:application --workers 1 --bind 0.0.0.0:8000