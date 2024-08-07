from punq import Container
from pytest import fixture

from app.infrastructure.repositories.messages import BaseChatRepository
from app.services.mediator import Mediator
from tests.fixtures import init_test_container


@fixture(scope="function")
def container() -> Container:
    return init_test_container()


@fixture(scope="function")
def chat_repository(container: Container) -> BaseChatRepository:
    return container.resolve(BaseChatRepository)


@fixture(scope="function")
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)
