# CS-4632 ATM Simulation

## Simulation Features
- Poisson **arrivals** (exponential inter-arrival times; hours as base unit)
- Numerous **ATMs** (c servers) and a FIFO queue
- **Lognormal service** times (mean minutes + CV)
- **Balking** logic when queue is at maximum capacity
- Metrics details these elements: arrivals, balked, started, completed, average wait, p95 wait, average queue length, per-ATM utilization
- Console logging: ARRIVAL; START; DONE; BALK

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

## How To Install
```bash
pip install -r requirements.txt
```

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

### Batch experiment
```bash
python tools\run_manager.py --plan experiments\plan.csv --outdir runs --config-format json --command "{python} main.py --config \"{config_path}\" --output-dir \"{run_dir}\""
```

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
