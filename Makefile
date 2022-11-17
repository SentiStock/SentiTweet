docker_compose = docker-compose -f devops/docker-compose.yml

.PHONY: up
up: # Builds, (re)creates, starts, and attaches to containers for a service.
	@$(docker_compose) up -d --build

.PHONY: build
build: # Builds
	@$(docker_compose) build

.PHONY: logs
logs: # View the logs of sentitweet activity
	@$(docker_compose) logs -f --tail=100

.PHONY: shell
shell: # Enter the shell of the docker where sentitweet is running
	docker exec -it sentitweet sh -c "export COLUMNS=`tput cols`; export LINES=`tput lines`; exec bash";

.PHONY: stop
stop: # Stop containers
	@$(docker_compose) stop

.PHONY: down
down: # Stops containers and removes containers, networks, volumes, and images created by up
	@$(docker_compose) down

.PHONY: migrate
migrate: # Execute migrate command in sentitweet container
	docker exec -i sentitweet python manage.py migrate

.PHONY: makemigrations
makemigrations: # Execute makemigrations command in sentitweet container
	docker exec -i sentitweet python manage.py makemigrations
