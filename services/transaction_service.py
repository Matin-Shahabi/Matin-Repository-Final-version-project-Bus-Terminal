from db.db import get_connection

class TransactionService:
    def add_transaction(self, user_id, ticket_id, amount, type_):
        with get_connection() as cur:
            cur.execute("""
                INSERT INTO transactions(user_id, ticket_id, amount, type, created_at)
                VALUES(%s,%s,%s,%s,NOW())
            """, (user_id, ticket_id, amount, type_))