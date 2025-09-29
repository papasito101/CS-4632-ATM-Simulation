from __future__ import annotations
import random
from typing import Optional, Callable
from customer import Customer

class Poisson:
    """
    Generates arrivals according to a Poisson process (exponential interarrival times).
    Times are in minutes; rate is customers per hour.
    """
    def __init__(self, engine, rate_per_hour: float, on_arrival: Callable[[Customer], None], seed: Optional[int] = None):
        if rate_per_hour <= 0:
            raise ValueError("rate_per_hour must be > 0")
        self.engine = engine
        self.lambda_per_min = rate_per_hour / 60.0
        self.rng = random.Random(seed)
        self.on_arrival = on_arrival
        self.next_id = 1

    def start(self, until_minutes: float) -> None:
        # Schedule the first arrival immediately (or with an exponential delay)
        self._schedule_next_arrival(until_minutes)

    def _exp_delay(self) -> float:
        # Exponential with mean 1/lambda (minutes)
        return self.rng.expovariate(self.lambda_per_min)

    def _schedule_next_arrival(self, until_minutes: float) -> None:
        delay = self._exp_delay()
        def _arrival():
            t = self.engine.time
            cust = Customer(cid=self.next_id, arrival_time=t)
            self.next_id += 1
            self.on_arrival(cust)
            # Schedule the next one if we haven't passed horizon
            if self.engine.time < until_minutes:
                self._schedule_next_arrival(until_minutes)
        self.engine.schedule(delay, _arrival)
