DC = docker-compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker/app.yaml
APP_CONTAINER = main-app
STORAGE = docker/storages.yaml
MESSAGING = docker/messaging.yaml
MESSAGE_CONTAINER = main-zookeeper

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: message
message:
	${DC} -f ${MESSAGING} ${ENV} up --build -d

.PHONY: message-logs
message-logs:
	${DC} -f ${MESSAGING} logs -f

.PHONY: storages
storages:
	${DC} -f ${STORAGE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: message-down
message-down:
	${DC} -f ${MESSAGING} down

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGE} down

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash


.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: test
ifeq ($(OS),Windows_NT)
	test:
		${EXEC} ${APP_CONTAINER} winpty pytest
else
	test:
		${EXEC} ${APP_CONTAINER} pytest
endif

.PHONY: all
all:
	${DC} -f ${STORAGE} -f ${APP_FILE} -f ${MESSAGING} ${ENV} up --build -d
