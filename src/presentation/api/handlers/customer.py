import uuid

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from src.application.commands.customer import CreateCustomerCommand, BuyNewTicketCommand
from src.application.mediator.mediator import Mediator
from src.domain.entities.customer import Customer
from src.domain.entities.ticket import Ticket
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
