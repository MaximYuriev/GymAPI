from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.events.base import BaseEvent


@dataclass(frozen=True, eq=False)
class AMQPMessageBroker(ABC):
    @abstractmethod
    async def publish(self, exchange: str, queue: str, event: BaseEvent) -> None:
        pass
