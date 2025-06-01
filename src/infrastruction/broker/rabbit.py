import json
from dataclasses import dataclass, asdict
from datetime import date, datetime

from aio_pika import Message
from aio_pika.abc import AbstractRobustChannel, AbstractRobustExchange, AbstractRobustQueue

from src.application.interfaces.brokers.amqp import AMQPMessageBroker
from src.domain.events.base import BaseEvent


@dataclass(frozen=True, eq=False)
class RMQMessageBroker(AMQPMessageBroker):
    _channel: AbstractRobustChannel

    async def publish(self, exchange: str, queue: str, event: BaseEvent) -> None:
        exchange = await self._declare_exchange(exchange)
        queue = await self._declare_queue(queue)
        await queue.bind(exchange=exchange.name, routing_key=queue.name)

        message = self._convert_event_to_message_broker(event)

        await exchange.publish(
            message=message,
            routing_key=queue.name,
        )

    async def _declare_exchange(self, exchange_name: str) -> AbstractRobustExchange:
        return await self._channel.declare_exchange(exchange_name)

    async def _declare_queue(self, queue_name: str) -> AbstractRobustQueue:
        return await self._channel.declare_queue(queue_name)

    @staticmethod
    def _convert_event_to_message_broker(event: BaseEvent) -> Message:
        data = asdict(event)

        for key, value in data.items():
            if isinstance(value, (date, datetime)):
                data[key] = value.isoformat()

        return Message(
            body=json.dumps(data).encode(),
            content_type="application/json"
        )
