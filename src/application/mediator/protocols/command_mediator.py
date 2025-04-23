from dataclasses import dataclass
from typing import Protocol, Type, Any

from src.application.commands.base import BaseCommand
from src.application.handlers.commands.base import BaseCommandHandler


@dataclass(frozen=True, eq=False)
class Command[CT: Type[BaseCommand], CR: Any](Protocol):
    def register_command(
            self,
            command: CT,
            command_handler: Type[BaseCommandHandler],
    ) -> None:
        pass

    async def handle_command(self, command: BaseCommand) -> CR:
        pass
