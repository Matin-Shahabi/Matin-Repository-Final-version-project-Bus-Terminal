from db.db import get_connection
from datetime import datetime

class AuditService:
    def log(self, actor: str, action: str):
        timestamp = datetime.now()
        with get_connection() as cur:
            cur.execute("""
                INSERT INTO audit_logs(actor, action, timestamp)
                VALUES (%s, %s, %s)
            """, (actor, action, timestamp))