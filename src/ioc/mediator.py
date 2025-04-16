from typing import AsyncIterable

from dishka import Provider, from_context, Scope, provide, make_async_container
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from src.application.handlers.commands.ticket import CreateTicketTypeCommandHandler
from src.application.interfaces.repositories.ticket import TicketTypeRepository
from src.config import Config, config
from src.infrastruction.db.repositories.ticket import SQLAlchemyTicketTypeRepository


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


class TicketProvider(Provider):
    scope = Scope.REQUEST

    ticket_type_repository = provide(SQLAlchemyTicketTypeRepository, provides=TicketTypeRepository)
    create_ticket_type_command_handler = provide(CreateTicketTypeCommandHandler)


mediator_dependencies_container = make_async_container(
    SQLAlchemyProvider(),
    TicketProvider(),
    context={Config: config}
)
