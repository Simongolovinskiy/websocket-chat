from app.application.api.entrypoint import create_app
from app.services.init import init_container
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture
from tests.fixtures import init_test_container


@fixture
def app() -> FastAPI:
    app = create_app()
    app.dependency_overrides[init_container] = init_test_container
    return app


@fixture
def test_app(app: FastAPI) -> TestClient:
    return TestClient(app=app)
