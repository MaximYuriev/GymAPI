import random

import pytest
from dishka import AsyncContainer

from src.application.commands.customer import CreateCustomerCommand
from src.application.commands.ticket import CreateTicketTypeCommand
from src.application.handlers.commands.customer import CreateCustomerCommandHandler
from src.application.handlers.commands.ticket import CreateTicketTypeCommandHandler
from src.application.handlers.queries.ticket import GetAllTicketTypesQueryHandler
from src.application.mediator import Mediator
from src.application.queries.ticket import GetAllTicketTypesQuery
from src.ioc.mediator import mediator_dependencies_container


@pytest.fixture
def mediator() -> Mediator:
    mediator = Mediator(mediator_dependencies_container)

    mediator.register_command(
        command=CreateTicketTypeCommand,
        command_handler=CreateTicketTypeCommandHandler,
    )
    mediator.register_command(
        command=CreateCustomerCommand,
        command_handler=CreateCustomerCommandHandler,
    )

    mediator.register_query(
        query=GetAllTicketTypesQuery,
        query_handler=GetAllTicketTypesQueryHandler,
    )


    return mediator


@pytest.fixture
def fake_phone_number() -> str:
    value = "89"
    for _ in range(9):
        value += str(random.randint(0, 9))
    return value
