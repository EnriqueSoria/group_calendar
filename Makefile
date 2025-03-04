PROJECT = web

all: build up

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down --remove-orphans

os-shell:
	docker compose -f docker compose.yml run --rm --entrypoint "bash" $(PROJECT)

makemigrations:
	docker compose -f docker compose.yml run --rm --entrypoint "python manage.py makemigrations" $(PROJECT)

migrate:
	docker compose -f docker compose.yml run --rm --entrypoint "python manage.py migrate" $(PROJECT)
