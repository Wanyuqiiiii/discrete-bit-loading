import numpy as np
from baseline import bit_loading_scan
from modified import bit_loading_heap
from data import make_loading_case

gap = 1.0
bmax = 6
checked = 0

for tones in [64, 256, 1024]:
    budget = float(tones)

    for seed in range(5):
        g_true, g_hat = make_loading_case(seed, tones=tones)

        for name, g in [("true", g_true), ("estimated", g_hat)]:
            original = g.copy()
            scan_bits = bit_loading_scan(g, budget, gap, bmax)
            assert np.array_equal(g, original)

            heap_bits = bit_loading_heap(g, budget, gap, bmax)
            assert np.array_equal(g, original)

            assert np.array_equal(scan_bits, heap_bits)

            for bits in [scan_bits, heap_bits]:
                energy = np.sum(gap / g * (2.0 ** bits - 1))

                assert bits.shape == (tones,)
                assert np.all(np.isfinite(bits))
                assert np.all(bits == np.floor(bits))
                assert np.all((bits >= 0) & (bits <= bmax))
                assert np.isfinite(energy)
                assert energy <= budget + 1e-9

            checked += 1

            print(
                f"N={tones}, seed={seed}, input={name}, "
                f"total bits={scan_bits.sum()}, agreement=True"
            )

print(f"All {checked} channel comparisons passed.")