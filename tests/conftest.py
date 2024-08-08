from punq import Container
from pytest import fixture

from app.infrastructure.repositories.messages.base import BaseChatsRepository
from app.services.mediator import Mediator
from tests.fixtures import init_test_container


@fixture()
def container() -> Container:
    return init_test_container()


@fixture()
def chat_repository(container: Container) -> BaseChatsRepository:
    return container.resolve(BaseChatsRepository)


@fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)
