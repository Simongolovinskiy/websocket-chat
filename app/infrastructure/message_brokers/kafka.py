from dataclasses import dataclass, field

import orjson
from aiokafka.consumer import AIOKafkaConsumer
from aiokafka.producer import AIOKafkaProducer

from app.infrastructure.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer
    consumer: AIOKafkaConsumer
    consumer_map: dict[str, AIOKafkaConsumer] = field(
        default_factory=dict, kw_only=True
    )

    async def send_message(self, key: bytes, topic: str, value: bytes) -> None:
        await self.producer.send(key=key, topic=topic, value=value)

    async def start_consuming(self, topic: str):

        self.consumer.subscribe(topics=[topic])

        async for message in self.consumer:
            yield orjson.loads(message.value)

    async def stop_consuming(self, topic: str) -> None:
        self.consumer.unsubscribe()
        await self.consumer.stop()

    async def start(self) -> None:
        await self.producer.start()
        await self.consumer.start()

    async def close(self) -> None:
        await self.producer.stop()
        await self.consumer.stop()
