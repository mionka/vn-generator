ifeq ($(shell test -e '.env' && echo -n yes),yes)
	include .env
endif


ifndef APP_PORT
override APP_PORT = 8000
endif

ifndef APP_HOST
override APP_HOST = 127.0.0.1
endif

args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
MESSAGE = "No such command (or you pass two or many targets to ). List of possible commands: make help"
else
MESSAGE = "Done"
endif

APPLICATION_NAME = app
TEST = poetry run python3 -m pytest --verbosity=2 --showlocals --log-level=DEBUG
CODE = src/$(APPLICATION_NAME)
DOCKER_RUN = docker run -p 8000:8000 -it --env-file .env $(APPLICATION_NAME)

# Commands
env:  ##@Environment Создать .env файл из семпла
	@$(eval SHELL:=/bin/bash)
	@cp .env.sample .env
	@echo "SECRET_KEY=$$(openssl rand -hex 32)" >> .env

alembic:  ##@Database Add alembic
	cd src/$(APPLICATION_NAME)/db && alembic init migration

db:  ##@Database Create database with docker-compose
	docker-compose -f docker-compose.yml up -d --remove-orphans

lint:  ##@Code Check code with pylint
	poetry run python3 -m pylint $(CODE)

format:  ##@Code Reformat code with isort and black
	poetry run python3 -m isort $(CODE)
	poetry run python3 -m black $(CODE)

migrate:  ##@Database Do all migrations in database
	cd src/$(APPLICATION_NAME)/db && alembic upgrade $(args)

run:  ##@Application Run application server
	poetry run python3 -m $(APPLICATION_NAME)

revision:  ##@Database Create new revision file automatically with message
	cd src/$(APPLICATION_NAME)/db && alembic revision --autogenerate -m $(message)

clean:  ##@Code Clean directory from garbage files
	rm -fr *.egg-info dist

%::
	echo $(MESSAGE)
