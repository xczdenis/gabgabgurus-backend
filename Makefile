DEFAULT_PROJECT_NAME=gabgabgurus-backend

PREFIX_DEV=dev
PREFIX_TEST=test
PREFIX_PROD=prod

CURRENT_ENVIRONMENT_PREFIX=PREFIX_DEV

DOCKER_COMPOSE_MAIN_FILE=docker-compose.yml
DOCKER_COMPOSE_DEV_FILE=docker-compose.dev.yml
DOCKER_COMPOSE_PROD_FILE=docker-compose.prod.yml
DOCKER_COMPOSE_TEST_FILE_NAME=docker-compose.test.yml

COMPOSE_OPTION_START_AS_DEMON=up -d --build
COMPOSE_PROFILE_DEFAULT=""--profile default""

# define standard colors
ifneq (,$(findstring xterm,${TERM}))
	BLACK        := $(shell printf "\033[30m")
	RED          := $(shell printf "\033[31m")
	GREEN        := $(shell printf "\033[32m")
	YELLOW       := $(shell printf "\033[33m")
	PURPLE       := $(shell printf "\033[34m")
	PINK         := $(shell printf "\033[35m")
	BLUE         := $(shell printf "\033[36m")
	ORANGE       := $(shell printf "\033[93m")
	WHITE        := $(shell printf "\033[97m")
	RESET        := $(shell printf "\033[00m")
	INFO         := $(shell printf "\033[36m")
	SUCCESS      := $(shell printf "\033[32m")
	WARNING      := $(shell printf "\033[33m")
	DANGER       := $(shell printf "\033[31m")
else
	BLACK        := ""
	RED          := ""
	GREEN        := ""
	YELLOW       := ""
	BLUE         := ""
	PURPLE       := ""
	ORANGE       := ""
	WHITE        := ""
	RESET        := ""
	INFO         := ""
	SUCCESS      := ""
	WARNING      := ""
	DANGER       := ""
endif

# read env variables from .env
ifneq (,$(wildcard ./.env))
	include .env
	export
endif

# looking for docker-compose files
ifeq (,$(wildcard ./${DOCKER_COMPOSE_PROD_FILE}))
	DOCKER_COMPOSE_PROD_FILE=_
endif
ifeq (,$(wildcard ./${DOCKER_COMPOSE_DEV_FILE}))
	DOCKER_COMPOSE_DEV_FILE=_
endif
ifeq (,$(wildcard ./${DOCKER_COMPOSE_TEST_FILE_NAME}))
	DOCKER_COMPOSE_TEST_FILE=_
else
	DOCKER_COMPOSE_TEST_FILE=${DOCKER_COMPOSE_TEST_FILE_NAME}
endif

# set envs if they are not defined
ifeq ($(PROJECT_NAME),)
	PROJECT_NAME=$(DEFAULT_PROJECT_NAME)
endif
ifeq ($(DOCKER_BUILDKIT),)
	DOCKER_BUILDKIT=1
endif
ifeq ($(ENVIRONMENT),)
	ENVIRONMENT=production
endif
ifeq ($(ENVIRONMENT), development)
   CURRENT_ENVIRONMENT_PREFIX=${PREFIX_DEV}
else
   CURRENT_ENVIRONMENT_PREFIX=${PREFIX_PROD}
endif


define log
	@echo ""
	@echo "${WHITE}----------------------------------------${RESET}"
	@echo "${BLUE}$(strip ${1})${RESET}"
	@echo "${WHITE}----------------------------------------${RESET}"
endef


# Function to check if service is available
define check_service
	@nc -z $(2) $(3) || (echo "${DANGER}ERROR:${RESET} $(1) at ${INFO}$(2):$(3)${RESET} is not available.${RESET}" && exit 1)
endef


# check if the Makefile is available: it should return PONG
.PHONY: ping
ping:
	echo "PONG"


# display info about: current envs, project name etc.
.PHONY: info
info:
	$(call log, INFORMATION (${RED}${CURRENT_ENVIRONMENT_PREFIX}${INFO})${RESET})
	@echo "PROJECT_NAME        = ${INFO}${PROJECT_NAME}${RESET}"
	@echo "ENVIRONMENT         = ${RED}${ENVIRONMENT}${RESET}"
	@echo "DOCKER_IMG_PLATFORM = ${INFO}${DOCKER_IMG_PLATFORM}${RESET}"


