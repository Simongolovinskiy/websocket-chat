from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope

from app.infrastructure.repositories.messages.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from app.infrastructure.repositories.messages.mongo import (
    MongoDBChatsRepository,
    MongoDBMessagesRepository,
)
from app.services.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
    CreateMessageCommand,
    CreateMessageCommandHandler,
)
from app.services.mediator import Mediator
from app.services.queries.messages import (
    GetChatDetailQuery,
    GetChatDetailQueryHandler,
    GetMessagesQueryHandler,
    GetMessagesQuery,
)
from app.settings.conf import Config


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(Config, instance=Config(), scope=Scope.singleton)
    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)
    #  CQRS
    container.register(GetChatDetailQueryHandler)
    container.register(GetMessagesQueryHandler)

    def create_mongodb_client():
        return AsyncIOMotorClient(
            config.mongodb_conn_uri, serverSelectionTimeoutMS=3000
        )

    container.register(
        AsyncIOMotorClient,
        factory=create_mongodb_client,
        scope=Scope.singleton,
    )

    config: Config = container.resolve(Config)
    client = container.resolve(AsyncIOMotorClient)

    def init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand, [container.resolve(CreateChatCommandHandler)]
        )
        mediator.register_command(
            CreateMessageCommand,
            [container.resolve(CreateMessageCommandHandler)],
        )
        mediator.register_query(
            GetChatDetailQuery, container.resolve(GetChatDetailQueryHandler)
        )
        mediator.register_query(
            GetMessagesQuery, container.resolve(GetMessagesQueryHandler)
        )
        return mediator

    def init_chats_mongodb_repository() -> MongoDBChatsRepository:
        return MongoDBChatsRepository(
            mongodb_client=client,
            mongodb_db_name=config.mongodb_chat_db_name,
            mongodb_collection_name=config.mongodb_chat_collection_name,
        )

    def init_messages_mongodb_repository() -> MongoDBMessagesRepository:
        return MongoDBMessagesRepository(
            mongodb_client=client,
            mongodb_db_name=config.mongodb_chat_db_name,
            mongodb_collection_name=config.mongodb_messages_collection_name,
        )

    container.register(
        BaseChatsRepository,
        factory=init_chats_mongodb_repository,
        scope=Scope.singleton,
    )
    container.register(
        BaseMessagesRepository,
        factory=init_messages_mongodb_repository,
        scope=Scope.singleton,
    )
    container.register(Mediator, factory=init_mediator)
    return container
