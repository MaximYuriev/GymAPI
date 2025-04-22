import random

import pytest

from src.application.exceptions.pagination import LimitValueTooSmallException, OffsetValueTooSmallException
from src.application.queries.filters.pagination import PaginationFilter


def test_create_pagination_mixin_success():
    limit = random.randint(0, 500)
    offset = random.randint(0, 500)
    pagination = PaginationFilter(
        limit=limit,
        offset=offset,
    )

    assert pagination.limit == limit
    assert pagination.offset == offset

def test_create_pagination_mixin_w_limit_le_0():
    with pytest.raises(LimitValueTooSmallException):
        PaginationFilter(
            limit=random.randint(-500, 0),
            offset=random.randint(0, 500),
        )

def test_create_pagination_mixin_w_offset_lt_0():
    with pytest.raises(OffsetValueTooSmallException):
        PaginationFilter(
            limit=random.randint(0,500),
            offset=random.randint(-500, -1),
        )