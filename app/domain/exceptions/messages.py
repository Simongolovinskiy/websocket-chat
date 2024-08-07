from dataclasses import dataclass

from app.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class TitleTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return f"Too long message: '{self.text[:255]}...'"


@dataclass(eq=False)
class EmptyTextException(ApplicationException):

    @property
    def message(self):
        return f"The text is empty."
