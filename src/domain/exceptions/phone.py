from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class PhoneFormatException(ApplicationException):
    value: str

    @property
    def message(self) -> str:
        return f"Номер должен быть записан в следующем формате: '89123456789'. Вы ввели '{self.value}'"
