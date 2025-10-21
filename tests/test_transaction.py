from services.transaction_service import TransactionService
from services.ticket_service import TicketService
from services.user_service import UserService
from db.db import get_connection

transaction_service = TransactionService()
ticket_service = TicketService()
user_service = UserService()

def test_topup_transaction():
    user_id = 1
    old_balance = user_service.get_balance(user_id)
    user_service.add_funds(user_id, 100)
    new_balance = user_service.get_balance(user_id)
    assert new_balance == old_balance + 100

def test_purchase_and_refund_transaction():
    user_id = 1
    trip_id = 1
    # خرید بلیت
    ticket_id = ticket_service.buy_ticket(user_id, trip_id)
    # بررسی تراکنش خرید
    with get_connection() as cur:
        cur.execute("SELECT type, amount FROM transactions WHERE ticket_id=%s", (ticket_id,))
        rows = cur.fetchall()
        assert any(r[0] == 'PURCHASE' for r in rows)
    # لغو بلیت
    refund = ticket_service.cancel_ticket(ticket_id, user_id)
    # بررسی تراکنش بازگشت وجه
    with get_connection() as cur:
        cur.execute("SELECT type, amount FROM transactions WHERE ticket_id=%s AND type='REFUND'", (ticket_id,))
        rows = cur.fetchall()
        assert rows[0][1] == refund