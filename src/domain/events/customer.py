import datetime
from dataclasses import dataclass

from src.domain.events.base import BaseEvent


@dataclass(frozen=True, eq=False)
class NewCustomerCreatedEvent(BaseEvent):
    name: str
    surname: str
    patronymic: str | None
    phone: str


@dataclass(frozen=True, eq=False)
class CustomerBoughtNewTicketEvent(BaseEvent):
    name: str
    surname: str
    patronymic: str | None
    phone: str


@dataclass(frozen=True, eq=False)
class CustomerGotAccessToTrainingEvent(BaseEvent):
    name: str
    surname: str
    patronymic: str | None
    phone: str
    workout_number: str | None
    expression_date: datetime.date
