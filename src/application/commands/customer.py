from dataclasses import dataclass

from src.application.commands.base import BaseCommand


@dataclass(frozen=True, eq=False)
class CreateCustomerCommand(BaseCommand):
    name: str
    surname: str
    patronymic: str | None
    phone: str
