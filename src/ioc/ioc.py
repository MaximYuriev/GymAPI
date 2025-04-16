from dishka import Provider, provide, Scope, make_async_container

from src.application.commands.ticket import CreateTicketTypeCommand
from src.application.handlers.commands.ticket import CreateTicketTypeCommandHandler
from src.application.mediator import Mediator


class MediatorProvider(Provider):
    @provide(scope=Scope.APP)
    def init_mediator(self) -> Mediator:
        mediator = Mediator()

        mediator.register_command(
            command=CreateTicketTypeCommand,
            command_handler=CreateTicketTypeCommandHandler,
        )

        return mediator


container = make_async_container(
    MediatorProvider(),
)
