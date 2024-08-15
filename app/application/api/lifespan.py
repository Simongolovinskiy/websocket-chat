from contextlib import asynccontextmanager


from app.infrastructure.message_brokers.base import BaseMessageBroker
from app.services.init import init_container


async def start_kafka(retries=5, delay=3):
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.start()


async def stop_kafka():
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.close()


@asynccontextmanager
async def lifespan(*_):
    await start_kafka()
    yield
    await stop_kafka()
