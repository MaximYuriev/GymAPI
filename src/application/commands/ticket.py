import datetime
from dataclasses import dataclass

from src.application.commands.base import BaseCommand


@dataclass(frozen=True, eq=False)
class CreateTicketTypeCommand(BaseCommand):
    type_name: str
    workout_number: int | None
    duration: datetime.timedelta
