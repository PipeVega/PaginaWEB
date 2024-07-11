#!/bin/bash
. .venv/bin/activate
python3 manage.py runscript -v3 eliminar_tablas_linux
rm -rf core/migrations
python3 manage.py makemigrations
python3 manage.py makemigrations core
python3 manage.py migrate
python3 manage.py migrate core
