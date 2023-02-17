.ONESHELL:
SHELL := bash
.DEFAULT_GOAL := help
OS := $(shell uname)

.PHONY: help build_and_test build_wheel clean deploy_test deploy_prod pip_install pip_install_dev test check mypy_check compile_req install create_venv rebuild_venv run_test_uvicorn

PYENV_VERSION=3.11.2
VENV_NAME=hyperborea3-venv

build_and_test: clean build_wheel pip_install test ## Build wheel, install, and execute tests

build_wheel: ## build the wheel for this package
	python -m build

clean: ## clean out dist/ directory
	rm -r dist/*

deploy_test: ## run all checks, build dist files, upload to test pypi
	black . --check
	flake8
	mypy hyperborea3 tests
	rm -f dist/*
	python -m build
	twine check dist/*
	twine upload --repository hyperborea3test dist/*

deploy_prod: ## run all checks, build dist files, upload to prod pypi
	black . --check
	flake8
	mypy hyperborea3 tests
	rm -f dist/*
	python -m build
	twine check dist/*
	twine upload --repository hyperborea3prod dist/*

pip_install: ## pip install this package
	python -m pip install dist/hyperborea3-*-py3-none-any.whl --force-reinstall

pip_install_dev: ## pip install in editable mode
	python -m pip install -e . --force-reinstall

test: ## Run pytest tests
	python -m pytest --cov-report term-missing tests/

check: ## Run all linting/formatting checks
	black . --check
	flake8
	mypy hyperborea3 tests

mypy_check: ## Run mypy type checker
	mypy hyperborea3 tests

compile_req: ## Generate new requirements files
	pip-compile --resolver=backtracking --upgrade -o requirements.txt pyproject.toml
	pip-compile --resolver=backtracking --upgrade --extra dev -o requirements_dev.txt pyproject.toml
	pip-compile --resolver=backtracking --upgrade --extra test -o requirements_test.txt pyproject.toml

install: ## install/reinstall all packages in the environment
	python -m pip install -U pip pip-tools
	pip-sync requirements*.txt
	python -m pip install -e . --force-reinstall
	pyenv rehash
	pre-commit install

create_venv: ## create virtualenv for this project
	pyenv install ${PYENV_VERSION} --skip-existing
	pyenv rehash
	pyenv virtualenv-delete --force ${VENV_NAME}
	pyenv virtualenv ${PYENV_VERSION} ${VENV_NAME}
	pyenv local ${VENV_NAME}

rebuild_venv: create_venv install ## rebuild project virtualenv

run_test_uvicorn: ## Run fastapi/uvicorn test server
	uvicorn main:app --reload

help: ## Generate and display help info on make commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
