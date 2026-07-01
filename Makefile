PYTHON = poetry run python3

CONFIG_FILE = config.txt
MAIN = mazegen/a_maze_ing.py


all: install build run

install:
	poetry install

build:
	poetry build

run:
	$(PYTHON) $(MAIN) $(CONFIG_FILE)

debug:
	poetry run python3 -m pdb $(MAIN) $(CONFIG_FILE)

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache dist
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	poetry run flake8 .
	poetry run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	poetry run flake8 .
	poetry run mypy  --strict .

.PHONY: install run debug clean lint lint-strict build all
