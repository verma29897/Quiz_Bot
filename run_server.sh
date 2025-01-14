#!/bin/sh

python manage.py makemigrations
python manage.py migrate

python -R manage.py runserver 127.0.0.1:8000
