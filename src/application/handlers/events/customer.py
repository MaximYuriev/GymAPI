from dataclasses import dataclass

from src.application.handlers.events.base import BaseEventHandler
from src.domain.events.customer import NewCustomerCreatedEvent, CustomerBoughtNewTicketEvent, \
    CustomerGotAccessToTrainingEvent


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


@dataclass(frozen=True, eq=False)
class CustomerGotAccessToTrainingEventHandler(BaseEventHandler):
    async def handle(self, event: CustomerGotAccessToTrainingEvent) -> None:
        template = (
            f"*Отправка смс на номер {event.phone}* "
            f"Уважаемый, {event.surname} {event.name} {event.patronymic}, благодарим за посещение тренажерного зала! "
        )
        if event.workout_number is not None:
            template += f"У вас осталось {event.workout_number} тренировок. "
        template += f"Абонемент действителен до {event.expression_date}"
        print(template)
