from dataclasses import dataclass
from typing import Type

from src.application.commands.base import BaseCommand
from src.application.queries.base import BaseQuery
from src.domain.events.base import BaseEvent
from src.domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class MediatorException(ApplicationException):
    @property
    def message(self) -> str:
        return "Ошибка медиатора!"


@dataclass(frozen=True, eq=False)
class CommandNotRegisteredException(MediatorException):
    command: Type[BaseCommand]

    @property
    def message(self) -> str:
        return f"Команда '{self.command}' не зарегистрирована в медиаторе!"


@dataclass(frozen=True, eq=False)
class EventNotRegisteredException(MediatorException):
    event: Type[BaseEvent]

    @property
    def message(self) -> str:
        return f"Событие '{self.event}' не зарегистрировано в медиаторе!"


@dataclass(frozen=True, eq=False)
class QueryNotRegisteredException(ApplicationException):
    query: Type[BaseQuery]

    @property
    def message(self) -> str:
        return f"Запрос '{self.query}' не зарегистрирован в медиаторе!"
