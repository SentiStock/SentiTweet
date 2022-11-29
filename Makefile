#File used only during development

include .env
docker_compose = docker-compose -f devops/deployment-from-${IMAGE_SOURCE}.yml
docker_web = docker exec -it sentitweet
docker_db_exec = docker exec -i postgres-db-sentitweet-timescale
docker_db = docker exec -it postgres-db-sentitweet-timescale

.PHONY: up
up: # Builds, (re)creates, starts, and attaches to containers for a service.
	@$(docker_compose) up -d --build

.PHONY: logs
logs: # View the logs of sentitweet activity
	@$(docker_compose) logs -f --tail=100

.PHONY: stop
stop: # Stop containers
	@$(docker_compose) stop

.PHONY: down
down: # Stops containers and removes containers, networks, volumes, and images created by up
	@$(docker_compose) down

.PHONY: shell
shell: # Enter the shell of the docker where sentitweet is running
	@$(docker_web) sh -c "export COLUMNS=`tput cols`; export LINES=`tput lines`; exec bash";

.PHONY: shell-db
shell-db: # Enter the shell of the docker where sentitweet is running
	@$(docker_db) sh -c "export COLUMNS=`tput cols`; export LINES=`tput lines`; exec bash";

.PHONY: migrate
migrate: # Execute migrate command in sentitweet container
	@$(docker_web) python manage.py migrate

.PHONY: makemigrations
makemigrations: # Execute makemigrations command in sentitweet container
	@$(docker_web) python manage.py makemigrations

.PHONY: db-rebuild-migrations
db-rebuild-migrations:
	@$(docker_db_exec) psql -U sentitweet -d dbsentitweet < devops/db/drop_and_create_schema.sql
	@$(docker_db_exec) psql -U sentitweet -d dbsentitweet < database.bak

.PHONY: db-redeploy
db-redeploy: db-rebuild-migrations migrate

.PHONY: install-requirements
install: ## Execute migrate command in sentitweet container
	@$(docker_web) pip install -r /app/requirements.txt