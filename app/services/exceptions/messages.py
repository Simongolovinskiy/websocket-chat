from dataclasses import dataclass

from app.services.exceptions.base import ServicesException


@dataclass(eq=False)
class ChatWithThatTitleAlreadyExistsException(ServicesException):
    title: str

    @property
    def message(self):
        return f"Chat with that title already exists - {self.title}"


@dataclass(eq=False)
class ChatNotFoundException(ServicesException):
    chat_oid: str

    @property
    def message(self):
        return f"Chat with that oid does not exist - {self.chat_oid}"
