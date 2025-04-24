import random

import pytest

from src.ioc import container
from src.application.mediator.mediator import Mediator


@pytest.fixture(scope="session")
async def mediator() -> Mediator:
    async with container() as _container:
        return await _container.get(Mediator)


@pytest.fixture
def fake_phone_number() -> str:
    value = "89"
    for _ in range(9):
        value += str(random.randint(0, 9))
    return value
