from uuid import UUID

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket

from punq import Container

from app.infrastructure.message_brokers.base import BaseMessageBroker
from app.services.init import init_container
from app.settings.conf import Config

router = APIRouter(tags=["chats"])


@router.websocket("/{chat_oid}/")
async def messages_handlers(
    chat_oid: UUID,
    websocket: WebSocket,
    container: Container = Depends(init_container),
):
    await websocket.accept()

    config: Config = container.resolve(Config)
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)

    try:
        async for consumed_message in message_broker.start_consuming(
            topic=config.new_message_received_event_topic.format(
                chat_oid=chat_oid
            )
        ):
            await websocket.send_json(consumed_message)
    finally:
        await message_broker.stop_consuming(topic=str(chat_oid))
        await websocket.close(reason="WebSocket has closed.")
