from itertools import product
import numpy as np
from baseline import bit_loading_scan

g = np.array([2.0, 1.0, 0.5])
gap = 1.0
bmax = 3

for budget in [0.0, 0.4, 1.0, 3.0, 8.0, 30.0]:
    best_total = 0

    for allocation in product(range(bmax + 1), repeat=len(g)):
        candidate = np.array(allocation)
        energy = np.sum(gap / g * (2.0 ** candidate - 1))

        if energy <= budget:
            best_total = max(best_total, candidate.sum())

    bits = bit_loading_scan(g, budget, gap, bmax)
    used = np.sum(gap / g * (2.0 ** bits - 1))

    assert bits.sum() == best_total
    assert used <= budget
    assert np.all((bits >= 0) & (bits <= bmax))

    print(
        f"Budget: {budget}, bits: {bits}, "
        f"total: {bits.sum()}, best: {best_total}"
    )

print("All exhaustive checks passed.")