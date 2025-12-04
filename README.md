# CS-4632 ATM Simulation  
### CS 4632 – Modeling & Simulation  
### Esai Dudoit
### Kennesaw State University
### December 4, 2025

---

## Overview
In this project, a discrete-event simulation model will be used to test out an ATM queue service system.
Among the elements for this model are:
- Poisson arrivals
- Lognormal service times
- A group of ATMs
- Queue capacity
- Customer balking
- Smoke tests and batch run experimentations
- Analysis outputs

We will be evaluating waiting times, the lengths of queues, utilizing ATMs, and customer behavior in every operational condition.

---

## Simulation Features
- Poisson **arrivals** (exponential inter-arrival times; hours as base unit)
- Numerous **ATMs** (c servers) and a FIFO queue
- **Lognormal service** times (mean minutes + CV)
- **Balking** logic when queue is at maximum capacity
- Metrics details these elements: arrivals, balked, started, completed, average wait, p95 wait, average queue length, per-ATM utilization
- Console logging: ARRIVAL; START; DONE; BALK
- **Batch experiments** tested with both `run_manager.py` and `plan.csv` 
- Collections of data: `events.csv`, `timeseries.csv`, `summary.json`, `meta.json`
- **Different scenarios** for the model: Normal, Lunch-Rush, High-Variability, Cap-Tight, Staff-Added

---

## Repo Structure
```
CS-4632-ATM-Simulation
  /config
    /example.yml
  /experiments
    /plan.csv
  /runs
    /run_XXX
    /smoke
    /runs_index.csv
  /src
    /__init__.py
    /atm.py
    /customer.py
    /metrics.py
    /queue_system.py
    /run_logger.py
    /simulation_engine.py
  /test
    /.gitkeep
  /tools
    /run_manager.py
  /main.py
  /.gitignore
  /README.md
  /requirements
```

---

## Installation
**Python version 3.6** was used in the making of this project.

Clone repository:
```bash
git clone https://github.com/papasito101/CS-4632-ATM-Simulation.git
cd CS-4632-ATM-Simulation
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## How To Simulate
### Smoke test:
```bash
python main.py --config config/example.yml --output-dir runs/smoke
```

Include in ```runs/smoke``` are:
- ```events.csv```
- ```timeseries.csv```
- ```meta.json```
- ```run_config.json```
- ```summary.json```
- ```walltime.txt```

---

### Batch experiment
```bash
python tools\run_manager.py --plan experiments\plan.csv --outdir runs --config-format json --command "{python} main.py --config \"{config_path}\" --output-dir \"{run_dir}\""
```

---

### Configuration
```yaml
atms: 2
duration_hours: 4
arrival_rate_per_hour: 12
service_mean_min: 3.5
service_cv: 0.6
max_queue: 12
seed: 42
timeseries_dt_min: 0.5
```

---

### Outputs
Included in each ```runs/run_XXX``` folders are:
- ```events.csv```
- ```timeseries.csv```
- ```meta.json```
- ```run_config.json```
- ```summary.json```
- ```stderr.log```
- ```stdout.log```
- ```walltime.txt```

---

### Future
- Incorporating method of determining reneging behavior
- A model for ATM reliability
- A policy for cash inventory (s, S)
- Visualization with a GUI

---

### License
This project has been created for educational and instructional purposes for this class of Kennesaw State University. Any other use of this project without permission from the author is prohibited.
