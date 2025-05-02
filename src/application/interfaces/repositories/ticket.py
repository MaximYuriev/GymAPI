import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.entities.ticket import TicketType, Ticket


@dataclass(frozen=True, eq=False)
class TicketTypeRepository(ABC):
    @abstractmethod
    async def add_ticket_type(self, ticket_type: TicketType) -> None:
        pass

    @abstractmethod
    async def check_exists_ticket_type_by_type_name(self, type_name: str) -> bool:
        pass

    @abstractmethod
    async def get_all_ticket_types(self, limit: int, offset: int) -> list[TicketType]:
        pass

    @abstractmethod
    async def get_ticket_type_by_id(self, ticket_type_id: uuid.UUID) -> TicketType | None:
        pass

    @abstractmethod
    async def update_ticket_type(self, ticket_type: TicketType) -> None:
        pass

    @abstractmethod
    async def delete_ticket_type(self, ticket_type: TicketType) -> None:
        pass


@dataclass(frozen=True, eq=False)
class TicketRepository(ABC):
    @abstractmethod
    async def add_ticket(self, ticket: Ticket) -> None:
        pass

    @abstractmethod
    async def check_exist_customers_active_ticket(self, customer_id: uuid.UUID) -> bool:
        pass

    @abstractmethod
    async def get_all_customer_ticket_list(self, customer_id: uuid.UUID, limit: int, offset: int) -> list[Ticket]:
        pass

    @abstractmethod
    async def get_active_customer_ticket(self, customer_id: uuid.UUID) -> Ticket | None:
        pass
