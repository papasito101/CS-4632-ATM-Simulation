# CS-4632 ATM Simulation

## Simulation Features
- Poisson **arrivals** (exponential inter-arrival times; hours as base unit)
- Numerous **ATMs** (c servers) and a FIFO queue
- **Lognormal service** times (mean minutes + CV)
- **Balking** logic when queue is at maximum capacity
- Metrics details these elements: arrivals, balked, started, completed, average wait, p95 wait, average queue length, per-ATM utilization
- Console logging: ARRIVAL; START; DONE; BALK

## How To Install
```bash
pip install -r requirements.txt
```

## How To Simulate
```bash
python .\simulation_engine.py --rate 12 --duration 1.0 --atms 2 --service-mean-min 3.0 --service-cv 0.6 --max-queue 12 --seed 7
```
Python arguments:
- `--rate`: arrival/hour (λ); default value: 12.0
- `--duration`: horizon in **hours**; default value: 1.0
- `--atms`: number of ATMs; default value: 2
- `--service-mean-min`: mean service time (minutes); default value: 3.0
- `--service-cv`: service time coefficient of variation; default value: 0.6
- `--max-queue`: max waiting customers before **balk**; default value: 12
- `--seed`: RNG seed

## Expected Output
```
[0.09h] ARRIVAL c001 -> q=1
[0.09h] START   ATM1 <- c001 (wait=0.00m, st=0.99m)
[0.11h] DONE    ATM1 -> c001
[0.31h] ARRIVAL c002 -> q=1
[0.31h] START   ATM1 <- c002 (wait=0.00m, st=2.71m)
[0.36h] DONE    ATM1 -> c002
[0.55h] ARRIVAL c003 -> q=1
[0.55h] START   ATM1 <- c003 (wait=0.00m, st=2.59m)
[0.59h] DONE    ATM1 -> c003
[0.62h] ARRIVAL c004 -> q=1
[0.62h] START   ATM1 <- c004 (wait=0.00m, st=1.70m)
[0.65h] DONE    ATM1 -> c004
[0.79h] ARRIVAL c005 -> q=1
[0.79h] START   ATM1 <- c005 (wait=0.00m, st=1.27m)
[0.80h] ARRIVAL c006 -> q=1
[0.80h] START   ATM2 <- c006 (wait=0.00m, st=2.91m)
[0.80h] ARRIVAL c007 -> q=1
[0.81h] DONE    ATM1 -> c005
[0.81h] START   ATM1 <- c007 (wait=0.88m, st=4.16m)
[0.85h] DONE    ATM2 -> c006
[0.88h] DONE    ATM1 -> c007
[END] time=1.00h, arrivals=7, balked=0, started=7, completed=7
      avg_wait=0.13m (p95=0.00m)  avg_q_len=0.01
      utilization: ATM1=0.22, ATM2=0.05
```

## Repo Structure
```
/src
  atm.py
  customer.py
  metrics.py
  queue_system.py
  simulation_engine.py
/test
  .gitkeep
.gitignore
README.md
requirements.txt
```
