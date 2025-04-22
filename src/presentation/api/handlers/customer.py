from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from src.application.commands.customer import CreateCustomerCommand
from src.application.mediator.mediator import Mediator
from src.domain.entities.customer import Customer
from src.presentation.api.commons.response import APIResponse
from src.presentation.api.schemas.customer import CustomerSchema, CreateCustomerSchema

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
