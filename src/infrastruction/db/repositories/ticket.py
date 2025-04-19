from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.repositories.ticket import TicketTypeRepository
from src.domain.entities.ticket import TicketType
from src.infrastruction.db.models.ticket import TicketTypeModel


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
