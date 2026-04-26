.PHONY: run test requirements migrate

run:
	python manage.py runserver

test:
	python -m pytest -v

requirements:
	pip install -r requirements.txt

migrate:
	python manage.py migrate