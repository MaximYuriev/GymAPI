import datetime
import random

import pytest
from faker.proxy import Faker

from src.domain.entities.ticket import TicketType
from src.domain.values.name import Name
from src.domain.values.workout_number import WorkoutNumber


@pytest.fixture
def ticket_type(faker: Faker) -> TicketType:
    type_name = Name(faker.text(max_nb_chars=100))
    workout_number = WorkoutNumber(random.randint(0, 100)) if random.randint(1, 2) == 1 else None
    duration = datetime.timedelta(days=random.randint(1, 100))
    return TicketType(
        type_name=type_name,
        workout_number=workout_number,
        duration=duration,
    )
