import csv
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

class RunLogger(object):
    def __init__(self, output_dir: str, config: Dict[str, Any], timeseries_dt_min: float = 0.5):
        self.out = Path(output_dir)
        self.out.mkdir(parents=True, exist_ok=True)

        # Files
        self.cfg_path = self.out / "run_config.json"
        self.events_path = self.out / "events.csv"
        self.ts_path = self.out / "timeseries.csv"
        self.summary_path = self.out / "summary.json"
        self.meta_path = self.out / "meta.json"

        # Used config
        self.cfg_path.write_text(json.dumps(config, indent=2))

        # Timeseries
        self.timeseries_dt_min = float(timeseries_dt_min)
        self._last_timeslice_t = None  # type: Optional[float]

        # CSV headers
        with open(self.events_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow([
                "sim_time_min", "type", "entity_id", "atm_id",
                "wait_min", "service_min", "queue_len", "message"
            ])

        with open(self.ts_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow([
                "sim_time_min", "queue_len", "in_service",
                "completed", "balked", "reneged", "atm_busy_flags"
            ])

        self._t0 = time.time()

    def log_event(
        self,
        sim_time_hours: float,
        etype: str,
        entity_id: Any = "",
        atm_id: Any = "",
        wait_min: Optional[float] = None,
        service_min: Optional[float] = None,
        queue_len: Optional[int] = None,
        message: str = "",
        **kwargs
    ) -> None:
        sim_time_min = float(sim_time_hours) * 60.0
        row = [
            "{:.6f}".format(sim_time_min),
            etype,
            entity_id if entity_id is not None else "",
            atm_id if atm_id is not None else "",
            "" if wait_min is None else "{:.6f}".format(float(wait_min)),
            "" if service_min is None else "{:.6f}".format(float(service_min)),
            "" if queue_len is None else int(queue_len),
            message or ""
        ]
        with open(self.events_path, "a", newline="") as f:
            csv.writer(f).writerow(row)

    def log_timeslice(
        self,
        sim_time_hours: float,
        queue_len: int,
        in_service: int,
        completed: int,
        balked: int,
        reneged: int,
        atm_busy_flags: Iterable[int]
    ) -> None:
        sim_time_min = float(sim_time_hours) * 60.0
        if (self._last_timeslice_t is None) or \
           ((sim_time_min - self._last_timeslice_t) >= (self.timeseries_dt_min - 1e-9)):
            with open(self.ts_path, "a", newline="") as f:
                csv.writer(f).writerow([
                    "{:.6f}".format(sim_time_min),
                    int(queue_len),
                    int(in_service),
                    int(completed),
                    int(balked),
                    int(reneged),
                    "".join(str(int(b)) for b in atm_busy_flags)
                ])
            self._last_timeslice_t = sim_time_min

    def finalize(self, summary: Dict[str, Any]) -> None:
        wall = time.time() - self._t0
        self.summary_path.write_text(json.dumps(summary, indent=2))
        self.meta_path.write_text(json.dumps({"wall_seconds": wall}, indent=2))
        # Convenience single-line walltime
        (self.out / "walltime.txt").write_text("{:.3f}\n".format(wall))
