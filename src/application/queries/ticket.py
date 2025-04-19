from dataclasses import dataclass

from src.application.queries.base import BaseQuery, PaginationMixin


@dataclass(frozen=True, eq=False)
class GetAllTicketTypesQuery(BaseQuery, PaginationMixin):
    pass
