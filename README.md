# discrete-bit-loading

## Overview
This project studies bit allocation under a total energy budget,
based on Campello's paper "Practical Bit Loading for DMT" (1999).

## Methods
The baseline scans all eligible subcarriers to find the cheapest
one-bit increment. I plan to replace this scan with a min-heap
and compare the runtime.

## Experiments
Both methods will use the same channels, energy budget and bit
limits. I will check allocation agreement, total bits and energy
use, and measure runtime for different numbers of subcarriers.

## Setup and quick checks

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

The smoke run saves eight timing records to `results/smoke_timing.csv`.

## Reproduce the results

Run these commands from the project folder on Windows.

```bat
.venv\Scripts\python.exe src/benchmark.py --config configs/final.json
.venv\Scripts\python.exe src/analyse_results.py
.venv\Scripts\python.exe src/benchmark.py --config configs/stress.json
.venv\Scripts\python.exe src/analyse_stress.py
.venv\Scripts\python.exe src/benchmark_heap_setup.py
```

The timing tables and figures are saved in `results/`. The main comparison is
shown in `runtime_difference.png`. The low-budget comparison is shown in
`stress_comparison.png`. Heap setup times are saved in `heap_setup_timing.csv`.

## Experiment settings

We tested 64, 256 and 1024 subcarriers, with 20 channels per size.
The random seeds were 1000–1019, 1020–1039 and 1040–1059, respectively.
For each channel, we timed both methods 10 times using true channel
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

