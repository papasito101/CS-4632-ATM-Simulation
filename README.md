# CS-4632 ATM Simulation (Day 1–2 Starter)

This repository contains a minimal **Day 1–2** starter for your Modeling & Simulation project.

## What’s implemented so far
- Project structure with `src/` modules
- A basic **SimulationEngine** with an **event queue**
- **Poisson arrivals** (exponential inter-arrival times)
- A simple FIFO **QueueSystem** to hold arriving customers
- Console logging for arrivals + queue length snapshots

> This satisfies the first milestone step of *“Set up repo + basic SimulationEngine + Poisson arrivals.”*

## Python Version
- Tested to be compatible with **Python 3.6** (no external dependencies).

## How to run
```bash
python src/simulation_engine.py --rate 15 --duration 2.0 --seed 42
```
**Arguments**
- `--rate` (λ): average arrivals per hour (default 12)
- `--duration`: simulation time **in hours** (default 1.0)
- `--seed`: RNG seed for reproducibility (optional)

## Example output
```
[00.01h] ARRIVAL c001 -> queue_len=1
[00.02h] ARRIVAL c002 -> queue_len=2
[00.03h] ARRIVAL c003 -> queue_len=3
...
[END] time=1.00h, arrivals=18, avg_queue_len=2.14
```

## Repository layout
```
/src
  simulation_engine.py   # event loop, Poisson generator, logging
  customer.py            # Customer entity
  queue_system.py        # FIFO queue + sampling helpers
  atm.py                 # placeholder for later (service logic)
  metrics.py             # basic counters and queue-length statistics
/tests
  (add tests here)
requirements.txt
.gitignore
README.md
```

## Next steps (Day 3–4)
- Implement **ATM service** with **lognormal** service times
- Start customers into service when ATM is free
- Add **balking** (max queue length) or **reneging** (patience timeout)
- Track metrics: wait times, service completions, utilization
- Commit often + move tasks on your Project board
```
