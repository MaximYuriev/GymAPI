from dataclasses import dataclass
from typing import Any

from aio_pika.abc import AbstractRobustConnection

from src.application.interfaces.brokers.amqp import AMQPMessageBroker


@dataclass(frozen=True, eq=False)
class RMQMessageBroker(AMQPMessageBroker):
    _connection: AbstractRobustConnection

    async def publish(self, exchange: str, queue: str, data: dict[str, Any]):
        pass
