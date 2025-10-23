from __future__ import print_function
import argparse, heapq, math, random
from itertools import count
from .customer import Customer
from .queue_system import QueueSystem
from .metrics import Metrics
from .atm import ATM

class Event(object):
    __slots__ = ("time", "etype", "payload")
    def __init__(self, time, etype, payload=None):
        self.time = float(time); self.etype = etype; self.payload = payload
    def __lt__(self, other): return self.time < other.time


class SimulationEngine(object):
    def __init__(
        self,
        rate_per_hour=12.0,
        duration_hours=1.0,
        seed=None,
        n_atms=2,
        svc_mean_min=3.0,
        svc_cv=0.6,
        max_queue=12,
        logger=None,
        timeseries_dt_min=0.5,
    ):
        self.now = 0.0
        self.end_time = float(duration_hours)
        self.rng = random.Random(seed)
        self.rate = float(rate_per_hour)
        self.events = []
        self._seq = count(0)
        self.queue = QueueSystem()
        self.metrics = Metrics()
        self._cid_seq = count(1)
        self.atms = [ATM(i + 1) for i in range(int(n_atms))]

        cv = max(0.0001, float(svc_cv))
        sigma2 = math.log(1.0 + cv * cv)
        self.sigma = math.sqrt(sigma2)
        self.mu = math.log(max(1e-9, float(svc_mean_min))) - 0.5 * sigma2

        self.max_queue = int(max_queue) if max_queue is not None else None

        self.logger = logger
        self._ts_dt_h = float(timeseries_dt_min) / 60.0
        self._next_ts = 0.0  # next sim-time (hours) to sample in timeseries

        self._summary = {}

    def _expovariate_hours(self, rate):
        u = self.rng.random()
        while u <= 1e-12:
            u = self.rng.random()
        return -math.log(u) / rate

    def _lognormal_minutes(self):
        return self.rng.lognormvariate(self.mu, self.sigma)

    def schedule(self, ev):
        heapq.heappush(self.events, (ev.time, next(self._seq), ev))

    def log(self, msg):
        print("[{:.02f}h] {}".format(self.now, msg))
        if self.logger is not None:
            self.logger.log_event(self.now, "LOG", message=msg, queue_len=len(self.queue))

    def initialize(self):
        self.queue.sample_len(0.0)

        if self.logger is not None:
            self.logger.log_timeslice(
                0.0,
                len(self.queue),
                0,                           # in_service
                self.metrics.completed,
                self.metrics.balked,
                0,                           # reneged (not implemented yet)
                [int(a.is_busy) for a in self.atms],
            )

        if self.rate > 0.0:
            t = self._expovariate_hours(self.rate)
            self.schedule(Event(t, "arrival", None))

    def _find_free_atm(self):
        for atm in self.atms:
            if not atm.is_busy:
                return atm
        return None

    def _try_start_service(self):
        while len(self.queue) > 0:
            atm = self._find_free_atm()
            if atm is None:
                break
            cust = self.queue.dequeue()
            wait_h = max(0.0, self.now - cust.arrival_time)
            svc_min = self._lognormal_minutes()
            svc_h = svc_min / 60.0
            end_t = self.now + svc_h
            atm.is_busy = True
            atm.busy_time += svc_h
            self.metrics.inc_started()
            self.metrics.wait_times.append(wait_h)

            self.log(
                "START   ATM{} <- {} (wait={:.2f}m, st={:.2f}m)".format(
                    atm.aid, cust.cid, wait_h * 60.0, svc_min
                )
            )
            if self.logger is not None:
                self.logger.log_event(
                    self.now,
                    "START",
                    entity_id=cust.cid,
                    atm_id=atm.aid,
                    wait_min=wait_h * 60.0,
                    service_min=svc_min,
                    queue_len=len(self.queue),
                )

            self.schedule(Event(end_t, "departure", {"atm": atm, "cust": cust}))
            self.queue.sample_len(self.now)

    def handle_arrival(self):
        cid = next(self._cid_seq)
        cust = Customer("c{:03d}".format(cid), self.now)
        self.metrics.inc_arrivals()

        if (self.max_queue is not None) and (len(self.queue) >= self.max_queue):
            self.metrics.inc_balked()
            self.log("BALK    {} (q_full q={})".format(cust.cid, len(self.queue)))
            if self.logger is not None:
                self.logger.log_event(self.now, "BALK", entity_id=cust.cid, queue_len=len(self.queue))
        else:
            self.queue.enqueue(cust)
            self.log("ARRIVAL {} -> q={}".format(cust.cid, len(self.queue)))
            if self.logger is not None:
                self.logger.log_event(self.now, "ARRIVAL", entity_id=cust.cid, queue_len=len(self.queue))
            self.queue.sample_len(self.now)
            self._try_start_service()

        if self.rate > 0.0:
            next_t = self.now + self._expovariate_hours(self.rate)
            if next_t <= self.end_time:
                self.schedule(Event(next_t, "arrival", None))

    def handle_departure(self, payload):
        atm = payload["atm"]
        cust = payload["cust"]
        self.metrics.inc_completed()
        self.log("DONE    ATM{} -> {}".format(atm.aid, cust.cid))
        if self.logger is not None:
            self.logger.log_event(self.now, "DONE", entity_id=cust.cid, atm_id=atm.aid, queue_len=len(self.queue))
        atm.is_busy = False
        self._try_start_service()
        self.queue.sample_len(self.now)

    def run(self):
        self.initialize()
        while self.events:
            t, _, ev = heapq.heappop(self.events)
            if t > self.end_time:
                break
            self.now = t

            if self.logger is not None:
                while self._next_ts <= self.now:
                    self.logger.log_timeslice(
                        self._next_ts,
                        len(self.queue),
                        sum(a.is_busy for a in self.atms),
                        self.metrics.completed,
                        self.metrics.balked,
                        0,  # reneged (if you add later, wire it in)
                        [int(a.is_busy) for a in self.atms],
                    )
                    self._next_ts += self._ts_dt_h

            if ev.etype == "arrival":
                self.handle_arrival()
            elif ev.etype == "departure":
                self.handle_departure(ev.payload)
            else:
                self.log("UNKNOWN EVENT {}".format(ev.etype))

        self.queue.sample_len(self.end_time)
        if self.logger is not None:
            self.logger.log_timeslice(
                self.end_time,
                len(self.queue),
                sum(a.is_busy for a in self.atms),
                self.metrics.completed,
                self.metrics.balked,
                0,
                [int(a.is_busy) for a in self.atms],
            )

        avg_q = self.queue.average_len(self.end_time)
        waits = sorted(self.metrics.wait_times)
        avg_w = sum(waits) / len(waits) if waits else 0.0
        p95 = waits[int(0.95 * len(waits)) - 1] if waits else 0.0
        util = [atm.busy_time / max(1e-12, self.end_time) for atm in self.atms]

        print(
            "[END] time={:.02f}h, arrivals={}, balked={}, started={}, completed={}".format(
                self.end_time,
                self.metrics.arrivals,
                self.metrics.balked,
                self.metrics.started,
                self.metrics.completed,
            )
        )
        print("      avg_wait={:.2f}m (p95={:.2f}m)  avg_q_len={:.2f}".format(avg_w * 60.0, p95 * 60.0, avg_q))
        print(
            "      utilization: {}".format(
                ", ".join("ATM{}={:.2f}".format(i + 1, u) for i, u in enumerate(util))
            )
        )

        self._summary = {
            "arrivals": self.metrics.arrivals,
            "balked": self.metrics.balked,
            "started": self.metrics.started,
            "completed": self.metrics.completed,
            "avg_wait_min": avg_w * 60.0,
            "p95_wait_min": p95 * 60.0,
            "avg_queue_len": avg_q,
            "utilization": util,
            "duration_hours": self.end_time,
            "n_atms": len(self.atms),
        }

    def get_summary(self):
        return dict(self._summary)

def main():
    p = argparse.ArgumentParser(description="ATM Simulation (Poisson arrivals, service, balking) - Python 3.6+")
    p.add_argument("--rate", type=float, default=12.0, help="arrival rate (customers per hour)")
    p.add_argument("--duration", type=float, default=1.0, help="simulation duration (hours)")
    p.add_argument("--atms", type=int, default=2, help="number of ATM servers (c)")
    p.add_argument("--service-mean-min", type=float, default=3.0, help="mean service time in minutes")
    p.add_argument("--service-cv", type=float, default=0.6, help="service time coefficient of variation")
    p.add_argument("--max-queue", type=int, default=12, help="max waiting customers (>= triggers balking)")
    p.add_argument("--seed", type=int, default=None, help="random seed")
    args = p.parse_args()
    sim = SimulationEngine(
        rate_per_hour=args.rate,
        duration_hours=args.duration,
        seed=args.seed,
        n_atms=args.atms,
        svc_mean_min=args.service_mean_min,
        svc_cv=args.service_cv,
        max_queue=args.max_queue,
    )
    sim.run()

if __name__ == "__main__":
    main()
