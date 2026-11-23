import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


root = Path(__file__).resolve().parent.parent

with (root / "results/final_timing.csv").open(
    encoding="utf-8"
) as file:
    records = list(csv.DictReader(file))

groups = {}

for row in records:
    key = (
        int(row["tones"]),
        row["condition"],
        int(row["seed"]),
        row["method"],
    )

    groups.setdefault(key, []).append(float(row["runtime_s"]))

medians = {}

for key, times in groups.items():
    medians[key] = np.median(times) * 1000

summary = []
paired = []
rng = np.random.default_rng(2026)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

for ax, condition in zip(axes, ["true", "estimated"]):
    sizes = []
    savings = []
    lower_errors = []
    upper_errors = []

    for tones in [64, 256, 1024]:
        seeds = sorted({
            key[2] for key in medians
            if key[0] == tones and key[1] == condition
        })

        scan = np.array([
            medians[(tones, condition, seed, "scan")]
            for seed in seeds
        ])

        heap = np.array([
            medians[(tones, condition, seed, "heap")]
            for seed in seeds
        ])

        difference = scan - heap
        mean_difference = difference.mean()

        samples = rng.choice(
            difference, size=(10000, len(seeds)), replace=True
        )
        low, high = np.percentile(samples.mean(axis=1), [2.5, 97.5])

        summary.append([
            tones, condition, len(seeds),
            scan.mean(), heap.mean(),
            mean_difference, low, high
        ])

        for seed, s, h in zip(seeds, scan, heap):
            paired.append([tones, condition, seed, s, h, s - h])

        print(
            f"N={tones}, {condition}: "
            f"scan={scan.mean():.3f} ms, "
            f"heap={heap.mean():.3f} ms, "
            f"saved={mean_difference:.3f} ms"
        )

        sizes.append(str(tones))
        savings.append(mean_difference)
        lower_errors.append(max(0, mean_difference - low))
        upper_errors.append(max(0, high - mean_difference))

    ax.errorbar(
        sizes, savings,
        yerr=[lower_errors, upper_errors],
        fmt="o-", capsize=5
    )
    ax.axhline(0, color="grey", linestyle="--")
    ax.set_title(f"{condition.capitalize()} channel information")
    ax.set_xlabel("Number of subcarriers")
    ax.set_ylabel("Mean time saved: scan - heap (ms)")
    ax.grid(alpha=0.3)

fig.suptitle("Paired runtime differences with 95% bootstrap intervals")
fig.tight_layout()
fig.savefig(root / "results/runtime_difference.png", dpi=200)
plt.close(fig)

tables = [
    (
        "timing_summary.csv",
        ["tones", "condition", "channels", "scan_mean_ms",
         "heap_mean_ms", "saved_mean_ms", "ci_low_ms", "ci_high_ms"],
        summary,
    ),
    (
        "paired_timing.csv",
        ["tones", "condition", "seed", "scan_ms", "heap_ms", "saved_ms"],
        paired,
    ),
]

for filename, header, rows in tables:
    with (root / "results" / filename).open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

print("Saved summary tables and runtime_difference.png")