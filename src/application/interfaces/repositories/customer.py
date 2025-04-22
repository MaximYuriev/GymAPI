from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.entities.customer import Customer


@dataclass(frozen=True, eq=False)
class CustomerRepository(ABC):
    @abstractmethod
    async def add_customer(self, customer: Customer) -> None:
        pass

    @abstractmethod
    async def check_phone_number_unique(self, phone_number: str) -> bool:
        pass
