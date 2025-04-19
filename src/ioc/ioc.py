from dishka import Provider, provide, Scope, make_async_container

from src.application.commands.ticket import CreateTicketTypeCommand
from src.application.handlers.commands.ticket import CreateTicketTypeCommandHandler
from src.application.handlers.queries.ticket import GetAllTicketTypesQueryHandler
from src.application.mediator import Mediator
from src.application.queries.ticket import GetAllTicketTypesQuery


class MediatorProvider(Provider):
    @provide(scope=Scope.APP)
    def init_mediator(self) -> Mediator:
        mediator = Mediator()

        mediator.register_command(
            command=CreateTicketTypeCommand,
            command_handler=CreateTicketTypeCommandHandler,
        )

        mediator.register_query(
            query=GetAllTicketTypesQuery,
            query_handler=GetAllTicketTypesQueryHandler,
        )

        return mediator


container = make_async_container(
    MediatorProvider(),
)
