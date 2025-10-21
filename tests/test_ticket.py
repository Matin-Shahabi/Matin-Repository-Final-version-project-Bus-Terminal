from services.ticket_service import TicketService
from services.user_service import UserService
from exceptions import InsufficientFundsError, TicketCancellationError

ticket_service = TicketService()
user_service = UserService()

def test_reserve_ticket():
    ticket_id = ticket_service.reserve_ticket(user_id=1, trip_id=1)
    assert ticket_id is not None

def test_pay_for_reserved_ticket():
    ticket_id = ticket_service.reserve_ticket(user_id=2, trip_id=2)
    ticket_service.pay_for_reserved_ticket(ticket_id, user_id=2)
    tickets = ticket_service.list_tickets_for_user(2)
    assert any(t[0] == ticket_id and t[3] == 'PAID' for t in tickets)

def test_buy_ticket_directly():
    ticket_id = ticket_service.buy_ticket(user_id=1, trip_id=1)
    tickets = ticket_service.list_tickets_for_user(1)
    assert any(t[0] == ticket_id and t[3] == 'PAID' for t in tickets)

def test_cancel_ticket_paid():
    ticket_id = ticket_service.buy_ticket(user_id=1, trip_id=1)
    refund = ticket_service.cancel_ticket(ticket_id, user_id=1)
    tickets = ticket_service.list_tickets_for_user(1)
    assert any(t[0] == ticket_id and t[3] == 'CANCELLED' for t in tickets)
    assert refund > 0

def test_cancel_ticket_reserved():
    ticket_id = ticket_service.reserve_ticket(user_id=2, trip_id=2)
    refund = ticket_service.cancel_ticket(ticket_id, user_id=2)
    tickets = ticket_service.list_tickets_for_user(2)
    assert any(t[0] == ticket_id and t[3] == 'CANCELLED' for t in tickets)
    assert refund == 0