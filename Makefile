.PHONY: env run user

env:
	cp .env.example .env

run:
	docker-compose up -d

user:
	docker-compose exec web python manage.py createsuperuser
