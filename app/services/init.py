from functools import lru_cache

from punq import Container, Scope

from app.infrastructure.repositories.messages import (
    MemoryChatRepository,
    BaseChatRepository,
)
from app.services.commands.messages import CreateChatCommand, CreateChatCommandHandler
from app.services.mediator import Mediator


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(BaseChatRepository, MemoryChatRepository, scope=Scope.singleton)
    container.register(CreateChatCommandHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand,
            [container.resolve(CreateChatCommandHandler)]
        )
        return mediator

    container.register(Mediator, factory=init_mediator)
    return container
