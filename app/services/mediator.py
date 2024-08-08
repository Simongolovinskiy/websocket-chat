from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, Iterable

from app.domain.events.base import BaseEvent
from app.services.commands.base import CR, CT, CommandHandler
from app.services.events.base import ER, ET, EventHandler
from app.services.exceptions.mediator import (
    CommandHandlersNotRegistered,
    EventHandlersNotRegistered,
)
from app.services.queries.base import QT, QueryHandler, QR


@dataclass(eq=False)
class Mediator:
    events_map: Dict[ET, EventHandler] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )
    commands_map: Dict[CT, CommandHandler] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )

    queries_map: Dict[QT, QueryHandler] = field(
        default_factory=dict, kw_only=True
    )

    def register_event(
        self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]]
    ) -> None:
        self.events_map[event].extend(event_handlers)

    def register_command(
        self, command: CT, command_handlers: Iterable[CommandHandler[CT, CR]]
    ) -> None:
        self.commands_map[command].extend(command_handlers)

    def register_query(
        self, query: QT, query_handler: QueryHandler[QT, QR]
    ) -> None:
        self.queries_map[query] = query_handler

    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        result = list()
        event_type = events.__class__
        handlers = self.events_map.get(event_type)
        if not handlers:
            raise EventHandlersNotRegistered(event_type)
        for event in events:
            result.extend(
                [await handler.handle(event) for handler in handlers]
            )
        return result

    async def handle_command(self, command: CT) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.commands_map.get(command_type)
        if not handlers:
            raise CommandHandlersNotRegistered(command_type)

        return [await handler.handle(command) for handler in handlers]

    async def handle_query(self, query: QT) -> QR:
        return await self.queries_map[query.__class__].handle(query)
