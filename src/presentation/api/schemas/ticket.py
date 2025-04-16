import datetime
import uuid

from pydantic import BaseModel

from src.domain.entities.ticket import TicketType


class TicketTypeSchema(BaseModel):
    type_id: uuid.UUID
    type_name: str
    workout_number: int
    duration: datetime.timedelta

    @classmethod
    def from_entity(cls, ticket_type: TicketType) -> 'TicketTypeSchema':
        return cls(
            type_id=ticket_type.type_id,
            type_name=ticket_type.type_name.value,
            workout_number=ticket_type.workout_number.value,
            duration=ticket_type.duration,
        )


class CreateTicketTypeSchema(BaseModel):
    type_name: str
    workout_number: int
    duration: datetime.timedelta
