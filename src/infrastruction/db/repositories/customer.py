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
        query = select(CustomerModel).where(CustomerModel.phone == phone_number)
        model = await self._session.scalar(query)
        if model is None:
            return True
        return False
