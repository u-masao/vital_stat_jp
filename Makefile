.PHONY: lint test

PROJECT_NAME=vital_statistics_jp

lint:
	poetry run isort $(PROJECT_NAME) tests
	poetry run black $(PROJECT_NAME) tests -l 79
	poetry run flake8 $(PROJECT_NAME) tests

test: lint
	poetry run pytest -s
