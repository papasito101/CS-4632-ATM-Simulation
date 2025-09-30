# CS-4632 ATM Simulation

**Day 3–4 milestone implemented**: ATM service + queue + balking. Python **3.6** compatible.

## Features
- Poisson **arrivals** (exponential inter-arrival times; hours as base unit)
- Multiple **ATMs** (c servers), FIFO queue
- **Lognormal service times** (configured by mean minutes + CV)
- **Balking** when queue length ≥ max allowed
- Metrics: arrivals, balked, started, completed, average wait, p95 wait, average queue length, per-ATM utilization
- Console logging of ARRIVAL / START / DONE / BALK

## Run
```bash
python src/simulation_engine.py --rate 18 --duration 2.0 --atms 2 --service-mean-min 3.0 --service-cv 0.6 --max-queue 12 --seed 7
```
Arguments:
- `--rate`: arrivals/hour (λ), default 12.0
- `--duration`: horizon in **hours**, default 1.0
- `--atms`: number of ATMs, default 2
- `--service-mean-min`: mean service time (minutes), default 3.0
- `--service-cv`: service time coefficient of variation, default 0.6
- `--max-queue`: max waiting customers before **balk**, default 12
- `--seed`: RNG seed

## Example (truncated)
```
[00.01h] ARRIVAL c001 -> q=1
[00.01h] START   ATM1 <- c001 (wait=0.00m, st=2.97m)
[00.06h] ARRIVAL c002 -> q=1
[00.07h] START   ATM2 <- c002 (wait=1.10m, st=2.41m)
...
[END] time=2.00h, arrivals=33, balked=3, started=30, completed=29
      avg_wait=5.42m (p95=18.73m)  avg_q_len=1.61
      utilization: ATM1=0.42, ATM2=0.39
```

## Layout
```
/src
  simulation_engine.py
  customer.py
  queue_system.py
  atm.py
  metrics.py
/tests
  .gitkeep
requirements.txt
.gitignore
README.md
```
