#!/bin/sh

if [ "$ENVIRONMENT" = "production" ]; then
    echo "Running in production mode"
    python manage.py migrate
    python manage.py loaddata providers.json
    exec gunicorn -c gunicorn.conf.py
elif [ "$ENVIRONMENT" = "development" ]; then
    echo "Running in development mode"
    exec python manage.py runserver 0.0.0.0:8000
else
    echo "ENVIRONMENT variable is not set"
fi