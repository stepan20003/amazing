PYTHON = poetry run python3
MAIN_SCRIPT = a_maze_ing.py
CONFIG_FILE = config.txt

.PHONY: install run debug clean lint lint-strict build

install:
	poetry install

run:
	$(PYTHON) $(MAIN_SCRIPT) $(CONFIG_FILE)

debug:
	poetry run python3 -m pdb $(MAIN_SCRIPT) $(CONFIG_FILE)

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache dist
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

lint:
	poetry run flake8 .
	poetry run mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	poetry run flake8 .
	poetry run mypy --strict .

build:
	poetry build
	cp dist/mazegen-1.0.0* .