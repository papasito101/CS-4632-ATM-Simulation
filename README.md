# CS-4632-ATM-Simulation
This will be a simulation on using an ATM

Minimal running prototype focused on **SimulationEngine** + **Poisson arrivals**.

## Status
- ✅ Discrete-event `SimulationEngine` with priority-queue scheduler
- ✅ Poisson customer arrivals (configurable rate per hour)
- ✅ Reproducible runs via `--seed`
- 🟡 Next: add service/queue, balking/reneging, metrics

## Examples
```bash
# Python 3.10+
cd src
python main.py --minutes 60 --rate 18 --seed 42
```

Example output:
```
[00.00] START sim (rate=18.0/hr, minutes=60, seed=42)
[00.09] ARRIVAL customer=1
[01.10] ARRIVAL customer=2
[01.13] ARRIVAL customer=3
...
[60.00] END sim
Arrivals: 18 | mean interarrival=3.29 min
```

## Files
atm.py - Main entrypoint
simulation_engine.py - DES scheduler
poisson.py - Poisson arrival generator
customer.py - Customer entity
