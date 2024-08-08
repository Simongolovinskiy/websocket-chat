from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope

from app.infrastructure.repositories.messages.base import BaseChatRepository
from app.infrastructure.repositories.messages.mongo import (
    MongoDBChatRepository,
)
from app.services.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
)
from app.services.mediator import Mediator
from app.settings.conf import Config


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(Config, instance=Config(), scope=Scope.singleton)
    container.register(CreateChatCommandHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand, [container.resolve(CreateChatCommandHandler)]
        )
        return mediator

    def init_chat_mongodb_repository() -> MongoDBChatRepository:
        config: Config = container.resolve(Config)
        client = AsyncIOMotorClient(
            config.mongodb_conn_uri, serverSelectionTimeoutMS=3000
        )
        return MongoDBChatRepository(
            mongodb_client=client,
            mongodb_db_name=config.mongodb_db_name,
            mongodb_collection_name=config.mongodb_collection_name,
        )

    container.register(
        BaseChatRepository,
        factory=init_chat_mongodb_repository,
        scope=Scope.singleton,
    )
    container.register(Mediator, factory=init_mediator)
    return container
