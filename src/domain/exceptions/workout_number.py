from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class WorkoutNumberTooSmallException(ApplicationException):
    @property
    def message(self) -> str:
        return "Количество тренировок не может быть меньше нуля!"


@dataclass(frozen=True, eq=False)
class WorkoutNumberTooBigException(ApplicationException):
    @property
    def message(self) -> str:
        return "Количество тренировок не может быть больше ста!"
