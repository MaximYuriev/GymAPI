from dataclasses import dataclass, asdict

from src.application.handlers.events.base import BaseEventHandler
from src.domain.events.customer import NewCustomerCreatedEvent, CustomerBoughtNewTicketEvent, \
    CustomerGotAccessToTrainingEvent


@dataclass(frozen=True, eq=False)
class NewCustomerCreatedEventHandler(BaseEventHandler):
    async def handle(self, event: NewCustomerCreatedEvent) -> None:
        await self._message_broker.publish(
            exchange=self._exchange,
            queue=self._queue,
            event=event,
        )


@dataclass(frozen=True, eq=False)
class CustomerBoughtNewTicketEventHandler(BaseEventHandler):
    async def handle(self, event: CustomerBoughtNewTicketEvent) -> None:
        await self._message_broker.publish(
            exchange=self._exchange,
            queue=self._queue,
            event=event,
        )


@dataclass(frozen=True, eq=False)
class CustomerGotAccessToTrainingEventHandler(BaseEventHandler):
    async def handle(self, event: CustomerGotAccessToTrainingEvent) -> None:
        await self._message_broker.publish(
            exchange=self._exchange,
            queue=self._queue,
            event=event,
        )
