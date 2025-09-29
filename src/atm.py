from __future__ import annotations
import argparse
from typing import List
from simulation_engine import SimulationEngine
from poisson_source import PoissonArrivalSource

def fmt(t: float) -> str:
    return f"[{t:05.2f}]"

def main():
    parser = argparse.ArgumentParser(description="ATM Simulation (Day 1–2): Engine + Poisson arrivals")
    parser.add_argument("--minutes", type=float, default=60.0, help="Simulation length in minutes (default: 60)")
    parser.add_argument("--rate", type=float, default=18.0, help="Arrival rate (customers per hour). E.g., 12-20 per proposal")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    args = parser.parse_args()

    eng = SimulationEngine()
    arrivals: List[float] = []

    def on_arrival(cust):
        print(f"{fmt(eng.time)} ARRIVAL customer={cust.cid}")
        arrivals.append(eng.time)

    print(f"{fmt(0.0)} START sim (rate={args.rate}/hr, minutes={args.minutes}, seed={args.seed})")
    source = PoissonArrivalSource(eng, rate_per_hour=args.rate, on_arrival=on_arrival, seed=args.seed)
    source.start(until_minutes=args.minutes)
    eng.run(until=args.minutes)
    print(f"{fmt(args.minutes)} END sim")

    # Simple stats
    if len(arrivals) >= 2:
        inter = [arrivals[i]-arrivals[i-1] for i in range(1, len(arrivals))]
        mean_inter = sum(inter)/len(inter)
        print(f"Arrivals: {len(arrivals)} | mean interarrival={mean_inter:.2f} min")
    else:
        print(f"Arrivals: {len(arrivals)}")

if __name__ == "__main__":
    main()
