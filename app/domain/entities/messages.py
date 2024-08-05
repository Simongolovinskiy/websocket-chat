from dataclasses import dataclass, field

from app.domain.entities.base import BaseEntity
from app.domain.events.messages import NewMessageReceivedEvent, NewChatCreated
from app.domain.values.messages import Text, Title


@dataclass
class Message(BaseEntity):
    text: Text
    __hash__ = BaseEntity.__hash__


@dataclass
class Chat(BaseEntity):
    title: Title
    __hash__ = BaseEntity.__hash__
    messages: set[Message] = field(
        default_factory=set,
        kw_only=True
    )

    @classmethod
    def create_chat(cls, title: Title) -> "Chat":
        new_chat = cls(title=title)
        new_chat.register_event(event=NewChatCreated(
            chat_oid=new_chat.oid,
            chat_title=new_chat.title.as_generic_type()
        )
        )
        return new_chat

    def add_message(self, message: Message) -> None:
        self.messages.add(message)
        self.register_event(
            NewMessageReceivedEvent(
                message_text=message.text.as_generic_type(),
                message_oid=message.oid,
                chat_oid=str(self.oid)
            )
        )
