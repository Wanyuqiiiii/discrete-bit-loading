# discrete-bit-loading

## Overview
This project studies bit allocation under a total energy budget,
based on Campello's paper "Practical Bit Loading for DMT" (1999).

## Methods
The baseline in `src/baseline.py` scans the subcarriers to find the cheapest
place to add one bit. In `src/modified.py`, I replaced this scan with a
min-heap. Both methods use the same rule for allocating bits.

## Experiments
I used `src/data.py` to generate the channels. I ran both methods on the
same inputs, checked that their allocations agreed, and compared their
runtimes. The timing tables and figures are in `results/`.

## Setup and quick checks
I tested the project on Windows with Python 3.13.15 and the package versions listed in `requirements.txt`.
```cmd
git clone https://github.com/Wanyuqiiiii/discrete-bit-loading.git
cd discrete-bit-loading
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe src/check_baseline.py
.venv\Scripts\python.exe src/modified.py
.venv\Scripts\python.exe src/check_channels.py
.venv\Scripts\python.exe src/benchmark.py --config configs/smoke.json
```
On my computer, `src/check_baseline.py` took about 0.14 seconds.
It checked six energy budgets and printed `All exhaustive checks passed.`
`src/modified.py` took about 0.13 seconds. The scan and heap methods gave the same allocation for all six budgets.
`src/check_channels.py` took about 0.41 seconds and printed `All 30 channel comparisons passed.`
The smoke run took about 0.18 seconds on my computer and saved 8 timing records to `results/smoke_timing.csv`.

## Reproduce the results

Run these commands from the project folder on Windows.

```bat
.venv\Scripts\python.exe src/benchmark.py --config configs/final.json
.venv\Scripts\python.exe src/analyse_results.py
.venv\Scripts\python.exe src/benchmark.py --config configs/stress.json
.venv\Scripts\python.exe src/analyse_stress.py
.venv\Scripts\python.exe src/benchmark_heap_setup.py
```

Approximate runtimes on my computer are shown below. All output files are saved in `results/`.

| Script | Time | Expected output |
|---|---:|---|
| `benchmark.py --config configs/final.json` | 11.29 s | `final_timing.csv` with 2,400 timing records |
| `analyse_results.py` | 0.98 s | `timing_summary.csv`, `paired_timing.csv` and `runtime_difference.png` |
| `benchmark.py --config configs/stress.json` | 0.46 s | `stress_timing.csv` with 2,400 timing records |
| `analyse_stress.py` | 0.92 s | `stress_comparison.png` |
| `benchmark_heap_setup.py` | 0.25 s | `heap_setup_timing.csv` with 120 records |

## Experiment settings

I simulated each channel with 8 taps and a noise variance of 0.1.
I estimated the channel response by averaging 20 noisy pilot observations.
Both methods used a gap of 1 and a limit of 6 bits per subcarrier.

The smoke test used seed 50. The final tests used a separate set of seeds
starting at 1000. For each seed, both methods used the same channel so
their runtimes could be compared on the same input.

I tested 64, 256 and 1024 subcarriers, with 20 channels per size.
The random seeds were 1000–1019, 1020–1039 and 1040–1059, respectively.
For each channel, I timed both methods 10 times using true channel
information and 10 times using estimated channel information.

The stress test used the same channels and reduced the energy budget
per subcarrier from 1 to 0.001.

## Limitations

The tests used simulated channels with up to 1024 subcarriers.

## AI assistance

I used AI to help write parts of the heap-based algorithm，the script that measures heap setup time and the script for analysing the low-budget test results. It also helped me draft the instructions for running the experiments in the README.

## References

The bit-loading model and energy formula follow the guide in
`ResearchProjectTopics.pdf`

