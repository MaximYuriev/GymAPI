from dataclasses import dataclass

from src.application.exceptions.ticket import TicketTypeNotFoundException
from src.application.handlers.queries.base import BaseQueryHandler
from src.application.interfaces.repositories.ticket import TicketTypeRepository
from src.application.queries.ticket import GetAllTicketTypesQuery, GetTicketTypeQuery
from src.domain.entities.ticket import TicketType


@dataclass(frozen=True, eq=False)
class GetAllTicketTypesQueryHandler(BaseQueryHandler):
    _repository: TicketTypeRepository

    async def handle(self, query: GetAllTicketTypesQuery) -> list[TicketType]:
        return await self._repository.get_all_ticket_types(
            limit=query.limit,
            offset=query.offset,
        )


@dataclass(frozen=True, eq=False)
class GetTicketTypeQueryHandler(BaseQueryHandler):
    _repository: TicketTypeRepository

    async def handle(self, query: GetTicketTypeQuery) -> TicketType:
        ticket_type = await self._repository.get_ticket_type_by_id(query.ticket_type_id)
        if ticket_type is None:
            raise TicketTypeNotFoundException(query.ticket_type_id)

        return ticket_type
