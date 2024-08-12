import asyncio

from contextlib import asynccontextmanager

from aiokafka.errors import KafkaConnectionError

from app.infrastructure.message_brokers.base import BaseMessageBroker
from app.services.init import init_container


async def start_kafka(retries=5, delay=3):
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    for attempt in range(retries):
        try:
            await message_broker.start()
            break
        except KafkaConnectionError as e:
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                raise e


async def stop_kafka():
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.close()


@asynccontextmanager
async def lifespan(*_):
    await start_kafka()
    yield
    await stop_kafka()
