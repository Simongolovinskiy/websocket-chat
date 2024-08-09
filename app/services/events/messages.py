from dataclasses import dataclass

from app.domain.events.messages import NewChatCreatedEvent
from app.infrastructure.message_brokers.converters import (
    convert_event_to_broker_message,
)
from app.services.events.base import EventHandler


@dataclass
class NewChatCreatedEventHandler(EventHandler[NewChatCreatedEvent, None]):

    async def handle(self, event: NewChatCreatedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event),
            key=str(event.event_id).encode(),
        )
        print(f"The event is handled {event.title}")
