from uuid import UUID

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket

from punq import Container

from app.application.api.common.websockets.managers import (
    BaseConnectionManager,
)
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
    connection_manager: BaseConnectionManager = container.resolve(
        BaseConnectionManager
    )
    await connection_manager.accept_connection(
        websocket=websocket, key=str(chat_oid)
    )

    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)

    try:
        async for message in message_broker.start_consuming(
            topic=config.new_message_received_event_topic
        ):
            await connection_manager.send_all(
                key=str(chat_oid), json_message=message
            )
    finally:
        await connection_manager.remove_connection(
            websocket=websocket, key=str(chat_oid)
        )
        await message_broker.stop_consuming()

    await websocket.close(reason="WebSocket has closed.")
