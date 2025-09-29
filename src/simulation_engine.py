import argparse
import heapq
import math
import random
from dataclasses import dataclass
from typing import List, Tuple, Optional

# ----- Events -----

ARRIVAL = "ARRIVAL"

@dataclass(order=True)
class Event:
    time: float
    type: str
    payload: dict

# ----- Entities -----

@dataclass
class Customer:
    id: int
    arrival_time: float  # minutes

# ----- Engine -----

class SimulationEngine:
    def __init__(self, duration_minutes: int, arrival_rate_per_hour: float, seed: Optional[int] = None):
        self.T_end = float(duration_minutes)
        self.lambda_per_min = float(arrival_rate_per_hour) / 60.0
        if self.lambda_per_min <= 0:
            raise ValueError("arrival_rate_per_hour must be > 0")
        self.rng = random.Random(seed)
        self.clock = 0.0
        self.event_q: List[Event] = []
        self.next_customer_id = 1
        self.queue: List[Customer] = []
        self.arrivals = 0

    # Exponential inter-arrival using stdlib random
    def expovariate(self, rate_per_min: float) -> float:
        u = self.rng.random()
        return -math.log(1.0 - u) / rate_per_min

    def schedule(self, evt: Event):
        heapq.heappush(self.event_q, evt)

    def schedule_first_arrival(self):
        t = self.expovariate(self.lambda_per_min)
        self.schedule(Event(time=t, type=ARRIVAL, payload={}))

    def handle_arrival(self, evt: Event):
        self.clock = evt.time
        cust = Customer(id=self.next_customer_id, arrival_time=self.clock)
        self.next_customer_id += 1
        self.queue.append(cust)
        self.arrivals += 1
        print(f"{self.clock:06.2f}  {ARRIVAL:<7} customer_id={cust.id}  queue_len={len(self.queue)}")

        # schedule next arrival if within horizon
        ia = self.expovariate(self.lambda_per_min)
        next_t = self.clock + ia
        if next_t <= self.T_end:
            self.schedule(Event(time=next_t, type=ARRIVAL, payload={}))

    def run(self):
        self.schedule_first_arrival()
        while self.event_q:
            evt = heapq.heappop(self.event_q)
            if evt.time > self.T_end:
                break
            if evt.type == ARRIVAL:
                self.handle_arrival(evt)
            else:
                # future event types go here
                pass

        print("-- SUMMARY --")
        print(f"sim_time_minutes={self.T_end:.2f}  arrivals={self.arrivals}  final_queue_len={len(self.queue)}")


def main():
    parser = argparse.ArgumentParser(description="ATM Simulation (Day 1–2): Poisson arrivals only.")
    parser.add_argument("--duration-minutes", type=int, default=120, help="Total simulation horizon in minutes.")
    parser.add_argument("--arrival-rate-per-hour", type=float, default=12.0, help="Average customers per hour.")
    parser.add_argument("--seed", type=int, default=None, help="RNG seed for reproducibility.")
    args = parser.parse_args()

    sim = SimulationEngine(duration_minutes=args.duration_minutes,
                           arrival_rate_per_hour=args.arrival_rate_per_hour,
                           seed=args.seed)
    sim.run()

if __name__ == "__main__":
    main()
