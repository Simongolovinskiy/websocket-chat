from typing import Any, Mapping

from app.domain.entities.messages import Chat, Message
from app.domain.values.messages import Text, Title


def convert_message_to_document(message: Message) -> dict:
    return dict(
        oid=message.oid,
        text=message.text.as_generic_type(),
        created_at=message.created_at,
        chat_oid=message.chat_oid,
    )


def convert_entity_to_document(chat: Chat) -> dict:
    return dict(
        oid=chat.oid,
        title=chat.title.as_generic_type(),
        created_at=chat.created_at,
    )


def convert_message_document_to_entity(message_document: Mapping[str, Any]) -> Message:
    return Message(
        text=Text(message_document["text"]),
        oid=message_document["oid"],
        created_at=message_document["created_at"],
        chat_oid=message_document["chat_oid"],
    )


def convert_document_to_entity(chat_document: Mapping[str, Any]) -> Chat:
    return Chat(
        title=Title(value=chat_document["title"]),
        oid=chat_document["oid"],
        created_at=chat_document["created_at"],
    )
