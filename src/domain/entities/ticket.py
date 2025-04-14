import datetime
import uuid
from dataclasses import dataclass, field

from src.domain.values.name import Name
from src.domain.values.workout_number import WorkoutNumber


@dataclass
class TicketType:
    type_id: uuid.UUID = field(default_factory=uuid.uuid4, kw_only=True)
    type_name: Name
    workout_number: WorkoutNumber
    duration: datetime.timedelta


@dataclass
class Ticket:
    ticket_id: uuid.UUID = field(default_factory=uuid.uuid4, kw_only=True)
    ticket_type: TicketType
    expression_date: datetime.date
    workout_number: WorkoutNumber

    @classmethod
    def create_ticket(cls, ticket_type: TicketType) -> 'Ticket':
        return cls(
            ticket_type=ticket_type,
            expression_date=datetime.date.today() + ticket_type.duration,
            workout_number=ticket_type.workout_number,
        )
