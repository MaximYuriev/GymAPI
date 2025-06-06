import uuid

from pydantic import BaseModel

from src.domain.entities.customer import Customer


class CustomerSchema(BaseModel):
    costumer_id: uuid.UUID
    name: str
    surname: str
    patronymic: str | None
    phone: str

    @classmethod
    def from_entity(cls, customer: Customer) -> 'CustomerSchema':
        return cls(
            costumer_id=customer.customer_id,
            name=customer.name.value,
            surname=customer.surname.value,
            patronymic=customer.patronymic.value,
            phone=customer.phone.value,
        )


class CreateCustomerSchema(BaseModel):
    name: str
    surname: str
    patronymic: str | None = None
    phone: str
