from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class BaseMessageBroker(ABC):
    # consumer: AIOKafkaConsumer

    @abstractmethod
    async def send_message(
        self, key: bytes, topic: str, value: bytes
    ) -> None: ...

    @abstractmethod
    async def receive_message(self, topic: str): ...
