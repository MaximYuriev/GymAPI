from dataclasses import dataclass
from typing import Protocol, Type, Any

from src.application.handlers.queries.base import BaseQueryHandler
from src.application.queries.base import BaseQuery


@dataclass(frozen=True, eq=False)
class QueryMediator[QT: Type[BaseQuery], QR: Any](Protocol):
    def register_query(
            self,
            query: QT,
            query_handler: Type[BaseQueryHandler],
    ) -> None:
        pass

    async def handle_query(self, query: BaseQuery) -> QR:
        pass
