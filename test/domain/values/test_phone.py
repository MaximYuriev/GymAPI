import random

import pytest

from src.domain.exceptions.phone import PhoneFormatException
from src.domain.values.phone import PhoneNumber


def test_create_phone_success():
    value = "89"
    for _ in range(9):
        value += str(random.randint(0, 9))

    phone = PhoneNumber(value)

    assert phone.value == value


def test_create_phone_with_too_short_number():
    value = "89"
    for _ in range(random.randint(0, 8)):
        value += str(random.randint(0, 9))
    with pytest.raises(PhoneFormatException):
        PhoneNumber(value)


def test_create_phone_with_too_long_number():
    value = "89"
    for _ in range(random.randint(10, 10000)):
        value += str(random.randint(0, 9))
    with pytest.raises(PhoneFormatException):
        PhoneNumber(value)


def test_create_phone_with_incorrect_first_numbers_format():
    value = "98"
    for _ in range(9):
        value += str(random.randint(0, 9))
    with pytest.raises(PhoneFormatException):
        PhoneNumber(value)
