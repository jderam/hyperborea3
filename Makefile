SHELL := bash
.DEFAULT_GOAL := help
OS := $(shell uname)

.PHONY: help build run deploy stop test format gen-requirements

build_and_test: build_wheel pip_install test ## Build wheel, install, and execute tests

build_wheel: ## build the wheel for this package
	python setup.py sdist bdist_wheel

pip_install: ## pip install this package
	pip install dist/hyperborea-*-py3-none-any.whl --force-reinstall

test: ## run tests
	python -m pytest tests

gen_requirements_txt: ## Generate a new requirements.txt file
	pip-compile requirements.in > requirements.txt

run_test_flask: ## Run flask test server
	FLASK_APP=app
	FLASK_DEBUG=1
	flask run

docker_build: ## build the docker container
	docker build -t hyperborea-app .

docker_run: ## run the docker container
	docker run --detach --publish 8000:8000 hyperborea-app

docker_build_and_run: docker_build docker_run ## build AND run!!!

help: ## Generate and display help info on make commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
