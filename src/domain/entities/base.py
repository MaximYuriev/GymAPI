from abc import ABC
from dataclasses import dataclass, field

from src.domain.events.base import BaseEvent


@dataclass
class BaseEntity(ABC):
    _event_list: list[BaseEvent] = field(default_factory=list, kw_only=True)

    def _push_event(self, base_event: BaseEvent) -> None:
        self._event_list.append(base_event)

    def pull_event(self) -> list[BaseEvent]:
        pulled_event_list = [event for event in self._event_list]
        self._event_list.clear()
        return pulled_event_list
