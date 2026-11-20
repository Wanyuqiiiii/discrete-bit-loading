##1
Implemented the scan-based bit allocation method.

The two-subcarrier example returned [2, 1], using 2.5 energy
units under a budget of 3. The zero-budget check also passed.

Next: verify small cases using exhaustive enumeration.


##2
Checked the scan method against exhaustive enumeration.
For three subcarriers with a cap of 3 bits each, all 64
allocations were examined at each of six energy budgets.
The scan method matched the optimal total bits in every case
and stayed within the energy budget and bit limits.

Next: implement the min-heap version.

##3
Added a min-heap version using Python's heapq module.
When two subcarriers have the same cost, the one with the lower
index is chosen, just like in the scan version.

Both methods returned identical allocations for the six
small budget cases.

Next: test more channel cases and compare runtime.

##4
Added the synthetic channel generator from the mathematical guide.
It returns true channel quality and an estimate from noisy pilots
and separate noise measurements.

Shape, finite-value and sign checks passed. Repeating the same
seed produced identical data.

Next: compare both allocation methods on generated channels.

##5
Checked both allocation methods on generated channels with
64, 256 and 1024 subcarriers, using development seeds 0–4.

All 30 comparisons passed across true and estimated channel
quality inputs. Both methods returned identical allocations,
satisfied the energy budget and bit limits, and preserved
the input arrays.

Next: add runtime measurements and save experiment results.

##6
Added checks on generated channels with 64, 256 and 1024 tones.
For each size, used five development seeds and tested both true
and estimated channel information.

All 30 comparisons passed. The checks covered allocation agreement,
energy feasibility, output shape, integer bit limits, finite values
and unchanged inputs.

Added a timing script with a warm-up and six repeated runs.
The execution order alternates between scan and heap.
Timing includes initialization and allocation, but excludes data
generation, checks and file output.

Saved individual measurements to results/development_timing.csv.
These are development cases, not the final test set.

Next: inspect timing results and prepare the final experiment settings.

