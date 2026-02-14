.ONESHELL:
SHELL := bash
.DEFAULT_GOAL := help
OS := $(shell uname)

.PHONY: help build_and_test build_wheel clean deploy_test deploy_prod pip_install pip_install_dev test check mypy_check install create_venv rebuild_venv run_test_uvicorn

PYTHON_VERSION=3.14

build_and_test: clean build_wheel pip_install test ## Build wheel, install, and execute tests

build_wheel: ## build the wheel for this package
	uv run python -m build

clean: ## clean out dist/ directory
	rm -rf dist/*

deploy_test: ## run all checks, build dist files, upload to test pypi
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy hyperborea3 tests
	rm -f dist/*
	uv run python -m build
	uv run twine check dist/*
	uv run twine upload --repository hyperborea3test dist/*

deploy_prod: ## run all checks, build dist files, upload to prod pypi
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy hyperborea3 tests
	rm -f dist/*
	uv run python -m build
	uv run twine check dist/*
	uv run twine upload --repository hyperborea3prod dist/*

test_wheel_install: ## pip install this package wheel
	uv pip install dist/hyperborea3-*-py3-none-any.whl

test: ## Run pytest tests
	uv run pytest --cov-report term-missing tests/

check: ## Run all linting/formatting checks
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy hyperborea3 scripts tests

mypy_check: ## Run mypy type checker
	uv run mypy hyperborea3 scripts tests

install: ## install/reinstall all packages in the environment
	uv sync --all-extras
	uv run pre-commit install

create_venv: ## create virtualenv for this project
	uv venv --python=${PYTHON_VERSION}

rebuild_venv: ## rebuild project virtualenv from scratch
	rm -rf .venv
	uv sync --python=${PYTHON_VERSION} --all-extras
	uv run pre-commit install

run_test_uvicorn: ## Run fastapi/uvicorn test server
	uv run uvicorn main:app --reload

help: ## Generate and display help info on make commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
