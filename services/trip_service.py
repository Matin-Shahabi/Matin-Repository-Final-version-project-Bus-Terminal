from db.db import get_connection

class TripService:
    def list_available_trips(self):
        with get_connection() as cur:
            cur.execute("SELECT id, destination, cost, available_seats FROM trips WHERE is_started=FALSE")
            return cur.fetchall()