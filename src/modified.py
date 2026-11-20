import heapq
import numpy as np

def bit_loading_heap(g, energy_budget, gap=1.0, bmax=6):
    g = np.asarray(g, dtype=float)

    bits = np.zeros(len(g), dtype=int)
    remaining = float(energy_budget)

    heap = []
    if bmax > 0:
        heap = [(gap / g[i], i) for i in range(len(g))]
        heapq.heapify(heap)

    while heap:
        cost, i = heapq.heappop(heap)

        if cost > remaining:
            break

        remaining -= cost
        bits[i] += 1

        if bits[i] < bmax:
            heapq.heappush(heap, (cost * 2, i))

    return bits


if __name__ == "__main__":
    from baseline import bit_loading_scan

    g = np.array([2.0, 1.0, 0.5])

    for budget in [0.0, 0.4, 1.0, 3.0, 8.0, 30.0]:
        scan_bits = bit_loading_scan(g, budget, bmax=3)
        heap_bits = bit_loading_heap(g, budget, bmax=3)

        assert np.array_equal(scan_bits, heap_bits)

        print(
            f"Budget: {budget}, "
            f"scan: {scan_bits}, heap: {heap_bits}"
        )

    print("All allocation comparisons passed.")