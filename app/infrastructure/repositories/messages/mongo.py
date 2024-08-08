from dataclasses import dataclass

from motor.core import AgnosticClient

from app.domain.entities.messages import Chat
from app.infrastructure.repositories.messages.base import BaseChatRepository
from app.infrastructure.repositories.messages.converters import (
    convert_entity_to_document,
)


@dataclass
class MongoDBChatRepository(BaseChatRepository):
    mongodb_client: AgnosticClient
    mongodb_db_name: str
    mongodb_collection_name: str

    def _get_chat_collection(self):
        return self.mongodb_client[self.mongodb_db_name][
            self.mongodb_collection_name
        ]

    async def check_chat_exists_by_title(self, title: str) -> bool:
        collection = self._get_chat_collection()

        return bool(await collection.find_one(filter={"title": title}))

    async def add_chat(self, chat: Chat) -> None:
        collection = self._get_chat_collection()
        await collection.insert_one(convert_entity_to_document(chat))
