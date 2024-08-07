import pytest
from faker import Faker
from fastapi import FastAPI
from httpx import Response
from starlette import status
from starlette.testclient import TestClient


def test_route_create_chat_success(
    app: FastAPI, test_app: TestClient, faker: Faker
) -> None:
    title = faker.text(max_nb_chars=15)
    url = app.url_path_for("create_chat_handler")
    response: Response = test_app.post(url, json={"title": title})
    assert response.is_success
    data = response.json()
    assert data.get("title") == title


def test_route_create_chat_fail(
    app: FastAPI, test_app: TestClient, faker: Faker
) -> None:
    title = faker.text(max_nb_chars=700)
    url = app.url_path_for("create_chat_handler")
    response: Response = test_app.post(url, json={"title": title})
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    data = response.json()
    assert data.get("detail").get("error")


def test_route_create_chat_fail_empty_text(
    app: FastAPI,
    test_app: TestClient,
) -> None:
    url = app.url_path_for("create_chat_handler")
    response: Response = test_app.post(url, json={"title": ""})
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    data = response.json()
    assert data.get("detail").get("error")
