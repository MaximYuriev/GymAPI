import uuid
from dataclasses import dataclass

from src.application.interfaces.repositories.customer import CustomerRepository
from src.domain.entities.customer import Customer
from src.infrastruction.db.models.customer import CustomerModel


@dataclass(frozen=True, eq=False)
class BeanieCustomerRepository(CustomerRepository):
    async def add_customer(self, customer: Customer) -> None:
        model = CustomerModel.from_entity(customer)
        await model.create()

    async def check_phone_number_unique(self, phone_number: str) -> bool:
        model = await CustomerModel.find_one({"phone": phone_number})
        if model is None:
            return True
        return False

    async def get_customer_by_id(self, customer_id: uuid.UUID) -> Customer | None:
        model = await CustomerModel.find_one({"customer_id": customer_id})
        if model is not None:
            return model.to_entity()
