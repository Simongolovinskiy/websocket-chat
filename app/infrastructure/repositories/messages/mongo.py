from abc import ABC
from dataclasses import dataclass

from motor.core import AgnosticClient

from app.domain.entities.messages import Chat, Message
from app.infrastructure.repositories.messages.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from app.infrastructure.repositories.messages.converters import (
    convert_entity_to_document,
    convert_message_to_document,
    convert_document_to_entity,
)


@dataclass
class BaseMongoDBRepository(ABC):
    mongodb_client: AgnosticClient
    mongodb_db_name: str
    mongodb_collection_name: str

    @property
    def _collection(self):
        return self.mongodb_client[self.mongodb_db_name][
            self.mongodb_collection_name
        ]


@dataclass
class MongoDBChatsRepository(BaseChatsRepository, BaseMongoDBRepository):

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        chat_document = await self._collection.find_one(filter={"oid": oid})
        if not chat_document:
            return None
        return convert_document_to_entity(chat_document)

    async def check_chat_exists_by_title(self, title: str) -> bool:
        return bool(await self._collection.find_one(filter={"title": title}))

    async def add_chat(self, chat: Chat) -> None:
        await self._collection.insert_one(convert_entity_to_document(chat))


@dataclass
class MongoDBMessagesRepository(BaseMessagesRepository, BaseMongoDBRepository):

    async def add_message(self, chat_oid: str, message: Message) -> None:
        await self._collection.update_one(
            {"oid": chat_oid},
            {"$push": {"messages": convert_message_to_document(message)}},
        )
