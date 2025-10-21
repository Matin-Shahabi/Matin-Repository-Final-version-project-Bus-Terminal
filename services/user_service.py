from db.db import get_connection
from services.transaction_service import TransactionService
from services.audit_service import AuditService

transaction_service = TransactionService()
audit_service = AuditService()

class UserService:
    def add_funds(self, user_id, amount):
        with get_connection() as cur:
            cur.execute("UPDATE users SET balance = balance + %s WHERE id=%s", (amount, user_id))
        type_ = 'TOPUP' if amount > 0 else 'DEDUCTION'
        transaction_service.add_transaction(user_id=user_id, ticket_id=None, amount=amount, type_=type_)
        audit_service.log(user_id, f"{'Added' if amount>0 else 'Deducted'} funds: {amount}")

    def get_balance(self, user_id):
        with get_connection() as cur:
            cur.execute("SELECT balance FROM users WHERE id=%s", (user_id,))
            balance = cur.fetchone()[0]
        return balance