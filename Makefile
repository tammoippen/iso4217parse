.PHONY: fmt check test

fmt:
	uv run ruff format .
	uv run ruff check --fix .

check:
	uv run ruff format --check .
	uv run ruff check .
	uv run mypy iso4217parse

test:
	PYTHONDEVMODE=1 uv run pytest -vvv -s
