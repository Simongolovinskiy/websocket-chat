from punq import Container, Scope

from app.infrastructure.repositories.messages.base import BaseChatsRepository
from app.infrastructure.repositories.messages.memory import MemoryChatsRepository
from app.services.init import _init_container


def init_test_container() -> Container:
    container = _init_container()
    container.register(BaseChatsRepository, MemoryChatsRepository, scope=Scope.singleton)
    return container
