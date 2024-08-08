from fastapi import FastAPI

from app.application.api.messages.handlers import router as message_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="AMQP + WebSocket Chat",
        docs_url="/api/docs",
        description="Kafka + DDD clean architect example",
        debug=True,
    )

    app.include_router(message_router, prefix="/chat")
    return app
