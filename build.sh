#!/bin/bash
if [[$CREATE_SUPERUSER]];
then
    echo "aefawfwafawf"
    python manage.py createsuperuser --no-input
fi
gunicorn backend.wsgi