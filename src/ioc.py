from beanie import init_beanie
from dishka import Provider, from_context, Scope, provide, make_async_container
from motor.motor_asyncio import AsyncIOMotorClient

from src.application.commands.customer import CreateCustomerCommand, BuyNewTicketCommand
from src.application.commands.ticket import CreateTicketTypeCommand, UpdateTicketTypeCommand, DeleteTicketTypeCommand
from src.application.handlers.commands.customer import CreateCustomerCommandHandler, BuyNewTicketCommandHandler
from src.application.handlers.commands.ticket import CreateTicketTypeCommandHandler, UpdateTicketTypeCommandHandler, \
    DeleteTicketTypeCommandHandler
from src.application.handlers.events.customer import NewCustomerCreatedEventHandler, CustomerBoughtNewTicketEventHandler
from src.application.handlers.queries.customer import GetAllCustomerTicketQueryHandler, \
    GetActiveCustomerTicketQueryHandler
from src.application.handlers.queries.ticket import GetAllTicketTypesQueryHandler, GetTicketTypeQueryHandler
from src.application.interfaces.repositories.customer import CustomerRepository
from src.application.interfaces.repositories.ticket import TicketTypeRepository, TicketRepository
from src.application.mediator.mediator import Mediator
from src.application.mediator.protocols.event_mediator import EventMediator
from src.application.queries.customer import GetAllCustomerTicketQuery, GetActiveCustomerTicketQuery
from src.application.queries.ticket import GetAllTicketTypesQuery, GetTicketTypeQuery
from src.config import Config, config
from src.domain.events.customer import NewCustomerCreatedEvent, CustomerBoughtNewTicketEvent
from src.infrastruction.db.models.customer import CustomerModel
from src.infrastruction.db.models.ticket import TicketTypeModel, TicketModel
from src.infrastruction.db.repositories.customer import BeanieCustomerRepository
from src.infrastruction.db.repositories.ticket import BeanieTicketRepository, BeanieTicketTypeRepository


class BeanieProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_mongodb_async_client(self, _config: Config) -> AsyncIOMotorClient:
        client = AsyncIOMotorClient(
            _config.mongodb.url,
            connectTimeoutMS=5000,
        )

        await init_beanie(
            database=client.get_database(_config.mongodb.db_name),
            document_models=[
                TicketModel,
                CustomerModel,
                TicketTypeModel,
            ],
        )

        return client


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
            command=UpdateTicketTypeCommand,
            command_handler=UpdateTicketTypeCommandHandler,
        )
        mediator.register_command(
            command=DeleteTicketTypeCommand,
            command_handler=DeleteTicketTypeCommandHandler,
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
        mediator.register_query(
            query=GetTicketTypeQuery,
            query_handler=GetTicketTypeQueryHandler,
        )
        mediator.register_query(
            query=GetAllCustomerTicketQuery,
            query_handler=GetAllCustomerTicketQueryHandler,
        )
        mediator.register_query(
            query=GetActiveCustomerTicketQuery,
            query_handler=GetActiveCustomerTicketQueryHandler,
        )

        return mediator

    @provide(scope=Scope.APP)
    def event_mediator(self, mediator: Mediator) -> EventMediator:
        return mediator


class TicketProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def init_beanie_ticket_type_repository(self, client: AsyncIOMotorClient) -> BeanieTicketTypeRepository:
        return BeanieTicketTypeRepository()

    @provide(scope=Scope.APP)
    async def init_beanie_ticket_repository(self, client: AsyncIOMotorClient) -> BeanieTicketRepository:
        return BeanieTicketRepository()

    ticket_type_repository = provide(init_beanie_ticket_type_repository, provides=TicketTypeRepository, scope=Scope.APP)
    ticket_repository = provide(init_beanie_ticket_repository, provides=TicketRepository, scope=Scope.APP)

    create_ticket_type_command_handler = provide(CreateTicketTypeCommandHandler)
    update_ticket_type_command_handler = provide(UpdateTicketTypeCommandHandler)
    delete_ticket_type_command_handler = provide(DeleteTicketTypeCommandHandler)

    get_all_ticket_types_query_handler = provide(GetAllTicketTypesQueryHandler)
    get_ticket_type_query_handler = provide(GetTicketTypeQueryHandler)


class CustomerProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def init_beanie_customer_repository(self, client: AsyncIOMotorClient) -> BeanieCustomerRepository:
        return BeanieCustomerRepository()

    customer_repository = provide(BeanieCustomerRepository, provides=CustomerRepository, scope=Scope.APP)

    create_customer_command_handler = provide(CreateCustomerCommandHandler)
    buy_new_ticket_command_handler = provide(BuyNewTicketCommandHandler)

    new_customer_created_event_handler = provide(NewCustomerCreatedEventHandler)
    bought_new_ticket_event_handler = provide(CustomerBoughtNewTicketEventHandler)

    get_all_customer_ticket_handler = provide(GetAllCustomerTicketQueryHandler)
    get_active_customer_ticket_handler = provide(GetActiveCustomerTicketQueryHandler)


container = make_async_container(
    BeanieProvider(),
    MediatorProvider(),
    TicketProvider(),
    CustomerProvider(),
    context={Config: config}
)
