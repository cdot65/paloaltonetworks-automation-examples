.PHONY: clean format lint typecheck test check

clean:
	find . -type d -name __pycache__ -o -name "*.pyc" -o -name "*.pyo" -o -name ".pytest_cache" | xargs rm -rf
	rm -rf .coverage htmlcov .mypy_cache

format:
	poetry run black .
	poetry run isort .
	poetry run ruff check --fix .

lint:
	poetry run flake8 .
	poetry run ruff check .

typecheck:
	poetry run mypy .

test:
	poetry run pytest -v

check: format lint typecheck
	@echo "All checks completed"

run:
	poetry run python app.py
