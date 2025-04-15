from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from src.application.commands.base import BaseCommand


@dataclass(frozen=True, eq=False)
class BaseCommandHandler[CT:BaseCommand, CR:Any](ABC):
    @abstractmethod
    async def handle(self, command: CT) -> CR:
        pass
