from dataclasses import dataclass

from src.application.handlers.events.base import BaseEventHandler
from src.domain.events.customer import NewCustomerCreatedEvent, CustomerBoughtNewTicketEvent


@dataclass(frozen=True, eq=False)
class NewCustomerCreatedEventHandler(BaseEventHandler):
    async def handle(self, event: NewCustomerCreatedEvent) -> None:
        print(
            f"*Отправка смс на номер {event.phone}* "
            f"Уважаемый, {event.surname} {event.name} {event.patronymic}, благодарим за регистрацию в нашем сервисе!"
        )


@dataclass(frozen=True, eq=False)
class CustomerBoughtNewTicketEventHandler(BaseEventHandler):
    async def handle(self, event: CustomerBoughtNewTicketEvent) -> None:
        print(
            f"*Отправка смс на номер {event.phone}* "
            f"Уважаемый, {event.surname} {event.name} {event.patronymic}, благодарим за покупку абонемента!"
        )
