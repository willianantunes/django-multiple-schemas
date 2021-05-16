#!/usr/bin/env bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -eu -o pipefail

python manage.py makemigrations
python manage.py migrate
python manage.py seed --create-super-user

python manage.py runserver 0.0.0.0:8000
