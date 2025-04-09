.PHONY: help format lint type check test clean

help:
	@echo "Available commands:"
	@echo "  make format        Format code with black, isort, and ruff"
	@echo "  make lint          Run linters (flake8, ruff)"
	@echo "  make type          Run type checking with mypy"
	@echo "  make check         Run all code quality checks (format, lint, type)"
	@echo "  make test          Run tests"
	@echo "  make clean         Remove build artifacts and cache directories"

format:
	@echo "Formatting code..."
	poetry run black .
	poetry run isort .
	poetry run ruff check --fix .

lint:
	@echo "Running linters..."
	poetry run flake8 .
	poetry run ruff check .

type:
	@echo "Running type checker..."
	poetry run mypy .

check: format lint type
	@echo "All checks completed"

test:
	@echo "Running tests..."
	poetry run pytest

clean:
	@echo "Cleaning up..."
	rm -rf .pytest_cache .ruff_cache .mypy_cache __pycache__ */__pycache__ *.egg-info build dist
