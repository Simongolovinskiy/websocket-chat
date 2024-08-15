from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import DefaultDict, List, Any, Mapping

from fastapi import WebSocket


@dataclass
class BaseConnectionManager(ABC):
    connections_map: DefaultDict[str, List[WebSocket]] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )

    @abstractmethod
    async def accept_connection(
        self, websocket: WebSocket, key: str
    ) -> None: ...

    @abstractmethod
    async def remove_connection(
        self, websocket: WebSocket, key: str
    ) -> None: ...

    @abstractmethod
    async def send_all(
        self, key: str, json_message: Mapping[str, Any]
    ) -> None: ...


@dataclass
class ConnectionManager(BaseConnectionManager):

    async def accept_connection(self, websocket: WebSocket, key: str) -> None:
        await websocket.accept()
        self.connections_map[key].append(websocket)

    async def remove_connection(self, websocket: WebSocket, key: str) -> None:
        await websocket.close()
        self.connections_map[key].remove(websocket)

    async def send_all(
        self, key: str, json_message: Mapping[str, Any]
    ) -> None:
        for websocket in self.connections_map[key]:
            await websocket.send_json(json_message)
