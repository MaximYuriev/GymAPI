from dataclasses import dataclass

from src.domain.exceptions.name import NullNameException, NameTooLongException
from src.domain.values.base import BaseValueObject


@dataclass
class Name(BaseValueObject):
    _value: str

    def _validate(self) -> None:
        if len(self._value) == 0:
            raise NullNameException

        elif len(self._value) > 100:
            raise NameTooLongException(self._value)


@dataclass
class Surname(Name):
    pass


@dataclass
class Patronymic(Name):
    _value: str | None = None

    def _validate(self) -> None:
        if self._value is not None:
            super()._validate()
