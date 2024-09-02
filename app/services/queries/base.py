from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar


@dataclass(frozen=True, eq=False)
class BaseQuery(ABC):
    chat_oid: str


QT = TypeVar("QT", bound=BaseQuery)
QR = TypeVar("QR", bound=Any)


@dataclass(frozen=True)
class QueryHandler(ABC, Generic[QT, QR]):
    @abstractmethod
    async def handle(self, query: QT) -> QR:
        ...
