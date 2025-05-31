from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, eq=False)
class AMQPMessageBroker(ABC):
    @abstractmethod
    async def publish(self, exchange: str, queue: str, data: dict[str, Any]):
        pass
