from uuid import uuid4
from datetime import datetime
from abc import ABC
from dataclasses import dataclass, field


@dataclass(eq=False)
class BaseEntity(ABC):
    oid: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True
    )
    created_at: datetime = field(
        default_factory=lambda: datetime.now(),
        kw_only=True
    )

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, other: "BaseEntity") -> bool:
        return self.oid == other.oid

