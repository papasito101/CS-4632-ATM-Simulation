from dataclasses import dataclass

@dataclass
class Customer:
    id: int
    time_of_arrival: float  # the time the customer arrived
