#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 1
done

echo "PostgreSQL started, migrating..."

python manage.py migrate

echo "Waiting for Elasticsearch"

while ! nc -z $ELASTICSEARCH_HOST $ELASTICSEARCH_PORT; do
    sleep 1
done

echo "Initializing Elasticsearch"

python setup_elasticsearch.py

python manage.py crontab add
python manage.py crontab show

exec "$@"