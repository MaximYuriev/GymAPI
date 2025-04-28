import uuid

from beanie import Document

from src.domain.entities.customer import Customer
from src.domain.values.name import Name, Surname, Patronymic
from src.domain.values.phone import PhoneNumber


class CustomerModel(Document):
    customer_id: uuid.UUID
    name: str
    surname: str
    patronymic: str | None
    phone: str

    @classmethod
    def from_entity(cls, customer: Customer) -> 'CustomerModel':
        return cls(
            customer_id=customer.customer_id,
            name=customer.name.value,
            surname=customer.surname.value,
            patronymic=customer.patronymic.value,
            phone=customer.phone.value,
        )

    def to_entity(self) -> Customer:
        return Customer(
            customer_id=self.customer_id,
            name=Name(self.name),
            surname=Surname(self.surname),
            patronymic=Patronymic(self.patronymic),
            phone=PhoneNumber(self.phone),
        )

    class Settings:
        name = "customer"
