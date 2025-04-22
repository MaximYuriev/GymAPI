from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class PhoneNumberNotUniqueException(ApplicationException):
    phone: str

    @property
    def message(self) -> str:
        return f"Номер телефона '{self.phone}' не уникален!"
