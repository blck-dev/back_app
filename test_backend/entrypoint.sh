#!/bin/sh
# to verify that Postgres is healthy
# before applying the migrations and running the Django development server

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "Hourra!! PostgreSQL started successfully"
fi

python3 manage.py flush --no-input
python3 manage.py makemigrations
python3 manage.py migrate --noinput
python3 manage.py create_xof_asset
python3 manage.py collectstatic --no-input --clear
export DJANGO_SUPERUSER_EMAIL=blck.dev@ept.sn
export DJANGO_SUPERUSER_PASSWORD=Fermat1976
python3 manage.py createsuperuser --no-input

exec "$@"
