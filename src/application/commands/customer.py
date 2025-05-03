import uuid
from dataclasses import dataclass

from src.application.commands.base import BaseCommand


@dataclass(frozen=True, eq=False)
class CreateCustomerCommand(BaseCommand):
    name: str
    surname: str
    patronymic: str | None
    phone: str


@dataclass(frozen=True, eq=False)
class BuyNewTicketCommand(BaseCommand):
    customer_id: uuid.UUID
    ticket_type_id: uuid.UUID


@dataclass(frozen=True, eq=False)
class GetAccessToTrainingCommand(BaseCommand):
    customer_id: uuid.UUID
    ticket_id: uuid.UUID
