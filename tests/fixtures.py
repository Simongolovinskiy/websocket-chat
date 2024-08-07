from app.infrastructure.repositories.messages import (
    BaseChatRepository,
    MemoryChatRepository,
)
from app.services.init import _init_container
from punq import Container, Scope


def init_test_container() -> Container:
    container = _init_container()
    container.register(
        BaseChatRepository, MemoryChatRepository, scope=Scope.singleton
    )
    return container
