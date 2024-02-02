#!/bin/bash
if [[ $CREATE_SUPERUSER ]];
then
    echo "aefawfwafawf"
    python manage.py createsuperuser --no-input
fi

python manage.py collectstatic

gunicorn backend.wsgi