from pytest import fixture

from app.services.mediator import Mediator
from app.services.init import init_mediator
from app.infrastructure.repositories.messages import BaseChatRepository, MemoryChatRepository


@fixture
def chat_repository() -> MemoryChatRepository:
    return MemoryChatRepository()


@fixture
def mediator(chat_repository: BaseChatRepository) -> Mediator:
    mediator = Mediator()
    init_mediator(mediator=mediator, chat_repository=chat_repository)
    return mediator
