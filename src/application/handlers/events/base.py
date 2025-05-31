from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from src.application.interfaces.brokers.amqp import AMQPMessageBroker
from src.domain.events.base import BaseEvent


@dataclass(frozen=True, eq=False)
class BaseEventHandler[ET:BaseEvent, ER:Any](ABC):
    _message_broker: AMQPMessageBroker

    @abstractmethod
    async def handle(self, event: ET) -> ER:
        pass
