from functools import lru_cache

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope

from app.application.api.common.websockets.managers import (
    ConnectionManager,
    BaseConnectionManager,
)
from app.domain.events.messages import (
    NewChatCreatedEvent,
    NewMessageReceivedEvent,
)
from app.infrastructure.message_brokers.base import BaseMessageBroker
from app.infrastructure.message_brokers.kafka import KafkaMessageBroker
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
from app.services.events.messages import (
    NewChatCreatedEventHandler,
    NewMessageReceivedEventHandler,
)
from app.services.mediator.base import Mediator
from app.services.mediator.event import EventMediator
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

    def create_message_broker() -> BaseMessageBroker:
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=config.broker_url),
            consumer=AIOKafkaConsumer(
                bootstrap_servers=config.broker_url, group_id="chat"
            ),
        )

    container.register(
        BaseMessageBroker, factory=create_message_broker, scope=Scope.singleton
    )

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
        create_chat_handler = CreateChatCommandHandler(
            _mediator=mediator,
            chats_repository=container.resolve(BaseChatsRepository),
        )
        create_message_handler = CreateMessageCommandHandler(
            _mediator=mediator,
            chats_repository=container.resolve(BaseChatsRepository),
            messages_repository=container.resolve(BaseMessagesRepository),
        )

        new_chat_created_event_handler = NewChatCreatedEventHandler(
            broker_topic=config.new_chats_event_topic,
            message_broker=container.resolve(BaseMessageBroker),
        )

        new_message_received_event_handler = NewMessageReceivedEventHandler(
            message_broker=container.resolve(BaseMessageBroker),
            broker_topic=config.new_message_received_event_topic,
        )
        mediator.register_event(
            NewMessageReceivedEvent, [new_message_received_event_handler]
        )
        mediator.register_event(
            NewChatCreatedEvent, [new_chat_created_event_handler]
        )
        mediator.register_command(CreateChatCommand, [create_chat_handler])
        mediator.register_command(
            CreateMessageCommand,
            [create_message_handler],
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
    container.register(EventMediator, factory=init_mediator)
    container.register(
        BaseConnectionManager,
        instance=ConnectionManager(),
        scope=Scope.singleton,
    )
    return container
