import uuid
from dataclasses import dataclass, field

from src.domain.entities.base import BaseEntity
from src.domain.entities.ticket import Ticket
from src.domain.events.customer import NewCustomerCreatedEvent
from src.domain.values.name import Name, Patronymic, Surname
from src.domain.values.phone import PhoneNumber


@dataclass
class Customer(BaseEntity):
    consumer_id: uuid.UUID = field(default_factory=uuid.uuid4, kw_only=True)
    name: Name
    surname: Surname
    patronymic: Patronymic
    phone: PhoneNumber
    tickets: list[Ticket] = field(default_factory=list, kw_only=True)

    @classmethod
    def create_customer(cls, name: Name, surname: Surname, patronymic: Patronymic, phone: PhoneNumber):
        customer = cls(
            name=name,
            surname=surname,
            patronymic=patronymic,
            phone=phone,
        )

        event = NewCustomerCreatedEvent(
            name=customer.name.value,
            surname=customer.surname.value,
            patronymic=customer.patronymic.value,
            phone=customer.phone.value,
        )
        customer._push_event(event)

        return customer
