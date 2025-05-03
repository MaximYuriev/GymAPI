import datetime
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


@dataclass(frozen=True, eq=False)
class TicketNotFoundException(ApplicationException):
    ticket_id: uuid.UUID

    @property
    def message(self) -> str:
        return f"Абонемент с id='{self.ticket_id}' не найден!"


@dataclass(frozen=True, eq=False)
class TicketIsNotActiveException(ApplicationException):
    ticket_id: uuid.UUID

    @property
    def message(self) -> str:
        return f"Абонемент с id='{self.ticket_id}' не является активным!"


@dataclass(frozen=True, eq=False)
class TicketActiveTimeExpireException(ApplicationException):
    expression_date: datetime.date

    @property
    def message(self) -> str:
        return f"Абонемент истек! Он был действителен до {self.expression_date}"


@dataclass(frozen=True, eq=False)
class TicketNotEnoughWorkoutNumberException(ApplicationException):
    @property
    def message(self) -> str:
        return "Не достаточно тренировок по абонементу!"
