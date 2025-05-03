import uuid
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query

from src.application.commands.customer import CreateCustomerCommand, BuyNewTicketCommand, GetAccessToTrainingCommand
from src.application.mediator.mediator import Mediator
from src.application.queries.customer import GetAllCustomerTicketQuery, GetActiveCustomerTicketQuery
from src.domain.entities.customer import Customer
from src.domain.entities.ticket import Ticket
from src.presentation.api.commons.pagination import PaginationQueryParams
from src.presentation.api.commons.response import APIResponse
from src.presentation.api.schemas.customer import CustomerSchema, CreateCustomerSchema
from src.presentation.api.schemas.ticket import TicketSchema, BuyTicketSchema

customer_router = APIRouter(prefix="/customer", tags=["Customer"])


@customer_router.post("/")
@inject
async def create_customer_handler(
        schema: CreateCustomerSchema,
        mediator: FromDishka[Mediator],
) -> APIResponse[CustomerSchema]:
    command = CreateCustomerCommand(
        name=schema.name,
        surname=schema.surname,
        patronymic=schema.patronymic,
        phone=schema.phone,
    )
    customer: Customer = await mediator.handle_command(command)

    return APIResponse(
        detail="Клиент добавлен в систему!",
        data=CustomerSchema.from_entity(customer)
    )


@customer_router.post("/{customer_id}/ticket/")
@inject
async def buy_new_ticket_handler(
        customer_id: uuid.UUID,
        schema: BuyTicketSchema,
        mediator: FromDishka[Mediator],
) -> APIResponse[TicketSchema]:
    command = BuyNewTicketCommand(
        customer_id=customer_id,
        ticket_type_id=schema.ticket_type_id,
    )
    ticket: Ticket = await mediator.handle_command(command)

    return APIResponse(
        detail="Новый абонемент успешно куплен!",
        data=TicketSchema.from_entity(ticket)
    )


@customer_router.get("/{customer_id}/ticket/")
@inject
async def get_all_customer_ticket_list_handler(
        customer_id: uuid.UUID,
        pagination_params: Annotated[PaginationQueryParams, Query()],
        mediator: FromDishka[Mediator],
) -> APIResponse[TicketSchema]:
    query = GetAllCustomerTicketQuery(
        customer_id=customer_id,
        limit=pagination_params.limit,
        offset=pagination_params.offset,
    )
    ticket_list: list[Ticket] = await mediator.handle_query(query)

    return APIResponse(
        detail="Список абонементов клиента:",
        data=[TicketSchema.from_entity(ticket) for ticket in ticket_list]
    )


@customer_router.get("/{customer_id}/ticket/active/")
@inject
async def get_active_customer_ticket_handler(
        customer_id: uuid.UUID,
        mediator: FromDishka[Mediator],
) -> APIResponse[TicketSchema]:
    query = GetActiveCustomerTicketQuery(
        customer_id=customer_id,
    )
    active_ticket: Ticket = await mediator.handle_query(query)

    return APIResponse(
        detail="Активный абонемент найден!",
        data=TicketSchema.from_entity(active_ticket),
    )


@customer_router.get("/{customer_id}/ticket/{ticket_id}/")
@inject
async def get_access_to_training_handler(
        customer_id: uuid.UUID,
        ticket_id: uuid.UUID,
        mediator: FromDishka[Mediator],
) -> APIResponse[TicketSchema]:
    command = GetAccessToTrainingCommand(
        customer_id=customer_id,
        ticket_id=ticket_id,
    )
    ticket: Ticket = await mediator.handle_command(command)

    return APIResponse(
        detail="Доступ к тренировке успешно получен!",
        data=TicketSchema.from_entity(ticket),
    )
