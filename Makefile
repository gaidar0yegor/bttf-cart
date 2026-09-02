.PHONY: install test lint typecheck run-api run-cli

install:
	poetry install --with dev

test:
	poetry run pytest

lint:
	poetry run ruff check .

typecheck:
	poetry run mypy src

run-api:
	poetry run uvicorn bttf.api:app --reload --port 8000

run-cli:
	@echo "Usage: echo 'Back to the Future 1' | make run-cli"
	poetry run python -m bttf.cli
