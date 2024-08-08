from dataclasses import dataclass
from typing import Generic

from app.domain.entities.messages import Chat
from app.infrastructure.repositories.messages.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from app.services.exceptions.messages import ChatNotFoundException
from app.services.queries.base import BaseQuery, QueryHandler, QR, QT


@dataclass(frozen=True)
class GetChatDetailQuery(BaseQuery):
    chat_oid: str


@dataclass(frozen=True)
class GetChatDetailQueryHandler(QueryHandler, Generic[QR, QT]):
    chat_repository: BaseChatsRepository
    messages_repository: BaseMessagesRepository

    async def handle(self, query: GetChatDetailQuery) -> Chat:
        chat_oid = query.chat_oid
        chat = await self.chat_repository.get_chat_by_oid(chat_oid)
        if not chat:
            raise ChatNotFoundException(chat_oid)
        return chat
