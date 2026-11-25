import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


results = Path(__file__).resolve().parent.parent / "results"


def read_results(filename):
    times = defaultdict(list)
    bits = {}

    with (results / filename).open(encoding="utf-8") as file:
        for row in csv.DictReader(file):
            case = (int(row["tones"]), row["condition"], int(row["seed"]))
            times[case + (row["method"],)].append(float(row["runtime_s"]) * 1000)
            bits[case] = int(row["total_bits"])

    saved = {}
    for case in bits:
        scan = np.median(times[case + ("scan",)])
        heap = np.median(times[case + ("heap",)])
        saved[case] = scan - heap

    return saved, bits


normal, normal_bits = read_results("final_timing.csv")
stress, stress_bits = read_results("stress_timing.csv")

if normal.keys() != stress.keys():
    raise ValueError("The normal and stress runs must use the same channel cases.")

fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

for ax, condition in zip(axes, ["true", "estimated"]):
    for index, tones in enumerate([64, 256, 1024]):
        cases = sorted(
            case for case in normal
            if case[0] == tones and case[1] == condition
        )

        for label, saved, bits, offset in [
            ("Normal budget", normal, normal_bits, -0.12),
            ("Low budget", stress, stress_bits, 0.12),
        ]:
            differences = [saved[case] for case in cases]
            counts = [bits[case] for case in cases]

            ax.scatter(
                [index + offset] * len(cases),
                differences,
                alpha=0.6,
                color="tab:blue" if label == "Normal budget" else "tab:orange",
                label=label if index == 0 else None,
            )

            print(
                f"N={tones}, {condition}, {label}: "
                f"{len(cases)} channels, bits={min(counts)}-{max(counts)}, "
                f"mean saved={np.mean(differences):.4f} ms"
            )

    ax.axhline(0, color="grey", linestyle="--")
    ax.set_xticks([0, 1, 2], ["64", "256", "1024"])
    ax.set_xlabel("Number of subcarriers")
    ax.set_title(f"{condition.capitalize()} channel information")
    ax.legend()

axes[0].set_ylabel("Time saved per channel (scan - heap, ms)")
fig.suptitle("Runtime comparison under normal and low energy budgets")
fig.tight_layout()
fig.savefig(results / "stress_comparison.png", dpi=200)
plt.close(fig)