.ONESHELL:
SHELL := bash
.DEFAULT_GOAL := help
OS := $(shell uname)

.PHONY: \
	help \
	activate \
	build_wheel \
	clean \
	deploy_test \
	deploy_prod \
	test \
	check \
	mypy_check \
	install \
	create_venv \
	upgrade_deps \
	run_test_uvicorn \
	run_test_docker \
	install_uv

PYTHON_VERSION=3.14

activate: ## Show how to activate/deactivate the virtualenv for this project
	@echo "To activate the virtualenv, run: source .venv/bin/activate"
	@echo "To deactivate the virtualenv, run: deactivate"

build_wheel: ## build the wheel for this package
	uv build

clean: ## clean out dist/ directory
	rm -rf dist/*

deploy_test: ## run all checks, build dist files, upload to test pypi
	$(MAKE) check
	uv build --clear
	uv run uv-publish --repository hyperborea3test

deploy_prod: ## run all checks, build dist files, upload to prod pypi
	@echo "prod deployment is automatic on merge to main branch via GitHub Actions workflow (publish.yml)."

test: ## Run pytest tests
	uv run pytest --cov-report term-missing tests/

check: ## Run all linting/formatting checks
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy hyperborea3 scripts tests

mypy_check: ## Run mypy type checker
	uv run mypy hyperborea3 scripts tests

install: ## install/reinstall all packages in the environment
	uv sync --python=${PYTHON_VERSION} --all-extras --frozen
	uv run pre-commit install

create_venv: ## create virtualenv for this project from scratch
	rm -rf .venv
	uv sync --python=${PYTHON_VERSION} --all-extras --frozen
	uv run pre-commit install

upgrade_deps: ## upgrade all dependencies to latest versions and update uv.lock
	uv sync --python=${PYTHON_VERSION} --all-extras --upgrade

run_test_uvicorn: ## Run fastapi/uvicorn test server
	uv run uvicorn main:app --reload

run_test_docker: ## Run test server in docker container
	docker build -t hyperborea3 .
	docker run -p 8000:8000 hyperborea3

install_uv: ## Install or update uv
	curl -LsSf https://astral.sh/uv/install.sh | sh

help: ## Generate and display help info on make commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
