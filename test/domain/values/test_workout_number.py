import random

import pytest

from src.domain.exceptions.workout_number import WorkoutNumberTooSmallException, WorkoutNumberTooBigException
from src.domain.values.workout_number import WorkoutNumber


def test_create_workout_number_success():
    value = random.randint(0, 100)
    workout_number = WorkoutNumber(value)

    assert workout_number.value == value


def test_create_too_small_workout_number():
    with pytest.raises(WorkoutNumberTooSmallException):
        WorkoutNumber(random.randint(-10000, -1))


def test_create_too_big_workout_number():
    with pytest.raises(WorkoutNumberTooBigException):
        WorkoutNumber(random.randint(101, 100000))


def test_create_null_workout_number():
    value = None
    workout_number = WorkoutNumber(value)

    assert workout_number.value is None


def test_compare_workout_number():
    workout_number_1 = WorkoutNumber(random.randint(0, 10))
    workout_number_2 = WorkoutNumber(random.randint(11, 100))
    workout_number_3 = WorkoutNumber(workout_number_1.value)

    assert workout_number_2 > workout_number_1
    assert workout_number_3 == workout_number_1