# display info about running docker containers, images, volumes
.PHONY: di
di:
	@echo "${INFO}Running containers:${RESET}"
	@docker ps
	@echo "${INFO}All containers:${RESET}"
	@docker ps -a
	@echo "${INFO}All images:${RESET}"
	@docker images
	@echo "${INFO}All volumes:${RESET}"
	@docker volume ls



# check if Postgres is available
.PHONY: check_pg
check_pg:
	$(call check_service,"Postgres",${POSTGRES_HOST},${POSTGRES_PORT})


define run_docker_compose_for_env
	@if [ $(strip ${2}) != "_" ]; then \
		make run_docker_compose_for_env \
			env=$(strip ${1}) \
			override_file="-f ${2}" \
			cmd=$(strip ${3}); \
    else \
		make run_docker_compose_for_env \
			env=$(strip ${1}) \
			cmd=$(strip ${3}); \
    fi
endef
run_docker_compose_for_env:
	@DOCKER_BUILDKIT=${DOCKER_BUILDKIT} \
		COMPOSE_PROJECT_NAME=${PROJECT_NAME} \
		docker compose \
			-f ${DOCKER_COMPOSE_MAIN_FILE} \
			$(strip ${override_file}) \
			$(strip ${cmd})


define run_docker_compose_for_current_env
	@if [ ${CURRENT_ENVIRONMENT_PREFIX} = ${PREFIX_DEV} ]; then \
		if [ "${DOCKER_COMPOSE_DEV_FILE}" != "_" ]; then \
			make run_docker_compose_for_env \
				env=${CURRENT_ENVIRONMENT_PREFIX} \
				override_file="-f ${DOCKER_COMPOSE_DEV_FILE}" \
				cmd="$(strip ${1})"; \
		else \
			make run_docker_compose_for_env \
				env=${CURRENT_ENVIRONMENT_PREFIX} \
				cmd="$(strip ${1})"; \
		fi \
    elif [ ${CURRENT_ENVIRONMENT_PREFIX} = ${PREFIX_PROD} ]; then \
		if [ "${DOCKER_COMPOSE_PROD_FILE}" != "_" ]; then \
			make run_docker_compose_for_env \
				env=${CURRENT_ENVIRONMENT_PREFIX} \
				override_file="-f ${DOCKER_COMPOSE_PROD_FILE}" \
				cmd="$(strip ${1})"; \
		else \
			make run_docker_compose_for_env \
				env=${CURRENT_ENVIRONMENT_PREFIX} \
				cmd="$(strip ${1})"; \
		fi \
    fi
endef


.PHONY: init
init:
	@./src/scripts/init.sh


.PHONY: lint
lint:
	@./src/scripts/lint.sh


.PHONY: format
format:
	@./src/scripts/format.sh


# remove all existing containers, volumes, images
.PHONY: remove
remove:
	@clear
	@echo "${RED}----------------!!! DANGER !!!----------------"
	@echo "Вы собираетесь удалить все неиспользуемые образы, контейнеры и тома."
	@echo "Будут удалены все незапущенные контейнеры, все образы для незапущенных контейнеров и все тома для незапущенных контейнеров"
	@read -p "${ORANGE}Вы точно уверены, что хотите продолжить? [yes/n]: ${RESET}" TAG \
	&& if [ "_$${TAG}" != "_yes" ]; then echo "Nothing happened"; exit 1 ; fi
	docker compose down --rmi all --volumes --remove-orphans && docker system prune -a --volumes --force


# create .env and .env.local files if they are not exist
.PHONY: env
env:
	@if [ -f .env ]; then \
		read -p "File ${GREEN}.env${RESET} already exists. Overwrite it [y/n]:${RESET} " yn; \
        case $$yn in \
            [Yy]* ) cp .env.template .env; echo "File ${GREEN}.env${RESET} has been overwritten!";; \
            * ) echo "Nothing happened";; \
        esac \
    else \
        cp .env.template .env; \
        echo "File ${GREEN}.env${RESET} created from ${GREEN}.env.template${RESET}!"; \
    fi


# stop and remove all running containers
.PHONY: down _down-prod _down-dev _down-test
down:
	$(call log, Down containers (${RED}${CURRENT_ENVIRONMENT_PREFIX}${INFO})${RESET})
	@make _down-prod
	@make _down-dev
	@make _down-test
