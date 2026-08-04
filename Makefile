.SILENT:
.PHONY: install run debug clean lint lint-strict

MAIN := Fly-In
VENV := $(MAIN)-venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
FLAKE8 := $(VENV)/bin/flake8
MYPY := $(VENV)/bin/mypy
ModuleFile := FlyIn

MAP := "maps/easy/01_linear_path.txt"

install:
	@echo "Installing Project $(MAIN)"
	python3 -m venv $(VENV)
	chmod 777 $(VENV)/bin/activate 
	$(VENV)/bin/activate
	$(PIP) install --upgrade pip
	$(PIP) install poetry
	$(VENV)/bin/poetry config cache-dir $(VENV)/poetrycache
	$(VENV)/bin/poetry install
	$(VENV)/bin/uv sync
run:
	echo "Running Project $(MAIN)"
	$(VENV)/bin/uv run python -m src $(MAP) 

debug:
	$(PYTHON) -m pdb $(MAIN)

lclean:
	rm -rf __pycache__ src/__pycache__ .mypy_cache .pytest_cache $(ModuleFile)/__pycache__ .vscode $(RESULTFILE) llm_sdk/__pycache__

clean:
	rm -rf $(VENV)
	rm -rf __pycache__ src/motor/Instances/__pycache__ src/motor/__pycache__ src/drone/__pycache__ src/__pycache__ .mypy_cache .pytest_cache $(ModuleFile)/__pycache__ .vscode $(RESULTFILE) .venv llm_sdk/__pycache__ poetry.lock uv.lock

lint:
	$(MYPY) ./src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	$(FLAKE8) ./src

lint-strict:
	$(MYPY) ./src --strict
	$(FLAKE8) ./src