from punq import Container, Scope

from app.infrastructure.repositories.messages.base import BaseChatRepository
from app.infrastructure.repositories.messages.memory import (
    MemoryChatRepository,
)
from app.services.init import _init_container


def init_test_container() -> Container:
    container = _init_container()
    container.register(
        BaseChatRepository, MemoryChatRepository, scope=Scope.singleton
    )
    return container
