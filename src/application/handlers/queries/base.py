from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from src.application.queries.base import BaseQuery


@dataclass(frozen=True, eq=False)
class BaseQueryHandler[QT:BaseQuery, QR:Any](ABC):
    @abstractmethod
    async def handle(self, query: QT) -> QR:
        pass
