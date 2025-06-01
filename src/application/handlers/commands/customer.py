import datetime
from dataclasses import dataclass

from src.application.commands.customer import CreateCustomerCommand, BuyNewTicketCommand, GetAccessToTrainingCommand
from src.application.exceptions.customer import PhoneNumberNotUniqueException, CustomerNotFoundException, \
    CustomerAlreadyHasActiveTicketException
from src.application.exceptions.ticket import TicketTypeNotFoundException, TicketNotFoundException, \
    TicketIsNotActiveException, TicketActiveTimeExpireException, TicketNotEnoughWorkoutNumberException
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


@dataclass(frozen=True, eq=False)
class GetAccessToTrainingCommandHandler(BaseCommandHandler):
    _customer_repository: CustomerRepository
    _ticket_repository: TicketRepository

    async def handle(self, command: GetAccessToTrainingCommand) -> Ticket:
        customer = await self._customer_repository.get_customer_by_id(command.customer_id)
        if customer is None:
            raise CustomerNotFoundException(command.customer_id)

        ticket = await self._ticket_repository.get_ticket_by_id(command.ticket_id)
        if ticket is None:
            raise TicketNotFoundException(command.ticket_id)

        if not ticket.is_active:
            raise TicketIsNotActiveException(ticket.ticket_id)

        if ticket.expression_date < datetime.date.today():
            ticket.is_active = False
            await self._ticket_repository.update_ticket(ticket)
            raise TicketActiveTimeExpireException(ticket.expression_date)

        if ticket.workout_number.value == 0:
            ticket.is_active = False
            await self._ticket_repository.update_ticket(ticket)
            raise TicketNotEnoughWorkoutNumberException

        ticket.reduce_workout_number()
        await self._ticket_repository.update_ticket(ticket)

        customer.get_access_to_training(ticket=ticket)

        for event in customer.pull_event():
            await self._event_mediator.handle_event(event)

        return ticket
