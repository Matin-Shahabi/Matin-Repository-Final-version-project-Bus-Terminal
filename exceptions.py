class InsufficientBalanceError(Exception):
    def _init_(self, balance, cost):
        self.balance = balance
        self.cost = cost
        super().__init__(f" Insufficient balance (Your balance: {balance}, Trip cost: {cost})")

class AuthenticationError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass

class SeatUnavailableError(Exception):
    pass

class TicketCancellationError(Exception):
    pass

class TransactionError(Exception):
    pass