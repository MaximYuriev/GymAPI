from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class LimitValueTooSmallException(ApplicationException):
    limit: int

    @property
    def message(self) -> str:
        return f"Значение limit должно быть больше нуля! Полученное значение: '{self.limit}'"


@dataclass(frozen=True, eq=False)
class OffsetValueTooSmallException(ApplicationException):
    offset: int

    @property
    def message(self) -> str:
        return f"Значение offset должно быть больше нуля или равняться ему! Полученное значение: '{self.offset}'"
