makemigrations:
	python ./CIT_STAFF/manage.py makemigrations

migrate:
	python ./CIT_STAFF/manage.py migrate

runserver:
	python ./CIT_STAFF/manage.py runserver

build:
	docker compose -f docker-compose.yml build

up:
	docker compose -f docker-compose.yml up -d

down:
	docker compose -f docker-compose.yml down

.PHONY: makemigrations migrate runserver build up down
