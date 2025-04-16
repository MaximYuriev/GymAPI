from dataclasses import dataclass, field
from typing import Type, Any

from src.application.commands.base import BaseCommand
from src.application.exceptions.mediator import CommandNotRegisteredException, EventNotRegisteredException
from src.application.handlers.commands.base import BaseCommandHandler
from src.application.handlers.events.base import BaseEventHandler
from src.domain.events.base import BaseEvent
from src.ioc.mediator import mediator_dependencies_container


@dataclass(frozen=True, eq=False)
class Mediator[ET: Type[BaseEvent], CT: Type[BaseCommand], ER: Any, CR: Any]:
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

    async def handle_command(self, command: BaseCommand) -> CR:
        command_type = command.__class__
        command_handler_type = self.commands_map.get(command_type)

        if command_handler_type is None:
            raise CommandNotRegisteredException(command_type)

        async with mediator_dependencies_container() as container:
            handler = await container.get(command_handler_type)
            return await handler.handle(command)

    async def handle_event(self, event: BaseEvent) -> ER:
        event_type = event.__class__
        event_handler_type = self.events_map.get(event_type)

        if event_handler_type is None:
            raise EventNotRegisteredException(event_type)

        with mediator_dependencies_container() as container:
            handler = await container.get(event_handler_type)
            return await handler.handle(event)
