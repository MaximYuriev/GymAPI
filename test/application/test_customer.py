import random

import pytest
from faker.proxy import Faker

from src.application.commands.customer import CreateCustomerCommand
from src.application.exceptions.customer import PhoneNumberNotUniqueException
from src.application.mediator.mediator import Mediator
from src.domain.entities.customer import Customer


@pytest.mark.usefixtures("prepare_database")
async def test_create_customer_success(
        mediator: Mediator,
        fake_phone_number: str,
        faker: Faker,
):
    command = CreateCustomerCommand(
        name=faker.name(),
        surname=faker.name(),
        patronymic=faker.name(),
        phone=fake_phone_number,
    )

    customer: Customer = await mediator.handle_command(command)

    assert customer.name.value == command.name
    assert customer.phone.value == command.phone


@pytest.mark.usefixtures("prepare_database")
async def test_create_customer_w_null_patronymic(
        mediator: Mediator,
        fake_phone_number: str,
        faker: Faker,
):
    command = CreateCustomerCommand(
        name=faker.name(),
        surname=faker.name(),
        patronymic=None,
        phone=fake_phone_number,
    )

    customer: Customer = await mediator.handle_command(command)

    assert customer.patronymic.value is None
    assert customer.name.value == command.name
    assert customer.phone.value == command.phone


@pytest.mark.usefixtures("prepare_database")
async def test_create_customer_w_not_unique_phone_number(
        mediator: Mediator,
        fake_phone_number: str,
        faker: Faker,
):
    command = CreateCustomerCommand(
        name=faker.name(),
        surname=faker.name(),
        patronymic=random.choice([None, faker.name()]),
        phone=fake_phone_number,
    )
    await mediator.handle_command(command)

    with pytest.raises(PhoneNumberNotUniqueException):
        await mediator.handle_command(command)
