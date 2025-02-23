SHELL = /bin/bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
.DEFAULT_GOAL := help

include .env
export $(shell sed 's/=.*//' .env)
export PYTHONPATH
export PIPENV_VENV_IN_PROJECT=1

PYTHON := python3
PIP := $(PYTHON) -m pip
PIPENV := $(PYTHON) -m pipenv

APP_NAME = peanut-butter-payroll:0.0.1
APP_DIR = backend
TEST_SRC = $(APP_DIR)/tests.py

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN \
	{FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

### Local commands ###
venv:
	$(PIP) install -U pipenv
	$(PIPENV) shell

install-packages:
	$(PIPENV) install --dev

run-local:
	$(PYTHON) -m uvicorn --chdir $(APP_DIR) main:app --reload

migrate:
	$(PYTHON) -m alembic $(APP_DIR) upgrade head

### Docker commands ###
up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f

docker-migrate:
	docker compose exec backend python -m alembic $(APP_DIR) upgrade head

copy-env:
	exec cp .env.example .env

test:
	docker compose exec backend python -m pytest $(TEST_SRC)

.PHONY: help venv install-packages run-local migrate test up down
	test-docker copy-env docker-migrate logs
