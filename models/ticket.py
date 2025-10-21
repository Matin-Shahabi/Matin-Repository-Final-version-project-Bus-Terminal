from constants import TICKET_STATUS_PAID, TICKET_STATUS_CANCELLED

class Ticket:
    def __init__(self, id: int, user_id: int, trip_id: int, seat_number: int, status: str, purchase_time):
        self.id = id
        self.user_id = user_id
        self.trip_id = trip_id
        self.seat_number = seat_number
        self.status = status
        self.purchase_time = purchase_time