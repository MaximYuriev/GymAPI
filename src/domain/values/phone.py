import re
from dataclasses import dataclass

from src.domain.exceptions.phone import PhoneFormatException
from src.domain.values.base import BaseValueObject


@dataclass
class PhoneNumber(BaseValueObject):
    _value: str

    def _validate(self) -> None:
        if re.search(r'89\d{9}$', self._value) is None:
            raise PhoneFormatException(self._value)
