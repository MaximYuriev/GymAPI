from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseValueObject[T](ABC):
    _value: T

    def __post_init__(self):
        self._validate()

    @abstractmethod
    def _validate(self) -> None:
        pass

    @property
    def value(self) -> T:
        return self._value
