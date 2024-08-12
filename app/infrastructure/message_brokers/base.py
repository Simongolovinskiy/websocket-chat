from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class BaseMessageBroker(ABC):

    @abstractmethod
    async def start(self): ...

    @abstractmethod
    async def close(self): ...

    @abstractmethod
    async def send_message(
        self, key: bytes, topic: str, value: bytes
    ) -> None: ...

    @abstractmethod
    async def start_consuming(self, topic: str): ...

    @abstractmethod
    async def stop_consuming(self, topic: str): ...
