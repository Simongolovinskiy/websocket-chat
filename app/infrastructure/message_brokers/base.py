from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseMessageBroker(ABC):
    @abstractmethod
    async def start(self) -> None:
        ...

    @abstractmethod
    async def close(self) -> None:
        ...

    @abstractmethod
    async def send_message(self, key: bytes, topic: str, value: bytes) -> None:
        ...

    @abstractmethod
    async def start_consuming(self, topic: str):
        ...

    @abstractmethod
    async def stop_consuming(self) -> None:
        ...

    async def consume(self):
        ...
