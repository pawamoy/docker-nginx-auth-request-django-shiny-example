.PHONY: help
.DEFAULT_GOAL := help

BASH = docker-compose run --rm djangoapp /bin/bash
DEV_BASH = docker-compose -f docker-compose-dev.yml run --rm dev /bin/bash

all: dev-setup build up-no-start migrate superuser up ## Setup, build, init, create super user and start application.

own: ## Chown files and directories (use it without sudo).
	@sudo chown -R $(USER):$(USER) *
	@sudo chown $(USER):$(USER) .*

build: ## Build the images for Django and Shiny.
	@docker-compose build

dev-setup: dev-yarn ## Setup the project for development.

dev-yarn: ## Run yarn in the static folder.
	@$(DEV_BASH) -c "cd djangoapp/static; yarn"

initial-migration: ## Create the initial Django migration.
	@$(BASH) -c "cd djangoapp; ./manage.py makemigrations djangoapp"

migrations: ## Make the subsequent migrations.
	@$(BASH) -c "cd djangoapp; ./manage.py makemigrations"

delete-migrations: ## Delete the migrations.
	@rm -rf djangoapp/djangoapp/migrations

new-migrations: delete-migrations initial-migration ## Delete all migrations and re-create the initial one.

migrate: ## Migrate (create) the database.
	@$(BASH) -c "cd djangoapp; ./manage.py migrate"

up: ## Start the application.
	@docker-compose up

up-no-start: ## Create the containers without starting them.
	@docker-compose up --no-start

down: ## Stop and remove the containers.
	@docker-compose down

superuser: ## Create a Django superuser.
	@$(BASH) -c "cd djangoapp; ./manage.py createsuperuser"

shell: ## Launch a shell in the Django container.
	@$(BASH)

python: ## Launch a Python shell in the Django container.
	@$(BASH) -c "cd djangoapp; ./manage.py shell_plus"

prune: ## Run docker system prune command (use with caution).
	@docker system prune -f

delete-database-volume: down ## Delete the database volume.
	@docker volume rm -f djangdjangoapp_data

help: ## Print this help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort
