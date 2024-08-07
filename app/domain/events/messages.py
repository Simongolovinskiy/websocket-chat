from dataclasses import dataclass

from app.domain.events.base import BaseEvent
from app.domain.values.messages import Text


@dataclass
class NewMessageReceivedEvent(BaseEvent):
    message_text: str
    message_oid: str
    chat_oid: str


@dataclass
class NewChatCreated(BaseEvent):
    chat_oid: str
    chat_title: str
