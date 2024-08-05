from uuid import uuid4, UUID
from abc import ABC
from dataclasses import dataclass, field


@dataclass
class BaseEvent(ABC):
    event_id: UUID = field(
        default_factory=uuid4,
        kw_only=True
    )

