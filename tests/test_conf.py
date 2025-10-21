import pytest
from db.db import get_connection

@pytest.fixture(autouse=True)
def setup_db():
    """پاکسازی و بارگذاری دیتای تست قبل از هر تست"""
    with get_connection() as cur:
        # پاکسازی جداول به ترتیب وابستگی
        cur.execute("DELETE FROM transactions")
        cur.execute("DELETE FROM tickets")
        cur.execute("DELETE FROM trips")
        cur.execute("DELETE FROM users")
        cur.execute("DELETE FROM audit_logs")
        cur.execute("DELETE FROM locks")

        # بارگذاری کاربران تست
        cur.execute("INSERT INTO users (id, username, password, balance) VALUES (1, 'alice', 'pass123', 500)")
        cur.execute("INSERT INTO users (id, username, password, balance) VALUES (2, 'bob', 'pass123', 300)")
        cur.execute("INSERT INTO users (id, username, password, balance) VALUES (3, 'admin', 'admin123', 0)")

        # بارگذاری سفرهای تست
        cur.execute("INSERT INTO trips (id, destination, cost, start_time, end_time, capacity, available_seats) "
                    "VALUES (1, 'Tehran', 100, NOW(), NOW() + INTERVAL '3 hour', 10, 10)")
        cur.execute("INSERT INTO trips (id, destination, cost, start_time, end_time, capacity, available_seats) "
                    "VALUES (2, 'Mashhad', 150, NOW() + INTERVAL '1 day', NOW() + INTERVAL '1 day 4 hour', 15, 15)")