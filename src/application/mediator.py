from dataclasses import dataclass, field
from typing import Type, Any

from src.application.commands.base import BaseCommand
from src.application.exception.mediator import CommandNotRegisteredException, EventNotRegisteredException
from src.application.handlers.commands.base import BaseCommandHandler
from src.application.handlers.events.base import BaseEventHandler
from src.domain.events.base import BaseEvent


@dataclass(frozen=True, eq=False)
class Mediator[ET:BaseEvent, CT:BaseCommand, ER: Any, CR: Any]:
    events_map: dict[ET, Type[BaseEventHandler]] = field(
        default_factory=dict,
        kw_only=True,
    )
    commands_map: dict[CT, Type[BaseCommandHandler]] = field(
        default_factory=dict,
        kw_only=True,
    )

    def register_event(
            self,
            event: ET,
            event_handler: Type[BaseEventHandler],
    ) -> None:
        self.events_map[event] = event_handler

    def register_command(
            self,
            command: CT,
            command_handler: Type[BaseCommandHandler],
    ) -> None:
        self.commands_map[command] = command_handler

    async def handle_command(self, command: CT) -> CR:
        command_handler = self.commands_map.get(command)
        if command_handler is None:
            raise CommandNotRegisteredException(command)

        return await command_handler().handle(command)

    async def handle_event(self, event: ET) -> ER:
        event_handler = self.events_map.get(event)
        if event_handler is None:
            raise EventNotRegisteredException(event)

        return await event_handler().handle(event)
