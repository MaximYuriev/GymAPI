from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class NullNameException(ApplicationException):
    @property
    def message(self) -> str:
        return "Имя не может быть пустым!"


@dataclass(frozen=True, eq=False)
class NameTooLongException(ApplicationException):
    value: str

    @property
    def message(self) -> str:
        return f"Слишком длинное имя: {self.value[100]}..."
