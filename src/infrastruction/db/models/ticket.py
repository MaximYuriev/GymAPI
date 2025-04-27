import datetime
import uuid

from beanie import Document

from src.domain.entities.ticket import TicketType, Ticket
from src.domain.values.name import Name
from src.domain.values.workout_number import WorkoutNumber


class TicketTypeModel(Document):
    type_id: uuid.UUID
    type_name: str
    workout_number: int | None
    duration: datetime.timedelta

    @classmethod
    def from_entity(cls, ticket_type: TicketType) -> "TicketTypeModel":
        return cls(
            type_id=ticket_type.type_id,
            type_name=ticket_type.type_name.value,
            workout_number=ticket_type.workout_number.value,
            duration=ticket_type.duration,
        )

    def to_entity(self) -> TicketType:
        return TicketType(
            type_id=self.type_id,
            type_name=Name(self.type_name),
            workout_number=WorkoutNumber(self.workout_number),
            duration=self.duration,
        )

    class Settings:
        name = "ticket_type"


class TicketModel(Document):
    ticket_id: uuid.UUID
    ticket_type: TicketTypeModel
    customer_id: uuid.UUID
    expression_date: datetime.date
    workout_number: int | None
    is_active: bool

    @classmethod
    def from_entity(cls, ticket: Ticket) -> "TicketModel":
        return cls(
            ticket_id=ticket.ticket_id,
            customer_id=ticket.customer_id,
            ticket_type=TicketTypeModel.from_entity(ticket.ticket_type),
            expression_date=ticket.expression_date,
            workout_number=ticket.workout_number.value,
            is_active=ticket.is_active,
        )

    def to_entity(self) -> Ticket:
        return Ticket(
            ticket_id=self.ticket_id,
            customer_id=self.customer_id,
            ticket_type=self.ticket_type.to_entity(),
            expression_date=self.expression_date,
            workout_number=WorkoutNumber(self.workout_number),
            is_active=self.is_active,
        )

    class Settings:
        name = "ticket"
