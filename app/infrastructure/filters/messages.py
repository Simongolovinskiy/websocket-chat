from dataclasses import dataclass


@dataclass
class GetMessageFilters:
    limit: int = 10
    offset: int = 0
