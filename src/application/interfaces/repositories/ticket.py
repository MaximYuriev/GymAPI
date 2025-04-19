from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.entities.ticket import TicketType


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
