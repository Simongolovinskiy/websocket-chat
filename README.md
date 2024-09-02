![Repository Top Language](https://img.shields.io/github/languages/top/Simongolovinskiy/websocket-chat)
![Python version](https://img.shields.io/badge/python-3.10-blue.svg)
![Github Repository Size](https://img.shields.io/github/repo-size/Simongolovinskiy/websocket-chat)
![Github Open Issues](https://img.shields.io/github/issues/Simongolovinskiy/websocket-chat)
![License](https://img.shields.io/badge/license-MIT-green)
![GitHub last commit](https://img.shields.io/github/last-commit/Simongolovinskiy/websocket-chat)
![GitHub contributors](https://img.shields.io/github/contributors/Simongolovinskiy/websocket-chat)
![Simply the best](https://img.shields.io/badge/simply-the%20best%20%3B%29-orange)

<img align="right" width="50%" src="./images/image.jpg">

# Websocket Chat

## Description

Chat based on websocket technology, message in chat
are translating in Kafka topics, and contains in NoSQL database -
MongoDB. Based on domain driven design
concept + clean architecture (example: you can easily change
MongoDB to PostgreSQL without much pain and rewriting tones of code), There are some routes which are implementing
CRUD operations with chats and messages data structures.

## Solution notes

- :trident: clean architecture (Also based on CQRS principle)
- :book: DDD layout
- :cd: docker compose + Makefile included
- :card_file_box: Documentation and some details included in Swagger
- :white_check_mark: tests with mocks included
- :boom: Users interfaces are building from YAML files, you just need to go to:
- ```http://localhost:8090/ - Kafka ui```
- ```http://localhost:28081/ - Mongo express```
- ```http://localhost:8000/api/docs - Swagger```

## HOWTO

- run with `make all`
- test with `make test`
- make logs in main app with `make app-logs`
- execute some scripts in main app with `make app-shell`

## The example of kafka ui working in live mode

<img src="./images/make-run.png">
