from typing import Dict, Iterable
from collections import defaultdict
from dataclasses import dataclass, field

from app.domain.events.base import BaseEvent
from app.services.events.base import EventHandler, ER, ET
from app.services.commands.base import CommandHandler, CR, CT
from app.services.exceptions.mediator import (
    EventHandlersNotRegistered,
    CommandHandlersNotRegistered,
)


@dataclass(eq=False)
class Mediator:
    events_map: Dict[ET, EventHandler] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )
    commands_map: Dict[CT, CommandHandler] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )

    def register_event(
        self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]]
    ) -> None:
        self.events_map[event].extend(event_handlers)

    def register_command(
        self, command: CT, command_handlers: Iterable[CommandHandler[CT, CR]]
    ) -> None:
        self.commands_map[command].extend(command_handlers)

    async def handle_event(self, event: BaseEvent) -> Iterable[ER]:
        event_type = event.__class__
        handlers = self.events_map.get(event_type)
        if not handlers:
            raise EventHandlersNotRegistered(event_type)

        return [await handler.handle(event) for handler in handlers]

    async def handle_command(self, command: CT) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.commands_map.get(command_type)
        if not handlers:
            raise CommandHandlersNotRegistered(command_type)

        return [await handler.handle(command) for handler in handlers]
