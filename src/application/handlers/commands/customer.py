from dataclasses import dataclass

from src.application.commands.customer import CreateCustomerCommand, BuyNewTicketCommand
from src.application.exceptions.customer import PhoneNumberNotUniqueException, CustomerNotFoundException, \
    CustomerAlreadyHasActiveTicketException
from src.application.exceptions.ticket import TicketTypeNotFoundException
from src.application.handlers.commands.base import BaseCommandHandler
from src.application.interfaces.repositories.customer import CustomerRepository
from src.application.interfaces.repositories.ticket import TicketTypeRepository, TicketRepository
from src.domain.entities.customer import Customer
from src.domain.entities.ticket import Ticket
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

        customer = Customer.create_customer(
            name=name,
            surname=surname,
            patronymic=patronymic,
            phone=phone,
        )
        await self._customer_repository.add_customer(customer)

        for event in customer.pull_event():
            await self._event_mediator.handle_event(event)

        return customer


@dataclass(frozen=True, eq=False)
class BuyNewTicketCommandHandler(BaseCommandHandler):
    _customer_repository: CustomerRepository
    _ticket_type_repository: TicketTypeRepository
    _ticket_repository: TicketRepository

    async def handle(self, command: BuyNewTicketCommand) -> Ticket:
        customer = await self._customer_repository.get_customer_by_id(customer_id=command.customer_id)
        if customer is None:
            raise CustomerNotFoundException(command.customer_id)

        if await self._ticket_repository.check_exist_customers_active_ticket(customer_id=customer.customer_id):
            raise CustomerAlreadyHasActiveTicketException

        ticket_type = await self._ticket_type_repository.get_ticket_type_by_id(command.ticket_type_id)
        if ticket_type is None:
            raise TicketTypeNotFoundException(command.ticket_type_id)

        ticket = customer.buy_new_ticket(ticket_type=ticket_type)
        await self._ticket_repository.add_ticket(ticket)

        for event in customer.pull_event():
            await self._event_mediator.handle_event(event)

        return ticket
