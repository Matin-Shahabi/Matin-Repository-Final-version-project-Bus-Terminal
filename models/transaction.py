class Transaction:
    def __init__(self, id: int, user_id: int, ticket_id: int, amount: float, type: str, created_at):
        self.id = id
        self.user_id = user_id
        self.ticket_id = ticket_id
        self.amount = amount
        self._type = type
        self.created_at = created_at