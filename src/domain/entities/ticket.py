import datetime
import uuid
from dataclasses import dataclass, field

from src.domain.entities.base import BaseEntity
from src.domain.values.name import Name
from src.domain.values.workout_number import WorkoutNumber


@dataclass
class TicketType(BaseEntity):
    type_id: uuid.UUID = field(default_factory=uuid.uuid4, kw_only=True)
    type_name: Name
    workout_number: WorkoutNumber
    duration: datetime.timedelta


@dataclass
class Ticket(BaseEntity):
    ticket_id: uuid.UUID = field(default_factory=uuid.uuid4, kw_only=True)
    customer_id: uuid.UUID
    ticket_type: TicketType
    expression_date: datetime.date
    workout_number: WorkoutNumber
    is_active: bool = field(default=True, kw_only=True)

    @classmethod
    def create_ticket(cls, customer_id: uuid.UUID, ticket_type: TicketType) -> 'Ticket':
        return cls(
            ticket_type=ticket_type,
            expression_date=datetime.date.today() + ticket_type.duration,
            workout_number=ticket_type.workout_number,
            customer_id=customer_id,
        )