_down-prod:
	$(call run_docker_compose_for_env, "${PREFIX_PROD}", "${DOCKER_COMPOSE_PROD_FILE}", "${COMPOSE_PROFILE_DEFAULT} down")
	$(call run_docker_compose_for_env, "_", "${DOCKER_COMPOSE_PROD_FILE}", "${COMPOSE_PROFILE_DEFAULT} down")
_down-dev:
	$(call run_docker_compose_for_env, "${PREFIX_DEV}", "${DOCKER_COMPOSE_DEV_FILE}", "${COMPOSE_PROFILE_DEFAULT} down")
	$(call run_docker_compose_for_env, "_", "${DOCKER_COMPOSE_DEV_FILE}", "${COMPOSE_PROFILE_DEFAULT} down")
_down-test:
	$(call run_docker_compose_for_env, "${PREFIX_TEST}", "${DOCKER_COMPOSE_TEST_FILE}", "${COMPOSE_PROFILE_DEFAULT} down")
	$(call run_docker_compose_for_env, "_", "${DOCKER_COMPOSE_TEST_FILE}", "${COMPOSE_PROFILE_DEFAULT} down")


# build and run docker containers in demon mode
.PHONY: run
run: down
	$(call log, Run containers (${RED}${CURRENT_ENVIRONMENT_PREFIX}${INFO})${RESET})
	$(call run_docker_compose_for_current_env, --profile default ${COMPOSE_OPTION_START_AS_DEMON} ${s})


# build and run docker containers in demon mode for db profile
.PHONY: run-db
run-db: down
	$(call log, Run containers for db profile (${CURRENT_ENVIRONMENT_PREFIX}))
	$(call run_docker_compose_for_current_env, --profile db ${COMPOSE_OPTION_START_AS_DEMON} ${s})


# show service's logs (e.g.: make logs s=proxy)
.PHONY: logs _logs
logs:
	@if [ -z "${s}" ]; then \
		read -p "${ORANGE}Container name: ${RESET}" _TAG && \
		make _logs s="$${_TAG}"; \
	else \
	    make _logs s="${s}"; \
	fi
_logs:
	$(call run_docker_compose_for_current_env, logs -f ${s})


# run bash into container
.PHONY: bash bashs
bash:
	@read -p "${ORANGE}Container name: ${RESET}" _TAG && \
	if [ "_$${_TAG}" != "_" ]; then \
		make bashs s="$${_TAG}"; \
	else \
	    echo aborting; exit 1; \
	fi
bashs:
	$(call run_docker_compose_for_current_env, exec -it ${s} bash)


# run sh into container (e.g. for Redis)
.PHONY: sh shs
sh:
	@read -p "${ORANGE}Container name: ${RESET}" _TAG && \
	if [ "_$${_TAG}" != "_" ]; then \
		make shs s="$${_TAG}"; \
	else \
	    echo aborting; exit 1; \
	fi
shs:
	$(call run_docker_compose_for_current_env, exec -it ${s} sh)


# stop services
.PHONY: stop stops
stop:
	@read -p "(${CURRENT_ENVIRONMENT_PREFIX}) ${ORANGE}Service name (press Enter to stop all services): ${RESET}" _TAG && \
	if [ "_$${_TAG}" != "_" ]; then \
		make stops s="$${_TAG}"; \
	else \
	    make stopall; \
	fi
stops:
	$(call log, Stop containers (${RED}${CURRENT_ENVIRONMENT_PREFIX}${INFO})${RESET})
	$(call run_docker_compose_for_current_env, --profile default stop ${s})
stopall:
	$(call log, Stop containers (${RED}${CURRENT_ENVIRONMENT_PREFIX}${INFO})${RESET})
	$(call run_docker_compose_for_current_env, --profile default stop)


# start services
.PHONY: start starts
start:
	@read -p "(${CURRENT_ENVIRONMENT_PREFIX}) ${ORANGE}Service name (press Enter to start all services): ${RESET}" _TAG && \
	if [ "_$${_TAG}" != "_" ]; then \
		make starts s="$${_TAG}"; \
	else \
	    make starts; \
	fi
starts:
	$(call log, Start containers (${RED}${CURRENT_ENVIRONMENT_PREFIX}${INFO})${RESET})
	$(call run_docker_compose_for_current_env, --profile default start ${s})


