import random
import uuid

import pytest
from faker import Faker

from src.application.commands.ticket import CreateTicketTypeCommand, DeleteTicketTypeCommand, UpdateTicketTypeCommand
from src.application.exceptions.ticket import TicketTypeAlreadyExistException, TicketTypeNotFoundException
from src.application.mediator.mediator import Mediator
from src.application.queries.ticket import GetAllTicketTypesQuery, GetTicketTypeQuery
from src.domain.entities.ticket import TicketType


@pytest.mark.usefixtures("prepare_database")
async def test_create_ticket_type_success(
        mediator: Mediator,
        faker: Faker,
):
    type_name = faker.text(max_nb_chars=100)
    workout_number = random.choice([None, random.randint(0, 100)])
    duration = faker.time_delta()
    command = CreateTicketTypeCommand(
        type_name=type_name,
        workout_number=workout_number,
        duration=duration,
    )

    ticket_type: TicketType = await mediator.handle_command(command)

    assert ticket_type.type_name.value == type_name
    assert ticket_type.workout_number.value == workout_number
    assert ticket_type.duration == duration


@pytest.mark.usefixtures("prepare_database")
async def test_create_ticket_type_w_null_workout_number(mediator: Mediator, faker: Faker):
    type_name = faker.text(max_nb_chars=100)
    duration = faker.time_delta()
    command = CreateTicketTypeCommand(
        type_name=type_name,
        workout_number=None,
        duration=duration,
    )

    ticket_type: TicketType = await mediator.handle_command(command)

    assert ticket_type.type_name.value == type_name
    assert ticket_type.workout_number.value is None
    assert ticket_type.duration == duration


@pytest.mark.usefixtures("prepare_database")
async def test_create_existed_ticket_type(mediator: Mediator, faker: Faker):
    type_name = faker.text(max_nb_chars=100)
    command = CreateTicketTypeCommand(
        type_name=type_name,
        workout_number=random.choice([None, random.randint(0, 100)]),
        duration=faker.time_delta(),
    )
    await mediator.handle_command(command)

    with pytest.raises(TicketTypeAlreadyExistException):
        await mediator.handle_command(command)


@pytest.mark.usefixtures("prepare_database")
async def test_get_ticket_type_list(mediator: Mediator, faker: Faker):
    command = CreateTicketTypeCommand(
        type_name=faker.text(max_nb_chars=100),
        workout_number=random.choice([None, random.randint(0, 100)]),
        duration=faker.time_delta(),
    )
    await mediator.handle_command(command)
    another_command = CreateTicketTypeCommand(
        type_name=faker.text(max_nb_chars=100),
        workout_number=random.choice([None, random.randint(0, 100)]),
        duration=faker.time_delta(),
    )
    await mediator.handle_command(another_command)

    query = GetAllTicketTypesQuery()
    ticket_type_list = await mediator.handle_query(query)

    assert len(ticket_type_list) == 2


@pytest.mark.usefixtures("prepare_database")
async def test_get_ticket_type_list_w_non_default_limit_and_offset_value(mediator: Mediator, faker: Faker):
    command = CreateTicketTypeCommand(
        type_name=faker.text(max_nb_chars=100),
        workout_number=random.choice([None, random.randint(0, 100)]),
        duration=faker.time_delta(),
    )
    await mediator.handle_command(command)
    another_command = CreateTicketTypeCommand(
        type_name=faker.text(max_nb_chars=100),
        workout_number=random.choice([None, random.randint(0, 100)]),
        duration=faker.time_delta(),
    )
    await mediator.handle_command(another_command)

    query = GetAllTicketTypesQuery(
        limit=1,
        offset=1
    )
    ticket_type_list = await mediator.handle_query(query)

    assert len(ticket_type_list) == 1


@pytest.mark.usefixtures("prepare_database")
async def test_get_empty_ticket_type_list(mediator: Mediator, faker: Faker):
    query = GetAllTicketTypesQuery()
    ticket_type_list = await mediator.handle_query(query)

    assert len(ticket_type_list) == 0


