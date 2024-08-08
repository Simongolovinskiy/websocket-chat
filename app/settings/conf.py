from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    mongodb_conn_uri: str = Field(
        default="mongodb://mongodb:27017", alias="MONGODB_CONN_URI"
    )
    mongodb_chat_db_name: str = Field(
        default="chat", alias="MONGODB_CHAT_DATABASE"
    )
    mongodb_chat_collection_name: str = Field(
        default="chat", alias="MONGODB_CHAT_COLLECTION_NAME"
    )
    mongodb_messages_collection_name: str = Field(
        default="messages", alias="MONGODB_MESSAGES_COLLECTION"
    )
