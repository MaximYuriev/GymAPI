import datetime
import uuid

from pydantic import BaseModel

from src.domain.entities.ticket import TicketType, Ticket


class TicketTypeSchema(BaseModel):
    type_id: uuid.UUID
    type_name: str
    workout_number: int | None
    duration: datetime.timedelta

    @classmethod
    def from_entity(cls, ticket_type: TicketType) -> 'TicketTypeSchema':
        return cls(
            type_id=ticket_type.type_id,
            type_name=ticket_type.type_name.value,
            workout_number=ticket_type.workout_number.value,
            duration=ticket_type.duration,
        )


class TicketSchema(BaseModel):
    ticket_id: uuid.UUID
    ticket_type: TicketTypeSchema
    expression_date: datetime.date
    workout_number: int | None
    is_active: bool

    @classmethod
    def from_entity(cls, ticket: Ticket) -> 'TicketSchema':
        return cls(
            ticket_id=ticket.ticket_id,
            ticket_type=TicketTypeSchema.from_entity(ticket.ticket_type),
            expression_date=ticket.expression_date,
            workout_number=ticket.workout_number.value,
            is_active=ticket.is_active,
        )


class CreateTicketTypeSchema(BaseModel):
    type_name: str
    workout_number: int | None = None
    duration: datetime.timedelta


class UpdateTicketTypeSchema(BaseModel):
    type_name: str


class BuyTicketSchema(BaseModel):
    ticket_type_id: uuid.UUID
