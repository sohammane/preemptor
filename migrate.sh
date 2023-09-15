# assume backend service is running
docker-compose run web-server python manage.py makemigrations
docker-compose run web-server python manage.py migrate
