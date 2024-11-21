#!/bin/sh

sleep 10

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    echo "nc -z $SQL_HOST $SQL_PORT;"
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

#python manage.py flush --no-input
#python manage.py migrate

exec "$@"
