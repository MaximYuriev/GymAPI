from dataclasses import dataclass
from typing import Protocol, Type, Any

from src.application.handlers.events.base import BaseEventHandler
from src.domain.events.base import BaseEvent


@dataclass(frozen=True, eq=False)
class EventMediator[ET: Type[BaseEvent], ER: Any](Protocol):
    def register_event(
            self,
            event: ET,
            event_handler: Type[BaseEventHandler],
    ) -> None:
        pass

    async def handle_event(self, event: BaseEvent) -> ER:
        pass
