from functools import lru_cache

from app.infrastructure.repositories.messages import (
    BaseChatRepository,
    MemoryChatRepository,
)
from app.services.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
)
from app.services.mediator import Mediator
from punq import Container, Scope


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(
        BaseChatRepository, MemoryChatRepository, scope=Scope.singleton
    )
    container.register(CreateChatCommandHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand, [container.resolve(CreateChatCommandHandler)]
        )
        return mediator

    container.register(Mediator, factory=init_mediator)
    return container
