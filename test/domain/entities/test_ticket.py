import datetime

from src.domain.entities.ticket import TicketType, Ticket


def test_create_ticket_success(ticket_type: TicketType):
    ticket = Ticket.create_ticket(ticket_type)

    assert ticket.ticket_type == ticket_type
    assert ticket.workout_number == ticket_type.workout_number
    assert ticket.expression_date == datetime.date.today() + ticket.ticket_type.duration
