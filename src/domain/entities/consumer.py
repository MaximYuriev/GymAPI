import uuid
from dataclasses import dataclass, field

from src.domain.entities.ticket import Ticket
from src.domain.values.name import Name, Patronymic, Surname
from src.domain.values.phone import PhoneNumber


@dataclass
class Consumer:
    consumer_id: uuid.UUID = field(default_factory=uuid.uuid4, kw_only=True)
    name: Name
    surname: Surname
    patronymic: Patronymic
    phone: PhoneNumber
    tickets: list[Ticket] = field(default_factory=list, kw_only=True)
