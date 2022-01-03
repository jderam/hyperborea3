SHELL := bash
.DEFAULT_GOAL := help
OS := $(shell uname)

.PHONY: help build run deploy stop test format gen-requirements

build_and_test: build_wheel pip_install test ## Build wheel, install, and execute tests

build_wheel: ## build the wheel for this package
	python setup.py sdist bdist_wheel

pip_install: ## pip install this package
	pip install dist/hyperborea-*-py3-none-any.whl --force-reinstall

test: ## Run pytest tests
	python -m pytest tests

gen_requirements_txt: ## Generate a new requirements.txt file
	pip-compile requirements.in > requirements.txt

run_test_flask: ## Run flask test server
	FLASK_APP=app
	FLASK_DEBUG=1
	flask run

d_build: ## Build the docker container
	docker build -t hyperborea-app .

d_run: ## Run the docker container
	docker run --name hyperborea-tools --detach --publish 8000:8000 hyperborea-app

d_build_and_run: d_build d_run ## build AND run!!!

d_stop: ## Stop running docker container
	docker stop hyperborea-tools

help: ## Generate and display help info on make commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
