from dataclasses import dataclass

from src.application.exceptions.customer import CustomerNotFoundException
from src.application.exceptions.ticket import ActiveTicketNotFoundException
from src.application.handlers.queries.base import BaseQueryHandler
from src.application.interfaces.repositories.customer import CustomerRepository
from src.application.interfaces.repositories.ticket import TicketRepository
from src.application.queries.customer import GetAllCustomerTicketQuery, GetActiveCustomerTicketQuery
from src.domain.entities.ticket import Ticket


@dataclass(frozen=True, eq=False)
class GetAllCustomerTicketQueryHandler(BaseQueryHandler):
    _ticket_repository: TicketRepository
    _customer_repository: CustomerRepository

    async def handle(self, query: GetAllCustomerTicketQuery) -> list[Ticket]:
        if await self._customer_repository.get_customer_by_id(query.customer_id) is None:
            raise CustomerNotFoundException(query.customer_id)

        return await self._ticket_repository.get_all_customer_ticket_list(
            customer_id=query.customer_id,
            limit=query.limit,
            offset=query.offset,
        )


@dataclass(frozen=True, eq=False)
class GetActiveCustomerTicketQueryHandler(BaseQueryHandler):
    _ticket_repository: TicketRepository
    _customer_repository: CustomerRepository

    async def handle(self, query: GetActiveCustomerTicketQuery) -> Ticket:
        if await self._customer_repository.get_customer_by_id(query.customer_id) is None:
            raise CustomerNotFoundException(query.customer_id)

        ticket = await self._ticket_repository.get_active_customer_ticket(query.customer_id)
        if ticket is None:
            raise ActiveTicketNotFoundException(query.customer_id)

        return ticket
