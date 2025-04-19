from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class BaseQuery(ABC):
    pass


@dataclass(frozen=True, eq=False)
class PaginationMixin:
    limit: int = 5
    offset: int = 0
