from db.db import get_connection
from services.audit_service import AuditService

audit_service = AuditService()

class AdminService:
    def total_income(self):
        with get_connection() as cur:
            cur.execute("SELECT SUM(amount) FROM transactions")
            income = cur.fetchone()[0] or 0
            print(f" Total income: {income:.2f}")

    def trip_income(self, trip_id):
        with get_connection() as cur:
            cur.execute("""
                SELECT SUM(t.amount)
                FROM transactions t
                JOIN tickets tk ON t.ticket_id = tk.id
                WHERE tk.trip_id=%s
            """, (trip_id,))
            income = cur.fetchone()[0] or 0
            print(f" Trip {trip_id} income: {income:.2f}")

    def stats(self):
        with get_connection() as cur:
            cur.execute("SELECT COUNT(*) FROM trips")
            trips_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM tickets")
            tickets_count = cur.fetchone()[0]
            print(f" Trips: {trips_count}, Tickets sold: {tickets_count}")

    def report_transactions(self):
        with get_connection() as cur:
            cur.execute("""
                SELECT t.id, u.username, t.type, t.amount, t.ticket_id, tr.destination, t.created_at
                FROM transactions t
                LEFT JOIN tickets tk ON t.ticket_id = tk.id
                LEFT JOIN trips tr ON tk.trip_id = tr.id
                LEFT JOIN users u ON t.user_id = u.id
                ORDER BY t.created_at DESC
            """)
            rows = cur.fetchall()

        if not rows:
            print("No transactions found.")
            return

        print("="*80)
        print(f"{'ID':<4} | {'User':<15} | {'Type':<10} | {'Amount':<8} | {'TicketID':<8} | {'Destination':<15} | {'Date'}")
        print("-"*80)
        total_income = 0
        for r in rows:
            tid, username, ttype, amount, ticket_id, destination, created_at = r
            # تبدیل مقادیر None و datetime به رشته
            username = username or "-"
            ticket_id = ticket_id or "-"
            destination = destination or "-"
            created_at = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else "-"
            print(f"{tid:<4} | {username:<15} | {ttype:<10} | {amount:<8.2f} | {ticket_id:<8} | {destination:<15} | {created_at}")
            if ttype == 'PURCHASE':
                total_income += amount
            elif ttype == 'REFUND':
                total_income -= amount
        print("-"*80)
        print(f" Total Income: {total_income:.2f}")
        print("="*80)