from dataclasses import dataclass
from typing import Iterable, Tuple

from app.domain.entities.messages import Chat, Message
from app.infrastructure.filters.messages import GetMessageFilters
from app.infrastructure.repositories.messages.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from app.services.exceptions.messages import ChatNotFoundException
from app.services.queries.base import BaseQuery, QueryHandler


@dataclass(frozen=True)
class GetChatDetailQuery(BaseQuery):
    chat_oid: str


@dataclass(frozen=True)
class GetMessagesQuery(BaseQuery):
    chat_oid: str
    filters: GetMessageFilters


@dataclass(frozen=True)
class GetChatDetailQueryHandler(QueryHandler):
    chat_repository: BaseChatsRepository
    messages_repository: BaseMessagesRepository

    async def handle(self, query: GetChatDetailQuery) -> Chat:
        chat_oid = query.chat_oid
        chat = await self.chat_repository.get_chat_by_oid(chat_oid)
        if not chat:
            raise ChatNotFoundException(chat_oid)
        return chat


@dataclass(frozen=True)
class GetMessagesQueryHandler(QueryHandler):
    messages_repository: BaseMessagesRepository

    async def handle(
        self, query: GetMessagesQuery
    ) -> Tuple[Iterable[Message], int]:
        return await self.messages_repository.fetch_messages(
            chat_oid=query.chat_oid,
            filters=query.filters,
        )
