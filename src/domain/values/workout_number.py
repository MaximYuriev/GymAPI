from dataclasses import dataclass

from src.domain.exceptions.workout_number import WorkoutNumberTooSmallException, WorkoutNumberTooBigException
from src.domain.values.base import BaseValueObject


@dataclass
class WorkoutNumber(BaseValueObject):
    _value: int | None = None

    def _validate(self) -> None:
        if self._value is not None:
            if self._value < 0:
                raise WorkoutNumberTooSmallException
            if self._value > 100:
                raise WorkoutNumberTooBigException

    def __gt__(self, other: "WorkoutNumber") -> bool:
        if self.value > other.value:
            return True
        return False
