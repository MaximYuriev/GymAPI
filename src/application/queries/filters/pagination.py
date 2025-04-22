from dataclasses import dataclass, field

from src.application.exceptions.pagination import LimitValueTooSmallException, OffsetValueTooSmallException


@dataclass(frozen=True, eq=False)
class PaginationFilter:
    limit: int = field(default=5, kw_only=True)
    offset: int = field(default=0, kw_only=True)

    def __post_init__(self):
        self._validate()

    def _validate(self) -> None:
        self._validate_limit_value()
        self._validate_offset_value()

    def _validate_limit_value(self) -> None:
        if self.limit <= 0:
            raise LimitValueTooSmallException(self.limit)

    def _validate_offset_value(self) -> None:
        if self.offset < 0:
            raise OffsetValueTooSmallException(self.offset)
