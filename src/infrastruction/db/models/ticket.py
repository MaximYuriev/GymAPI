import datetime
import uuid

from sqlalchemy.orm import Mapped, mapped_column

from src.domain.entities.ticket import TicketType
from src.domain.values.name import Name
from src.domain.values.workout_number import WorkoutNumber
from src.infrastruction.db.models.base import Base


class TicketTypeModel(Base):
    __tablename__ = "ticket_type"
    type_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    type_name: Mapped[str]
    workout_number: Mapped[int] = mapped_column(nullable=True)
    duration: Mapped[datetime.timedelta]

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
