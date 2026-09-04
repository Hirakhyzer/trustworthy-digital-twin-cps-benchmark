from twinsec.benchmark.runner import BenchmarkRunner
from twinsec.benchmark.transfer import leave_one_domain_out_thresholds

runner = BenchmarkRunner(seed=7)
native = {d: runner.calibrate_domain(d) for d in [
    "battery","water","robot","microgrid","factory","ev_charging","railway"
]}
transfer = leave_one_domain_out_thresholds(runner)
for domain in native:
    gap = abs(native[domain] - transfer[domain]) / max(native[domain], 1e-9)
    print(f"{domain:12s} native={native[domain]:.3f} transfer={transfer[domain]:.3f} gap={gap:.1%}")
