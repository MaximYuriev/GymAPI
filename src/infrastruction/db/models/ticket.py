import datetime
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.entities.ticket import TicketType, Ticket
from src.domain.values.name import Name
from src.domain.values.workout_number import WorkoutNumber
from src.infrastruction.db.models.base import Base
from src.infrastruction.db.models.customer import CustomerModel


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


class TicketModel(Base):
    __tablename__ = "ticket"
    ticket_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    customer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(CustomerModel.customer_id, ondelete="CASCADE"))
    ticket_type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(TicketTypeModel.type_id, ondelete="CASCADE"))
    expression_date: Mapped[datetime.date]
    workout_number: Mapped[int] = mapped_column(nullable=True)
    is_active: Mapped[bool]

    ticket_type: Mapped[TicketTypeModel] = relationship()

    @classmethod
    def from_entity(cls, ticket: Ticket) -> "TicketModel":
        return cls(
            ticket_id=ticket.ticket_id,
            customer_id=ticket.customer_id,
            ticket_type_id=ticket.ticket_type.type_id,
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
