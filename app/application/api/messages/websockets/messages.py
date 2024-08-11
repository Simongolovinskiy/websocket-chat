from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket

router = APIRouter(tags=["chats"])


@router.websocket("/{chat_oid}")
async def messages_handlers(chat_oid: str, websocket: WebSocket):
    await websocket.accept()
    while True:
        print(chat_oid)

        await websocket.send_text(chat_oid)
