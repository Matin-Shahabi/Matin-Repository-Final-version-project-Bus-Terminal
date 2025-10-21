class Trip:
    def __init__(self, id: int, destination: str, cost: float, start_time, end_time, capacity: int, available_seats: int, is_started: bool):
        self.id = id
        self.destination = destination
        self.cost = cost
        self.start_time = start_time
        self.end_time = end_time
        self.capacity = capacity
        self.available_seats = available_seats
        self.is_started = is_started