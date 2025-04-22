import random

import pytest

from src.application.mediator.bootstrap import init_mediator
from src.application.mediator.mediator import Mediator


@pytest.fixture(scope="session")
def mediator() -> Mediator:
    return init_mediator()


@pytest.fixture
def fake_phone_number() -> str:
    value = "89"
    for _ in range(9):
        value += str(random.randint(0, 9))
    return value
