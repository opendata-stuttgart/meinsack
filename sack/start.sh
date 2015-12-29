#!/bin/bash
export DJANGO_SETTINGS_MODULE=sack.settings.production
export PYTHONUNBUFFERED=0
mkdir -p /home/uid1000/sack
mkdir -p /home/uid1000/sack/logs
mkdir -p /home/uid1000/sack/run
chmod -R 777 /home/uid1000/sack/run
python3 manage.py migrate
python3 manage.py collectstatic --noinput
exec uwsgi --http-socket 0.0.0.0:8010 --wsgi-file /opt/code/sack/sack/wsgi.py --master --processes 4 --threads 2
#gunicorn sack.wsgi:application --log-level=info --bind=unix:/home/uid1000/meinsack/run/server.sock -w 3
