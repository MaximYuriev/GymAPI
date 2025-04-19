from dataclasses import dataclass

from src.application.handlers.queries.base import BaseQueryHandler
from src.application.interfaces.repositories.ticket import TicketTypeRepository
from src.application.queries.ticket import GetAllTicketTypesQuery
from src.domain.entities.ticket import TicketType


@dataclass(frozen=True, eq=False)
class GetAllTicketTypesQueryHandler(BaseQueryHandler):
    _repository: TicketTypeRepository

    async def handle(self, query: GetAllTicketTypesQuery) -> list[TicketType]:
        return await self._repository.get_all_ticket_types(
            limit=query.limit,
            offset=query.offset,
        )
