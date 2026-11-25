import csv
import json
from pathlib import Path
from time import perf_counter_ns

import numpy as np

from data import make_loading_case
from modified import build_heap


root = Path(__file__).resolve().parent.parent
config = json.loads((root / "configs/final.json").read_text(encoding="utf-8"))
rows = []

for index, tones in enumerate(config["tones"]):
    cases = config["cases_per_size"]
    first_seed = config["seed_start"] + index * cases
    group_times = {"true": [], "estimated": []}

    for seed in range(first_seed, first_seed + cases):
        g_true, g_hat = make_loading_case(
            seed, tones, config["taps"],
            config["noise_var"], config["pilots"]
        )

        for condition, g in [("true", g_true), ("estimated", g_hat)]:
            build_heap(g, config["gap"])
            times = []

            for _ in range(config["repeats"]):
                start = perf_counter_ns()
                heap = build_heap(g, config["gap"])
                elapsed = perf_counter_ns() - start
                del heap
                times.append(elapsed / 1_000_000)

            setup_ms = float(np.median(times))
            rows.append([tones, seed, condition, setup_ms])
            group_times[condition].append(setup_ms)

    for condition, times in group_times.items():
        print(f"N={tones}, {condition}: mean heap setup={np.mean(times):.4f} ms")

output = root / "results" / "heap_setup_timing.csv"
output.parent.mkdir(parents=True, exist_ok=True)

with output.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["tones", "seed", "condition", "heap_setup_ms"])
    writer.writerows(rows)

print(f"Saved {len(rows)} rows to {output}")