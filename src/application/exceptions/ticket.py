import uuid
from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class TicketTypeAlreadyExistException(ApplicationException):
    type_name: str

    @property
    def message(self) -> str:
        return f"Тип абонемента с таким названием: '{self.type_name}' уже существует!"


@dataclass(frozen=True, eq=False)
class TicketTypeNotFoundException(ApplicationException):
    ticket_type_id: uuid.UUID

    @property
    def message(self) -> str:
        return f"Тип абонемента с id='{self.ticket_type_id}' не найден!"


@dataclass(frozen=True, eq=False)
class ActiveTicketNotFoundException(ApplicationException):
    customer_id: uuid.UUID

    @property
    def message(self) -> str:
        return f"Активный абонемент для клиента с id='{self.customer_id}' не найден!"
