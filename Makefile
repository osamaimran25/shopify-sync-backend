.PHONY: help setup up down restart shell migrate createsuperuser test lint format

## Show this help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Install requirements inside virtualenv
	pip install -r requirements/local.txt

up: ## Start the docker containers
	docker-compose up -d --build

down: ## Stop the docker containers
	docker-compose down

restart: down up ## Restart the docker containers

shell: ## Open Django shell inside Docker container
	docker-compose exec web python manage.py shell

migrate: ## Apply migrations
	docker-compose exec web python manage.py migrate

createsuperuser: ## Create a Django superuser
	docker-compose exec web python manage.py createsuperuser

test: ## Run Django tests
	docker-compose exec web python manage.py test

lint: ## Run flake8
	flake8 .

format: ## Auto-format code using black
	black .
