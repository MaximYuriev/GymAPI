import uuid

from sqlalchemy.orm import Mapped, mapped_column

from src.domain.entities.customer import Customer
from src.domain.values.name import Name, Surname, Patronymic
from src.domain.values.phone import PhoneNumber
from src.infrastruction.db.models.base import Base


class CustomerModel(Base):
    __tablename__ = "customer"
    customer_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(unique=True)

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
