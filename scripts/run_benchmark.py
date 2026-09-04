import csv
from pathlib import Path
from twinsec.benchmark.runner import BenchmarkRunner

rows = BenchmarkRunner(seed=7, steps=180).run_suite()
out = Path("results")
out.mkdir(exist_ok=True)
path = out / "baseline_metrics.csv"
with path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
print(f"Wrote {len(rows)} rows to {path}")
