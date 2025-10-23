from __future__ import print_function
import argparse, csv, json, os, shlex, subprocess, sys, time
from pathlib import Path
from typing import Dict, Any, List

REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON_EXE = sys.executable  # current interpreter

def parse_args():
    p = argparse.ArgumentParser("RunManager - batch execute ATM sim experiments")
    p.add_argument("--plan", required=True, help="CSV with experiment rows")
    p.add_argument("--outdir", required=True, help="Root output directory, e.g. runs")
    p.add_argument("--config-format", choices=["json"], default="json")
    p.add_argument(
        "--command",
        required=True,
        help='Template to execute per row, e.g. "python main.py --config {config_path} --output-dir {run_dir}"',
    )
    p.add_argument("--force", action="store_true", help="Overwrite existing run directories")
    p.add_argument("--index-name", default="runs_index.csv", help="Name for the master index CSV")
    return p.parse_args()

def read_plan(plan_path: Path) -> List[Dict[str, str]]:
    rows = []
    with open(plan_path, "r") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({k.strip(): v.strip() for k, v in r.items()})
    if not rows:
        raise RuntimeError("Plan file has no data rows: {}".format(plan_path))
    return rows

def build_config(row: Dict[str, str]) -> Dict[str, Any]:
    return {
        "atms": int(row["atms"]),
        "duration_hours": float(row["duration_hours"]),
        "arrival_rate_per_hour": float(row["arrival_rate_per_hour"]),
        "service_mean_min": float(row["service_mean_min"]),
        "service_cv": float(row["service_cv"]),
        "max_queue": int(row["max_queue"]),
        "seed": int(row["seed"]),
        "timeseries_dt_min": float(row.get("timeseries_dt_min", 0.5)),
    }

def run_command(cmd: str):
    """Run a shell command and return (rc, wall_seconds, stdout, stderr)."""
    t0 = time.time()
    # IMPORTANT: On Windows, use posix=False so backslashes and quotes survive correctly.
    args = shlex.split(cmd, posix=(os.name != "nt"))
    proc = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        shell=False,
        cwd=str(REPO_ROOT),
    )
    wall = time.time() - t0
    return proc.returncode, wall, proc.stdout, proc.stderr

def main():
    args = parse_args()
    out_root = Path(args.outdir)
    out_root.mkdir(parents=True, exist_ok=True)

    plan_rows = read_plan(Path(args.plan))
    index_rows = []

    for row in plan_rows:
        run_id = row["run_id"]
        purpose = row.get("purpose", "")
        run_dir = out_root / ("run_" + run_id)

        if run_dir.exists() and args.force:
            for root, dirs, files in os.walk(str(run_dir), topdown=False):
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                    except Exception:
                        pass
                for name in dirs:
                    try:
                        os.rmdir(os.path.join(root, name))
                    except Exception:
                        pass
            try:
                os.rmdir(str(run_dir))
            except Exception:
                pass

        run_dir.mkdir(parents=True, exist_ok=True)

        cfg = build_config(row)
        cfg_path = run_dir / "run_config.json"
        cfg_path.write_text(json.dumps(cfg, indent=2))

        cmd = args.command.format(
            python=PYTHON_EXE,
            config_path=str(cfg_path.resolve()),
            run_dir=str(run_dir.resolve()),
        )

        rc, wall, out, err = run_command(cmd)

        (run_dir / "stdout.log").write_text(out)
        (run_dir / "stderr.log").write_text(err)

        if rc != 0 and err:
            first_line = err.splitlines()[0] if err.splitlines() else err
            print("  stderr:", first_line)

        index_rows.append({
            "run_id": run_id,
            "purpose": purpose,
            "status": "OK" if rc == 0 else "ERR",
            "rc": rc,
            "wall_seconds": "{:.3f}".format(wall),
            "config_path": str(cfg_path),
            "run_dir": str(run_dir),
        })
        print("Run {}: rc={} wall={:.2f}s".format(run_id, rc, wall))

    index_path = out_root / args.index_name
    with open(index_path, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["run_id", "purpose", "status", "rc", "wall_seconds", "config_path", "run_dir"]
        )
        writer.writeheader()
        writer.writerows(index_rows)

    print("Wrote {} rows to {}".format(len(index_rows), index_path))

if __name__ == "__main__":
    main()
