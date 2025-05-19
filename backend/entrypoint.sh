#!/bin/sh

# Django のマイグレーションを先に実行
python manage.py migrate --noinput

# 必要なら collectstatic も
python manage.py collectstatic --noinput

# 最後にアプリを起動
exec gunicorn config.wsgi:application -b 0.0.0.0:$PORT
