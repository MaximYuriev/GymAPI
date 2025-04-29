from dataclasses import dataclass

from src.application.commands.ticket import CreateTicketTypeCommand, DeleteTicketTypeCommand, UpdateTicketTypeCommand
from src.application.exceptions.ticket import TicketTypeAlreadyExistException, TicketTypeNotFoundException
from src.application.handlers.commands.base import BaseCommandHandler
from src.application.interfaces.repositories.ticket import TicketTypeRepository
from src.domain.entities.ticket import TicketType
from src.domain.values.name import Name
from src.domain.values.workout_number import WorkoutNumber


@dataclass(frozen=True, eq=False)
class CreateTicketTypeCommandHandler(BaseCommandHandler):
    _ticket_type_repository: TicketTypeRepository

    async def handle(self, command: CreateTicketTypeCommand) -> TicketType:
        if await self._ticket_type_repository.check_exists_ticket_type_by_type_name(command.type_name):
            raise TicketTypeAlreadyExistException(command.type_name)

        type_name = Name(command.type_name)
        workout_number = WorkoutNumber(command.workout_number)

        ticket_type = TicketType(
            type_name=type_name,
            workout_number=workout_number,
            duration=command.duration,
        )

        await self._ticket_type_repository.add_ticket_type(ticket_type)

        return ticket_type


@dataclass(frozen=True, eq=False)
class UpdateTicketTypeCommandHandler(BaseCommandHandler):
    _ticket_type_repository: TicketTypeRepository

    async def handle(self, command: UpdateTicketTypeCommand) -> TicketType:
        ticket_type = await self._ticket_type_repository.get_ticket_type_by_id(command.ticket_type_id)
        if ticket_type is None:
            raise TicketTypeNotFoundException(command.ticket_type_id)

        if await self._ticket_type_repository.check_exists_ticket_type_by_type_name(command.type_name):
            raise TicketTypeAlreadyExistException(command.type_name)

        name = Name(command.type_name)
        ticket_type.type_name = name

        await self._ticket_type_repository.update_ticket_type(ticket_type)
        return ticket_type


@dataclass(frozen=True, eq=False)
class DeleteTicketTypeCommandHandler(BaseCommandHandler):
    _ticket_type_repository: TicketTypeRepository

    async def handle(self, command: DeleteTicketTypeCommand) -> TicketType:
        ticket_type = await self._ticket_type_repository.get_ticket_type_by_id(command.ticket_type_id)
        if ticket_type is None:
            raise TicketTypeNotFoundException(command.ticket_type_id)

        await self._ticket_type_repository.delete_ticket_type(ticket_type)

        return ticket_type
