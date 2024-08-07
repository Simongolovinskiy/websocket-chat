from punq import Container, Scope

from app.infrastructure.repositories.messages import MemoryChatRepository, BaseChatRepository
from app.services.init import _init_container


def init_test_container() -> Container:
    container = _init_container()
    container.register(BaseChatRepository, MemoryChatRepository, scope=Scope.singleton)
    return container
