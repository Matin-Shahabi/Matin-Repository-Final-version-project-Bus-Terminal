from db.db import get_connection
from exceptions import AuthenticationError
import os
from models.user import User

SUPERUSER = os.getenv("SUPERUSER", "admin")
SUPERPASS = os.getenv("SUPERPASS", "admin123")

class AuthService:
    def register(self, username, password):
        with get_connection() as cur:
            cur.execute("SELECT id FROM users WHERE username=%s", (username,))
            if cur.fetchone():
                raise AuthenticationError("Username already exists")
            cur.execute("INSERT INTO users(username, password, balance) VALUES(%s,%s,%s)", (username, password, 0))

    def login(self, username, password):
        if username == SUPERUSER and password == SUPERPASS:
            return type('SuperUser', (), {'username': SUPERUSER})
        with get_connection() as cur:
            cur.execute("SELECT id, username, password, balance FROM users WHERE username=%s AND password=%s", (username, password))
            row = cur.fetchone()
            if not row:
                raise AuthenticationError("Invalid username or password")
            return User(*row)