.PHONY: fmt check test

fmt:
	poetry run ruff format .
	poetry run ruff check --fix .

check:
	poetry run ruff format --check .
	poetry run ruff check .
	poetry run mypy iso4217parse

test:
	PYTHONDEVMODE=1 poetry run pytest -vvv -s
