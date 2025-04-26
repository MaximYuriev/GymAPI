import uuid
from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class PhoneNumberNotUniqueException(ApplicationException):
    phone: str

    @property
    def message(self) -> str:
        return f"Номер телефона '{self.phone}' не уникален!"


@dataclass(frozen=True, eq=False)
class CustomerNotFoundException(ApplicationException):
    customer_id: uuid.UUID

    @property
    def message(self) -> str:
        return f"Клиент с id='{self.customer_id}' не найден!"


@dataclass(frozen=True, eq=False)
class CustomerAlreadyHasActiveTicketException(ApplicationException):
    @property
    def message(self) -> str:
        return "Клиент уже имеет активный абонемент!"
