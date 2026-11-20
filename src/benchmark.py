import csv
from pathlib import Path
from time import perf_counter
import numpy as np
from baseline import bit_loading_scan
from modified import bit_loading_heap
from data import make_loading_case
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--config", required=True)
args = parser.parse_args()

root = Path(__file__).resolve().parent.parent

with (root / args.config).open(encoding="utf-8") as file:
    config = json.load(file)

gap = config["gap"]
bmax = config["bmax"]
repeats = config["repeats"]

methods = {
    "scan": bit_loading_scan,
    "heap": bit_loading_heap,
}

rows = []

for size_index, tones in enumerate(config["tones"]):
    budget = config["energy_per_tone"] * tones
    first_seed = config["seed_start"] + size_index * config["cases_per_size"]

    for seed in range(first_seed, first_seed + config["cases_per_size"]):
        g_true, g_hat = make_loading_case(
            seed,
            tones=tones,
            taps=config["taps"],
            noise_var=config["noise_var"],
            pilots=config["pilots"],
        )

        for condition, g in [("true", g_true), ("estimated", g_hat)]:
            scan_bits = bit_loading_scan(g, budget, gap, bmax)
            heap_bits = bit_loading_heap(g, budget, gap, bmax)
            assert np.array_equal(scan_bits, heap_bits)

            times = {"scan": [], "heap": []}

            for repeat in range(repeats):
                order = ["scan", "heap"]
                if repeat % 2 == 1:
                    order.reverse()

                for name in order:
                    start = perf_counter()
                    bits = methods[name](g, budget, gap, bmax)
                    elapsed = perf_counter() - start

                    assert np.array_equal(bits, scan_bits)

                    energy = np.sum(gap / g * (2.0 ** bits - 1))
                    assert energy <= budget + 1e-9

                    times[name].append(elapsed)

                    rows.append({
                        "tones": tones,
                        "seed": seed,
                        "condition": condition,
                        "method": name,
                        "repeat": repeat,
                        "gap": gap,
                        "bmax": bmax,
                        "budget": budget,
                        "total_bits": int(bits.sum()),
                        "energy": float(energy),
                        "runtime_s": elapsed,
                    })

            scan_ms = np.median(times["scan"]) * 1000
            heap_ms = np.median(times["heap"]) * 1000

            print(
                f"N={tones}, seed={seed}, {condition}: "
                f"scan={scan_ms:.3f} ms, heap={heap_ms:.3f} ms"
            )

run_name = Path(args.config).stem
output = root / "results" / f"{run_name}_timing.csv"
output.parent.mkdir(parents=True, exist_ok=True)

with output.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved {len(rows)} rows to {output}")