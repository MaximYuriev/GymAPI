import uuid
from dataclasses import dataclass

from src.application.queries.base import BaseQuery
from src.application.queries.filters.pagination import PaginationFilter


@dataclass(frozen=True, eq=False)
class GetAllTicketTypesQuery(BaseQuery, PaginationFilter):
    pass


@dataclass(frozen=True, eq=False)
class GetTicketTypeQuery(BaseQuery):
    ticket_type_id: uuid.UUID
