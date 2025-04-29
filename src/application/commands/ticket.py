import datetime
import uuid
from dataclasses import dataclass

from src.application.commands.base import BaseCommand


@dataclass(frozen=True, eq=False)
class CreateTicketTypeCommand(BaseCommand):
    type_name: str
    workout_number: int | None
    duration: datetime.timedelta


@dataclass(frozen=True, eq=False)
class UpdateTicketTypeCommand(BaseCommand):
    ticket_type_id: uuid.UUID
    type_name: str


@dataclass(frozen=True, eq=False)
class DeleteTicketTypeCommand(BaseCommand):
    ticket_type_id: uuid.UUID
