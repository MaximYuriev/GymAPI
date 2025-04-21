from dishka import Provider, provide, Scope, make_async_container, AsyncContainer

from src.application.commands.ticket import CreateTicketTypeCommand
from src.application.handlers.commands.ticket import CreateTicketTypeCommandHandler
from src.application.handlers.queries.ticket import GetAllTicketTypesQueryHandler
from src.application.mediator import Mediator
from src.application.queries.ticket import GetAllTicketTypesQuery
from src.ioc.mediator import mediator_dependencies_container


class MediatorProvider(Provider):
    @provide(scope=Scope.APP)
    def init_mediator(self, di_container: AsyncContainer) -> Mediator:
        mediator = Mediator(di_container)

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
    context={AsyncContainer: mediator_dependencies_container},
)
