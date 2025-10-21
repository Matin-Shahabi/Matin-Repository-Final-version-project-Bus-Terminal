from db.db import get_connection
from exceptions import InsufficientFundsError, TicketCancellationError, SeatUnavailableError
from datetime import datetime
from services.transaction_service import TransactionService
from services.user_service import UserService
from services.audit_service import AuditService

transaction_service = TransactionService()
user_service = UserService()
audit_service = AuditService()

class TicketService:
    def reserve_ticket(self, user_id, trip_id):
        with get_connection() as cur:
            cur.execute("SELECT available_seats, is_started FROM trips WHERE id=%s", (trip_id,))
            trip = cur.fetchone()
            if not trip:
                raise Exception("Trip not found")
            available_seats, is_started = trip
            if is_started:
                raise Exception("Trip has already started")
            if available_seats <= 0:
                raise SeatUnavailableError("No available seats")
            # Assign seat
            seat_number = trip[0] - available_seats + 1
            cur.execute("""
                INSERT INTO tickets(user_id, trip_id, seat_number, status)
                VALUES (%s,%s,%s,'RESERVED') RETURNING id
            """, (user_id, trip_id, seat_number))
            ticket_id = cur.fetchone()[0]
            cur.execute("UPDATE trips SET available_seats=available_seats-1 WHERE id=%s", (trip_id,))
            # Audit log
            audit_service.log(user_id, f"Reserved ticket {ticket_id} for trip {trip_id}")
        return ticket_id

    def pay_for_reserved_ticket(self, ticket_id, user_id):
        with get_connection() as cur:
            cur.execute("SELECT trip_id, status FROM tickets WHERE id=%s AND user_id=%s", (ticket_id, user_id))
            row = cur.fetchone()
            if not row:
                raise Exception("Ticket not found")
            trip_id, status = row
            if status != 'RESERVED':
                raise Exception("Ticket is not reserved or already paid")
            # بررسی موجودی
            cur.execute("SELECT cost FROM trips WHERE id=%s", (trip_id,))
            cost = cur.fetchone()[0]
            balance = user_service.get_balance(user_id)
            if balance < cost:
                raise InsufficientFundsError("Not enough balance")
            user_service.add_funds(user_id, -cost)
            cur.execute("UPDATE tickets SET status='PAID', purchase_time=NOW() WHERE id=%s", (ticket_id,))
            transaction_service.add_transaction(user_id, ticket_id, cost, 'PURCHASE')
            audit_service.log(user_id, f"Paid for reserved ticket {ticket_id} (Trip {trip_id})")
        return True

    def buy_ticket(self, user_id, trip_id):
        ticket_id = self.reserve_ticket(user_id, trip_id)
        self.pay_for_reserved_ticket(ticket_id, user_id)
        return ticket_id

    def list_tickets_for_user(self, user_id):
        with get_connection() as cur:
            cur.execute("""
                SELECT t.id, tr.destination, t.seat_number, t.status
                FROM tickets t
                JOIN trips tr ON t.trip_id = tr.id
                WHERE t.user_id=%s
            """, (user_id,))
            rows = cur.fetchall()
        return rows

    def cancel_ticket(self, ticket_id, user_id):
        with get_connection() as cur:
            cur.execute("SELECT trip_id, status FROM tickets WHERE id=%s AND user_id=%s", (ticket_id, user_id))
            row = cur.fetchone()
            if not row:
                raise TicketCancellationError("Ticket not found")
            trip_id, status = row
            if status not in ['PAID', 'RESERVED']:
                raise TicketCancellationError("Cannot cancel this ticket")
            refund = 0
            if status == 'PAID':
                cur.execute("SELECT cost FROM trips WHERE id=%s", (trip_id,))
                cost = cur.fetchone()[0]
                refund = float(cost) * 0.85
                user_service.add_funds(user_id, refund)
                transaction_service.add_transaction(user_id, ticket_id, refund, 'REFUND')
            cur.execute("UPDATE tickets SET status='CANCELLED' WHERE id=%s", (ticket_id,))
            cur.execute("UPDATE trips SET available_seats=available_seats+1 WHERE id=%s", (trip_id,))
            audit_service.log(user_id, f"Cancelled ticket {ticket_id} for trip {trip_id}, refund: {refund}")
        return refund