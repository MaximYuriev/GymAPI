from dataclasses import dataclass

from src.application.commands.customer import CreateCustomerCommand
from src.application.exceptions.customer import PhoneNumberNotUniqueException
from src.application.handlers.commands.base import BaseCommandHandler
from src.application.interfaces.repositories.customer import CustomerRepository
from src.domain.entities.customer import Customer
from src.domain.values.name import Name, Surname, Patronymic
from src.domain.values.phone import PhoneNumber


@dataclass(frozen=True, eq=False)
class CreateCustomerCommandHandler(BaseCommandHandler):
    _customer_repository: CustomerRepository

    async def handle(self, command: CreateCustomerCommand) -> Customer:
        name = Name(command.name)
        surname = Surname(command.surname)
        patronymic = Patronymic(command.patronymic)
        phone = PhoneNumber(command.phone)

        if not (await self._customer_repository.check_phone_number_unique(phone.value)):
            raise PhoneNumberNotUniqueException(phone.value)

        customer = Customer(
            name=name,
            surname=surname,
            patronymic=patronymic,
            phone=phone,
        )
        await self._customer_repository.add_customer(customer)

        return customer
