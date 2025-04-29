import uuid
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query

from src.application.commands.ticket import CreateTicketTypeCommand, UpdateTicketTypeCommand, DeleteTicketTypeCommand
from src.application.mediator.mediator import Mediator
from src.application.queries.ticket import GetAllTicketTypesQuery, GetTicketTypeQuery
from src.domain.entities.ticket import TicketType
from src.presentation.api.commons.pagination import PaginationQueryParams
from src.presentation.api.commons.response import APIResponse
from src.presentation.api.schemas.ticket import CreateTicketTypeSchema, TicketTypeSchema, UpdateTicketTypeSchema

ticket_router = APIRouter(prefix="/ticket", tags=["Ticket"])


@ticket_router.post("/type/")
@inject
async def create_ticket_type_handler(
        create_ticket_type_schema: CreateTicketTypeSchema,
        mediator: FromDishka[Mediator]
) -> APIResponse[TicketTypeSchema]:
    command = CreateTicketTypeCommand(
        type_name=create_ticket_type_schema.type_name,
        workout_number=create_ticket_type_schema.workout_number,
        duration=create_ticket_type_schema.duration,
    )

    ticket_type: TicketType = await mediator.handle_command(command)

    return APIResponse(
        detail="Тип абонемента успешно добавлен!",
        data=TicketTypeSchema.from_entity(ticket_type),
    )


@ticket_router.get("/type/")
@inject
async def get_all_ticket_types_handler(
        pagination_params: Annotated[PaginationQueryParams, Query()],
        mediator: FromDishka[Mediator],
) -> APIResponse[list[TicketTypeSchema]]:
    query = GetAllTicketTypesQuery(
        limit=pagination_params.limit,
        offset=pagination_params.offset,
    )

    list_ticket_type: list[TicketType] = await mediator.handle_query(query)

    return APIResponse(
        detail="Найденные типы абонемента",
        data=[TicketTypeSchema.from_entity(ticket_type) for ticket_type in list_ticket_type],
    )


@ticket_router.get("/type/{type_id}/")
@inject
async def get_ticket_type_by_id(
        type_id: uuid.UUID,
        mediator: FromDishka[Mediator],
) -> APIResponse[TicketTypeSchema]:
    query = GetTicketTypeQuery(
        ticket_type_id=type_id,
    )
    ticket_type: TicketType = await mediator.handle_query(query)

    return APIResponse(
        detail="Тип абонемента найден!",
        data=TicketTypeSchema.from_entity(ticket_type),
    )


@ticket_router.patch("/type/{type_id}/")
@inject
async def update_type_name_handler(
        type_id: uuid.UUID,
        schema: UpdateTicketTypeSchema,
        mediator: FromDishka[Mediator],
) -> APIResponse[TicketTypeSchema]:
    command = UpdateTicketTypeCommand(
        ticket_type_id=type_id,
        type_name=schema.type_name,
    )
    ticket_type: TicketType = await mediator.handle_command(command)

    return APIResponse(
        detail="Тип абонемента был успешно обновлен!",
        data=TicketTypeSchema.from_entity(ticket_type),
    )


@ticket_router.delete("/type/{type_id}/")
@inject
async def delete_ticket_type_by_id_handler(
        type_id: uuid.UUID,
        mediator: FromDishka[Mediator],
) -> APIResponse[TicketTypeSchema]:
    command = DeleteTicketTypeCommand(
        ticket_type_id=type_id,
    )
    ticket_type: TicketType = await mediator.handle_command(command)

    return APIResponse(
        detail="Тип абонемента успешно удален!",
        data=TicketTypeSchema.from_entity(ticket_type),
    )
