import uuid
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.repositories.customer import CustomerRepository
from src.domain.entities.customer import Customer
from src.infrastruction.db.models.customer import CustomerModel


@dataclass(frozen=True, eq=False)
class SQLAlchemyCustomerRepository(CustomerRepository):
    _session: AsyncSession

    async def add_customer(self, customer: Customer) -> None:
        model = CustomerModel.from_entity(customer)
        self._session.add(model)
        await self._session.commit()

    async def check_phone_number_unique(self, phone_number: str) -> bool:
        model = await self._get_customer_model(phone=phone_number)
        if model is None:
            return True
        return False

    async def get_customer_by_id(self, customer_id: uuid.UUID) -> Customer | None:
        model = await self._get_customer_model(customer_id=customer_id)
        if model is not None:
            return model.to_entity()

    async def _get_customer_model(self, **kwargs) -> CustomerModel | None:
        query = select(CustomerModel).filter_by(**kwargs)
        return await self._session.scalar(query)
