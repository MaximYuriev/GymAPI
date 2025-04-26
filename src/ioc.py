from typing import AsyncIterable

from dishka import Provider, from_context, Scope, provide, AsyncContainer, make_async_container
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from src.application.commands.customer import CreateCustomerCommand, BuyNewTicketCommand
from src.application.commands.ticket import CreateTicketTypeCommand
from src.application.handlers.commands.customer import CreateCustomerCommandHandler, BuyNewTicketCommandHandler
from src.application.handlers.commands.ticket import CreateTicketTypeCommandHandler
from src.application.handlers.events.customer import NewCustomerCreatedEventHandler, CustomerBoughtNewTicketEventHandler
from src.application.handlers.queries.ticket import GetAllTicketTypesQueryHandler
from src.application.interfaces.repositories.customer import CustomerRepository
from src.application.interfaces.repositories.ticket import TicketTypeRepository, TicketRepository
from src.application.mediator.mediator import Mediator
from src.application.mediator.protocols.event_mediator import EventMediator
from src.application.queries.ticket import GetAllTicketTypesQuery
from src.config import Config, config
from src.domain.events.customer import NewCustomerCreatedEvent, CustomerBoughtNewTicketEvent
from src.infrastruction.db.repositories.customer import SQLAlchemyCustomerRepository
from src.infrastruction.db.repositories.ticket import SQLAlchemyTicketTypeRepository, SQLAlchemyTicketRepository


class SQLAlchemyProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_async_engine(self, config: Config) -> AsyncEngine:
        return create_async_engine(config.postgres.db_url, echo=False)

    @provide(scope=Scope.APP)
    def get_async_session_maker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session


class MediatorProvider(Provider):
    @provide(scope=Scope.APP)
    def init_mediator(self) -> Mediator:
        mediator = Mediator()

        # register di
        mediator.register_di_container(
            di_container=container
        )

        # register events
        mediator.register_event(
            event=NewCustomerCreatedEvent,
            event_handler=NewCustomerCreatedEventHandler,
        )
        mediator.register_event(
            event=CustomerBoughtNewTicketEvent,
            event_handler=CustomerBoughtNewTicketEventHandler,
        )

        # register commands
        mediator.register_command(
            command=CreateTicketTypeCommand,
            command_handler=CreateTicketTypeCommandHandler,
        )
        mediator.register_command(
            command=CreateCustomerCommand,
            command_handler=CreateCustomerCommandHandler,
        )
        mediator.register_command(
            command=BuyNewTicketCommand,
            command_handler=BuyNewTicketCommandHandler,
        )

        # register queries
        mediator.register_query(
            query=GetAllTicketTypesQuery,
            query_handler=GetAllTicketTypesQueryHandler,
        )

        return mediator

    @provide(scope=Scope.APP)
    def event_mediator(self, mediator: Mediator) -> EventMediator:
        return mediator


class TicketProvider(Provider):
    scope = Scope.REQUEST

    ticket_type_repository = provide(SQLAlchemyTicketTypeRepository, provides=TicketTypeRepository)
    ticket_repository = provide(SQLAlchemyTicketRepository, provides=TicketRepository)

    create_ticket_type_command_handler = provide(CreateTicketTypeCommandHandler)

    get_all_ticket_types_query_handler = provide(GetAllTicketTypesQueryHandler)


class CustomerProvider(Provider):
    scope = Scope.REQUEST

    customer_repository = provide(SQLAlchemyCustomerRepository, provides=CustomerRepository)

    create_customer_command_handler = provide(CreateCustomerCommandHandler)
    buy_new_ticket_command_handler = provide(BuyNewTicketCommandHandler)

    new_customer_created_event_handler = provide(NewCustomerCreatedEventHandler)
    bought_new_ticket_event_handler = provide(CustomerBoughtNewTicketEventHandler)


async def create_di_container() -> AsyncContainer:
    di_container = make_async_container(
        SQLAlchemyProvider(),
        MediatorProvider(),
        TicketProvider(),
        CustomerProvider(),
        context={Config: config}
    )

    async with di_container() as _container:
        mediator = await _container.get(Mediator)
        mediator.register_di_container(di_container)

    return di_container


container = make_async_container(
    SQLAlchemyProvider(),
    MediatorProvider(),
    TicketProvider(),
    CustomerProvider(),
    context={Config: config}
)
