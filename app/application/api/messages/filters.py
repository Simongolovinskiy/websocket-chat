from pydantic import BaseModel

from app.infrastructure.filters.messages import GetMessageFilters


class GetMessagesFilters(BaseModel):
    limit: int = 10
    offset: int = 0

    def to_infrastructure(
        self,
    ):
        return GetMessageFilters(limit=self.limit, offset=self.offset)
