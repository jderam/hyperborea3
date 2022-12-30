SHELL := bash
.DEFAULT_GOAL := help
OS := $(shell uname)

.PHONY: help build run deploy stop test format gen-requirements

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
	python -m pytest

check: ## Run all linting/formatting checks
	black . --check
	flake8
	mypy hyperborea3 tests

mypy_check: ## Run mypy type checker
	mypy hyperborea3 tests

gen_requirements: ## Generate new requirements files
	pip-compile --upgrade -o requirements.txt pyproject.toml
	pip-compile --upgrade --extra dev -o requirements_dev.txt pyproject.toml
	pip-compile --upgrade --extra test -o requirements_test.txt pyproject.toml

resync_requirements: ## reinstall all packages in the environment
	pip-sync requirements.txt requirements_dev.txt requirements_test.txt
	python -m pip install -e . --force-reinstall
	pre-commit install

run_test_uvicorn: ## Run fastapi/uvicorn test server
	uvicorn main:app --reload

d_build: ## Build the docker container
	# docker rm hyperborea-tools
	docker build -t hyperborea-app .

d_run: ## Run the docker container
	docker run --name hyperborea-tools --detach --rm --publish 8000:8000 hyperborea-app

d_build_and_run: d_build d_run ## build AND run!!!

d_stop: ## Stop running docker container
	docker stop hyperborea-tools

help: ## Generate and display help info on make commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
