#!/bin/sh
docker-compose -f docker-compose.yml build backend
docker-compose -f docker-compose.yml run --rm --no-deps backend python manage.py collectstatic --noinput
docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose.yml exec backend python manage.py makemigrations
docker-compose -f docker-compose.yml exec backend python manage.py migrate
docker-compose -f docker-compose.yml exec backend python manage.py test core.tests

if [ -n "$(docker images -f "dangling=true" -q)" ]; then
  docker rm -v $(docker images -f "dangling=true" -q)
fi
