import uuid
from dataclasses import dataclass

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.repositories.ticket import TicketTypeRepository, TicketRepository
from src.domain.entities.ticket import TicketType, Ticket
from src.infrastruction.db.models.ticket import TicketTypeModel, TicketModel


@dataclass(frozen=True, eq=False)
class SQLAlchemyTicketTypeRepository(TicketTypeRepository):
    _session: AsyncSession

    async def add_ticket_type(self, ticket_type: TicketType) -> None:
        model = TicketTypeModel.from_entity(ticket_type)
        self._session.add(model)
        await self._session.commit()

    async def check_exists_ticket_type_by_type_name(self, type_name: str) -> bool:
        query = select(TicketTypeModel).where(TicketTypeModel.type_name == type_name)
        return bool(await self._session.scalar(query))

    async def get_all_ticket_types(self, limit: int, offset: int) -> list[TicketType]:
        query = select(TicketTypeModel).limit(limit).offset(offset)
        query_result = await self._session.scalars(query)
        model_list = query_result.all()
        return [model.to_entity() for model in model_list]

    async def get_ticket_type_by_id(self, ticket_type_id: uuid.UUID) -> TicketType | None:
        query = select(TicketTypeModel).where(TicketTypeModel.type_id == ticket_type_id)
        model = await self._session.scalar(query)
        if model is not None:
            return model.to_entity()


@dataclass(frozen=True, eq=False)
class SQLAlchemyTicketRepository(TicketRepository):
    _session: AsyncSession

    async def add_ticket(self, ticket: Ticket) -> None:
        model = TicketModel.from_entity(ticket)
        self._session.add(model)
        await self._session.commit()

    async def check_exist_customers_active_ticket(self, customer_id: uuid.UUID) -> bool:
        query = (
            select(TicketModel)
            .where(
                and_(TicketModel.customer_id == customer_id, TicketModel.is_active == True)
            )
        )
        return bool(await self._session.scalar(query))
