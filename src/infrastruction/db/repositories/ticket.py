import uuid
from dataclasses import dataclass

from src.application.interfaces.repositories.ticket import TicketTypeRepository, TicketRepository
from src.domain.entities.ticket import TicketType, Ticket
from src.infrastruction.db.models.ticket import TicketTypeModel, TicketModel


@dataclass(frozen=True, eq=False)
class BeanieTicketTypeRepository(TicketTypeRepository):
    async def add_ticket_type(self, ticket_type: TicketType) -> None:
        model = TicketTypeModel.from_entity(ticket_type)
        await model.create()

    async def check_exists_ticket_type_by_type_name(self, type_name: str) -> bool:
        query = TicketTypeModel.find_one({"type_name": type_name})
        return bool(await query)

    async def get_all_ticket_types(self, limit: int, offset: int) -> list[TicketType]:
        model_list = await TicketTypeModel.find_all(limit=limit, skip=offset).to_list()
        return [model.to_entity() for model in model_list]

    async def get_ticket_type_by_id(self, ticket_type_id: uuid.UUID) -> TicketType | None:
        model = await self._get_model_by_id(ticket_type_id=ticket_type_id)
        if model is not None:
            return model.to_entity()

    async def update_ticket_type(self, ticket_type: TicketType) -> None:
        model = await self._get_model_by_id(ticket_type_id=ticket_type.type_id)
        model.type_name = ticket_type.type_name.value

        await model.save()

    async def delete_ticket_type(self, ticket_type: TicketType) -> None:
        model = await self._get_model_by_id(ticket_type_id=ticket_type.type_id)
        await model.delete()

    @staticmethod
    async def _get_model_by_id(ticket_type_id: uuid.UUID) -> TicketTypeModel:
        return await TicketTypeModel.find_one({"type_id": ticket_type_id})


@dataclass(frozen=True, eq=False)
class BeanieTicketRepository(TicketRepository):
    async def add_ticket(self, ticket: Ticket) -> None:
        model = TicketModel.from_entity(ticket)
        await model.create()

    async def check_exist_customers_active_ticket(self, customer_id: uuid.UUID) -> bool:
        query = TicketModel.find_one(
            {
                "customer_id": customer_id,
                "is_active": True,
            },
        )
        return bool(await query)
