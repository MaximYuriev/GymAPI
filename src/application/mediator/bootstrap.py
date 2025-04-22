from src.application.commands.customer import CreateCustomerCommand
from src.application.commands.ticket import CreateTicketTypeCommand
from src.application.handlers.commands.customer import CreateCustomerCommandHandler
from src.application.handlers.commands.ticket import CreateTicketTypeCommandHandler
from src.application.handlers.queries.ticket import GetAllTicketTypesQueryHandler
from src.application.mediator.ioc import mediator_dependencies_container
from src.application.mediator.mediator import Mediator
from src.application.queries.ticket import GetAllTicketTypesQuery


def init_mediator() -> Mediator:
    mediator = Mediator(mediator_dependencies_container)

    # register commands
    mediator.register_command(
        command=CreateTicketTypeCommand,
        command_handler=CreateTicketTypeCommandHandler,
    )
    mediator.register_command(
        command=CreateCustomerCommand,
        command_handler=CreateCustomerCommandHandler,
    )

    # register queries
    mediator.register_query(
        query=GetAllTicketTypesQuery,
        query_handler=GetAllTicketTypesQueryHandler,
    )

    return mediator
