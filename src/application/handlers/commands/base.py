from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from src.application.commands.base import BaseCommand
from src.application.mediator.protocols.event_mediator import EventMediator


@dataclass(frozen=True, eq=False)
class BaseCommandHandler[CT:BaseCommand, CR:Any](ABC):
    _event_mediator: EventMediator

    @abstractmethod
    async def handle(self, command: CT) -> CR:
        pass
