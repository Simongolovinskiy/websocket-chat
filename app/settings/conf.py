from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    mongodb_conn_uri: str = Field(alias="MONGODB_CONN_URI")
    mongodb_db_name: str = Field(default="chat", alias="MONGODB_DATABASE")
    mongodb_collection_name: str = Field(alias="MONGODB_COLLECTIONNAME")
