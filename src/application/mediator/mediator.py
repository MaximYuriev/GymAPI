from dataclasses import dataclass, field
from typing import Type, Any

from dishka import AsyncContainer

from src.application.commands.base import BaseCommand
from src.application.exceptions.mediator import CommandNotRegisteredException, EventNotRegisteredException, \
    QueryNotRegisteredException, DiContainerNotRegisteredException
from src.application.handlers.commands.base import BaseCommandHandler
from src.application.handlers.events.base import BaseEventHandler
from src.application.handlers.queries.base import BaseQueryHandler
from src.application.queries.base import BaseQuery
from src.domain.events.base import BaseEvent


@dataclass(eq=False)
class Mediator[ET: Type[BaseEvent], CT: Type[BaseCommand], QT: Type[BaseQuery], ER: Any, CR: Any, QR: Any]:
    _events_map: dict[ET, Type[BaseEventHandler]] = field(
        default_factory=dict,
        kw_only=True,
    )
    _commands_map: dict[CT, Type[BaseCommandHandler]] = field(
        default_factory=dict,
        kw_only=True,
    )
    _query_map: dict[QT, Type[BaseQueryHandler]] = field(
        default_factory=dict,
        kw_only=True,
    )
    _mediator_di_container: AsyncContainer | None = None

    def register_di_container(self, di_container: AsyncContainer) -> None:
        self._mediator_di_container = di_container

    def register_event(
            self,
            event: ET,
            event_handler: Type[BaseEventHandler],
    ) -> None:
        self._events_map[event] = event_handler

    def register_command(
            self,
            command: CT,
            command_handler: Type[BaseCommandHandler],
    ) -> None:
        self._commands_map[command] = command_handler

    def register_query(
            self,
            query: QT,
            query_handler: Type[BaseQueryHandler],
    ) -> None:
        self._query_map[query] = query_handler

    async def handle_command(self, command: BaseCommand) -> CR:
        command_type = command.__class__
        command_handler_type = self._commands_map.get(command_type)

        if command_handler_type is None:
            raise CommandNotRegisteredException(command_type)

        if self._mediator_di_container is None:
            raise DiContainerNotRegisteredException

        async with self._mediator_di_container() as container:
            handler = await container.get(command_handler_type)
            return await handler.handle(command)

    async def handle_event(self, event: BaseEvent) -> ER:
        event_type = event.__class__
        event_handler_type = self._events_map.get(event_type)

        if event_handler_type is None:
            raise EventNotRegisteredException(event_type)

        if self._mediator_di_container is None:
            raise DiContainerNotRegisteredException

        async with self._mediator_di_container() as container:
            handler = await container.get(event_handler_type)
            return await handler.handle(event)

    async def handle_query(self, query: BaseQuery) -> QR:
        query_type = query.__class__
        query_handler_type = self._query_map.get(query_type)

        if query_handler_type is None:
            raise QueryNotRegisteredException(query_type)

        if self._mediator_di_container is None:
            raise DiContainerNotRegisteredException

        async with self._mediator_di_container() as container:
            handler = await container.get(query_handler_type)
            return await handler.handle(query)
