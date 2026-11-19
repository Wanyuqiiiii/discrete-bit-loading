import numpy as np

def bit_loading_scan(g, energy_budget, gap=1.0, bmax=6):
    g = np.asarray(g, dtype=float)

    bits = np.zeros(len(g), dtype=int)
    cost = gap / g
    remaining = float(energy_budget)

    while np.any(bits < bmax):
        eligible_cost = np.where(bits < bmax, cost, np.inf)
        i = np.argmin(eligible_cost)

        if eligible_cost[i] > remaining:
            break

        remaining -= eligible_cost[i]
        bits[i] += 1
        cost[i] *= 2

    return bits

if __name__ == "__main__":
    g = np.array([2.0, 1.0])
    budget = 3.0

    bits = bit_loading_scan(g, budget, gap=1.0, bmax=3)
    energy = np.sum((2.0 ** bits - 1) / g)

    print("Bit allocation:", bits)
    print("Total bits:", bits.sum())
    print("Energy used:", energy)
    print("Energy budget:", budget)

    assert np.array_equal(bits, [2, 1])
    assert energy <= budget

    zero_bits = bit_loading_scan(g, 0.0)
    assert np.all(zero_bits == 0)

    print("Checks passed.")