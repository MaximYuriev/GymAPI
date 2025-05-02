import uuid
from dataclasses import dataclass

from src.application.queries.base import BaseQuery
from src.application.queries.filters.pagination import PaginationFilter


@dataclass(frozen=True, eq=False)
class GetAllCustomerTicketQuery(BaseQuery, PaginationFilter):
    customer_id: uuid.UUID


@dataclass(frozen=True, eq=False)
class GetActiveCustomerTicketQuery(BaseQuery):
    customer_id: uuid.UUID