@pytest.mark.usefixtures("prepare_database")
async def test_delete_ticket_type_success(mediator: Mediator, faker: Faker):
    command = CreateTicketTypeCommand(
        type_name=faker.text(max_nb_chars=100),
        workout_number=random.choice([None, random.randint(0, 100)]),
        duration=faker.time_delta(),
    )
    ticket_type: TicketType = await mediator.handle_command(command)

    command = DeleteTicketTypeCommand(
        ticket_type_id=ticket_type.type_id,
    )
    deleted_ticket_type: TicketType = await mediator.handle_command(command)

    assert ticket_type == deleted_ticket_type
    with pytest.raises(TicketTypeNotFoundException):
        query = GetTicketTypeQuery(deleted_ticket_type.type_id)
        await mediator.handle_query(query)


@pytest.mark.usefixtures("prepare_database")
async def test_delete_not_existed_ticket_type(mediator: Mediator):
    with pytest.raises(TicketTypeNotFoundException):
        command = DeleteTicketTypeCommand(
            ticket_type_id=uuid.uuid4(),
        )
        await mediator.handle_command(command)


@pytest.mark.usefixtures("prepare_database")
async def test_update_ticket_type_success(mediator: Mediator, faker: Faker):
    command = CreateTicketTypeCommand(
        type_name=faker.text(max_nb_chars=100),
        workout_number=random.choice([None, random.randint(0, 100)]),
        duration=faker.time_delta(),
    )
    ticket_type: TicketType = await mediator.handle_command(command)

    command = UpdateTicketTypeCommand(
        ticket_type_id=ticket_type.type_id,
        type_name=faker.text(max_nb_chars=100),
    )
    updated_ticket_type: TicketType = await mediator.handle_command(command)

    assert updated_ticket_type != ticket_type
    assert updated_ticket_type.type_name != ticket_type.type_name


@pytest.mark.usefixtures("prepare_database")
async def test_update_not_existed_ticket_type(mediator: Mediator, faker: Faker):
    with pytest.raises(TicketTypeNotFoundException):
        command = UpdateTicketTypeCommand(
            ticket_type_id=uuid.uuid4(),
            type_name=faker.text(max_nb_chars=100),
        )
        await mediator.handle_command(command)


@pytest.mark.usefixtures("prepare_database")
async def test_update_ticket_type_w_not_unique_type_name(mediator: Mediator, faker: Faker):
    type_name = faker.text(max_nb_chars=100)
    command = CreateTicketTypeCommand(
        type_name=type_name,
        workout_number=random.choice([None, random.randint(0, 100)]),
        duration=faker.time_delta(),
    )
    ticket_type: TicketType = await mediator.handle_command(command)

    command = UpdateTicketTypeCommand(
        ticket_type_id=ticket_type.type_id,
        type_name=type_name,
    )

    with pytest.raises(TicketTypeAlreadyExistException):
        await mediator.handle_command(command)


@pytest.mark.usefixtures("prepare_database")
async def test_get_ticket_type_success(mediator: Mediator, faker: Faker):
    command = CreateTicketTypeCommand(
        type_name=faker.text(max_nb_chars=100),
        workout_number=random.choice([None, random.randint(0, 100)]),
        duration=faker.time_delta(),
    )
    ticket_type: TicketType = await mediator.handle_command(command)

    query = GetTicketTypeQuery(
        ticket_type_id=ticket_type.type_id,
    )
    founded_ticket_type: TicketType = await mediator.handle_query(query)

    assert ticket_type == founded_ticket_type


@pytest.mark.usefixtures("prepare_database")
async def test_get_not_existed_ticket_type(mediator: Mediator):
    query = GetTicketTypeQuery(
        ticket_type_id=uuid.uuid4(),
    )

    with pytest.raises(TicketTypeNotFoundException):
        await mediator.handle_query(query)
