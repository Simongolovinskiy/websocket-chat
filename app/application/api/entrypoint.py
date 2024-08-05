from fastapi import FastAPI


def create_app():
    return FastAPI(
        title="AMQP + WebSocket Chat",
        docs_url="/api/docs",
        description="Kafka + DDD clean architect example",
        debug=True
    )

