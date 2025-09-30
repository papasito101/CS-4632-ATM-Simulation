from __future__ import print_function
import argparse
import heapq
import math
import random
from itertools import count

from customer import Customer
from queue_system import QueueSystem
from metrics import Metrics

class Event(object):
    __slots__ = ("time", "etype", "payload")

    def __init__(self, time, etype, payload=None):
        self.time = float(time)
        self.etype = etype  # 'arrival' (service later)
        self.payload = payload

    def __lt__(self, other):
        return self.time < other.time

class SimulationEngine(object):
    def __init__(self, rate_per_hour=12.0, duration_hours=1.0, seed=None):
        self.now = 0.0
        self.end_time = float(duration_hours)
        self.rng = random.Random(seed)
        self.rate = float(rate_per_hour)  # lambda (per hour)
        self.events = []
        self.queue = QueueSystem()
        self.metrics = Metrics()
        self._cid_seq = count(1)

    # ---- Poisson process helpers ----
    def _expovariate_hours(self, rate):
        # Exponential with mean 1/rate (hours)
        # random.Random.expovariate expects rate per unit; unit is hours here.
        u = self.rng.random()
        while u <= 1e-12:
            u = self.rng.random()
        return -math.log(u) / rate

    def schedule(self, ev):
        heapq.heappush(self.events, (ev.time, ev))

    def log(self, msg):
        # Print time in hours with 2 decimals (00.01h)
        print("[{:.02f}h] {}".format(self.now, msg))

    def initialize(self):
        self.queue.sample_len(0.0)
        # Schedule first arrival at t ~ Exp(lambda)
        if self.rate > 0.0:
            t = self._expovariate_hours(self.rate)
            self.schedule(Event(t, 'arrival', None))

    def handle_arrival(self):
        cid = next(self._cid_seq)
        cust = Customer("c{:03d}".format(cid), self.now)
        self.metrics.inc_arrivals()
        # Enqueue customer (service logic will be added in Day 3–4)
        self.queue.enqueue(cust)
        self.log("ARRIVAL {} -> queue_len={}".format(cust.cid, len(self.queue)))
        self.queue.sample_len(self.now)

        # Schedule next arrival (if within horizon)
        if self.rate > 0.0:
            next_t = self.now + self._expovariate_hours(self.rate)
            if next_t <= self.end_time:
                self.schedule(Event(next_t, 'arrival', None))

    def run(self):
        self.initialize()
        while self.events:
            t, ev = heapq.heappop(self.events)
            if t > self.end_time:
                break
            self.now = t
            if ev.etype == 'arrival':
                self.handle_arrival()
            else:
                self.log("UNKNOWN EVENT {}".format(ev.etype))
        # Final queue sample at end to compute average properly
        self.queue.sample_len(self.end_time)
        avg_q = self.queue.average_len(self.end_time)
        print("[END] time={:.02f}h, arrivals={}, avg_queue_len={:.2f}".format(
            self.end_time, self.metrics.arrivals, avg_q))

def main():
    p = argparse.ArgumentParser(description="ATM Simulation (Day 1–2 Poisson arrivals only)")
    p.add_argument("--rate", type=float, default=12.0, help="arrival rate (customers per hour)")
    p.add_argument("--duration", type=float, default=1.0, help="simulation duration (hours)")
    p.add_argument("--seed", type=int, default=None, help="random seed")
    args = p.parse_args()

    sim = SimulationEngine(rate_per_hour=args.rate, duration_hours=args.duration, seed=args.seed)
    sim.run()

if __name__ == "__main__":
    main()
