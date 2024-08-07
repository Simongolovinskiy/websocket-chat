from app.infrastructure.repositories.messages import BaseChatRepository
from app.services.mediator import Mediator
from punq import Container
from pytest import fixture
from tests.fixtures import init_test_container


@fixture()
def container() -> Container:
    return init_test_container()


@fixture()
def chat_repository(container: Container) -> BaseChatRepository:
    return container.resolve(BaseChatRepository)


@fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)
