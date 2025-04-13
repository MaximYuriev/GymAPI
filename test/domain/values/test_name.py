import pytest

from src.domain.exceptions.name import NullNameException, NameTooLongException
from src.domain.values.name import Name, Surname, Patronymic


def test_create_name_success(faker):
    value = faker.first_name()
    name = Name(value)

    assert name.value == value


def test_create_empty_name():
    with pytest.raises(NullNameException):
        Name("")


def test_create_too_long_name(faker):
    with pytest.raises(NameTooLongException):
        value = faker.text(max_nb_chars=500)
        Name(value)


def test_create_surname_success(faker):
    value = faker.first_name()
    surname = Surname(value)

    assert surname.value == value


def test_create_empty_surname():
    with pytest.raises(NullNameException):
        Surname("")


def test_create_too_long_surname(faker):
    with pytest.raises(NameTooLongException):
        value = faker.text(max_nb_chars=500)
        Surname(value)


def test_create_patronymic_success(faker):
    value = faker.first_name()
    patronymic = Patronymic(value)

    assert patronymic.value == value


def test_create_empty_patronymic():
    with pytest.raises(NullNameException):
        Patronymic("")


def test_create_too_long_patronymic(faker):
    with pytest.raises(NameTooLongException):
        value = faker.text(max_nb_chars=500)
        Patronymic(value)

def test_create_null_patronymic():
    patronymic = Patronymic()

    assert patronymic.value is None