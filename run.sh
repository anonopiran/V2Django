#/bin/bash

case $1 in
serve) gunicorn V2Django.wsgi ;;
collect) python manage.py collectstatic --noinput ;;
migrate) python manage.py migrate --noinput;;
esac
exit 0