# build containers
.PHONY: build build-profile build-all
build:
	@read -p "(${CURRENT_ENVIRONMENT_PREFIX}) ${ORANGE}Profile name (press Enter to build images for all profiles): ${RESET}" _TAG && \
	if [ "_$${_TAG}" != "_" ]; then \
		make build-profile p="$${_TAG}"; \
	else \
	    make build-all; \
	fi
build-profile:
	$(call log, Build images for profile ${p} (${RED}${CURRENT_ENVIRONMENT_PREFIX}${INFO})${RESET})
	$(call run_docker_compose_for_current_env, --profile ${p} build)
build-all:
	$(call log, Build all images (${RED}${CURRENT_ENVIRONMENT_PREFIX}${INFO})${RESET})
	$(call run_docker_compose_for_current_env, --profile default build)


# show docker-compose status
.PHONY: status status-all
status:
	$(call run_docker_compose_for_current_env, ps)
status-all:
	$(call run_docker_compose_for_current_env, ps -a)


# remove all stopped containers/unused images/unused volumes/unused networks
.PHONY: prune prune-с prune-i prune-v prune-n
prune:
	$(call log, Remove all stopped containers)
	docker system prune
prune-c:
	$(call log, Remove all stopped containers)
	docker container prune
prune-i:
	$(call log, Remove all stopped containers)
	docker images prune
prune-v:
	$(call log, Remove all stopped containers)
	docker volume prune
prune-n:
	$(call log, Remove all stopped containers)
	docker network prune


# show docker-compose configuration
.PHONY: config
config:
	$(call log, Docker-compose configuration (${RED}${CURRENT_ENVIRONMENT_PREFIX}${INFO})${RESET})
	$(call run_docker_compose_for_current_env, ${COMPOSE_PROFILE_DEFAULT} config)


# build and run tests in docker
.PHONY: tests-docker
tests-docker: down
	$(call log, Run tests in docker)
	@if [ "${DOCKER_COMPOSE_TEST_FILE}" != "_" ]; then \
		make run_docker_compose_for_env \
			env=${PREFIX_TEST} \
			override_file="-f ${DOCKER_COMPOSE_TEST_FILE}" \
			cmd="--profile default --profile tests build"; \
    	make run_docker_compose_for_env \
			env=${PREFIX_TEST} \
			override_file="-f ${DOCKER_COMPOSE_TEST_FILE}" \
			cmd="--profile default --profile tests run tests"; \
	else \
		echo "${RED}ERROR:${RESET} No such file '${DOCKER_COMPOSE_TEST_FILE_NAME}'. Tests cannot be run."; \
	fi \


.PHONY: tests
tests:
	@cd $(CURDIR) && python -m pytest


# create migrations
.PHONY: makemigrations
makemigrations: check_pg
	@python src/gabgabgurus/manage.py makemigrations


# do migrations - upgrade database
.PHONY: migrate
migrate: check_pg
	@python src/gabgabgurus/manage.py migrate


# create migrations and upgrade database
.PHONY: db-upgrade
db-upgrade: makemigrations migrate


# create superuser
.PHONY: su
su: check_pg
	@python src/gabgabgurus/manage.py create_superuser


# create all countries from init_data/countries_languages.json
.PHONY: init-c
init-c: check_pg
	@python src/gabgabgurus/manage.py create_countries


# create all languages from init_data/countries_languages.json
.PHONY: init-l
init-l: check_pg
	@python src/gabgabgurus/manage.py create_languages

# create new django app
.PHONY: app
app:
	@read -p "${ORANGE}Enter app name (press Enter to exit): ${RESET}" _appname; \
	if [ -z "$$_appname" ]; then \
		echo "No app name provided. Exiting..."; \
	elif [ -d "src/gabgabgurus/$$_appname" ]; then \
		echo "The folder with name ${GREEN}$$_appname${RESET} already exists in ${GREEN}src/gabgabgurus/${RESET}!"; \
	else \
		python src/gabgabgurus/manage.py startapp $$_appname; \
		mv $$_appname src/gabgabgurus/; \
		echo "App ${GREEN}$$_appname${RESET} successfully created into ${GREEN}src/gabgabgurus/${RESET}"; \
	fi


# run django dev server (runserver)
.PHONY: serve
serve: check_pg
	$(call check_service,"Postgres",${POSTGRES_HOST},${POSTGRES_PORT})
	@python src/gabgabgurus/manage.py runserver ${APP_HOST}:${APP_PORT}
