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

##7
Set the main experiment sizes to 64, 256 and 1024 tones,
with 20 independent channels per size and 10 timing repeats.

Reserved seeds starting at 1000 for final testing.
The main comparison will use paired runtime differences,
while checking allocation agreement and energy feasibility.

##8
Updated the benchmark to read experiment settings from JSON.
The smoke run completed and saved eight timing records.
Both methods produced identical allocations and passed
the energy-budget checks.

##9
Completed the benchmark at 64, 256 and 1024 tones using
20 channels per size, true and estimated information,
and 10 timing repeats. All checks passed.

Saved 2400 records to results/final_timing.csv.
Next: analyse runtime differences and plot results.

##10
Summarized the final timing results using the median of
10 repeats for each method on each channel.

Calculated paired runtime differences across 20 channels
per size and condition. Estimated 95% bootstrap intervals
using 10000 resamples of the channel-level differences.

The heap method had lower mean runtime in all six groups.

##11
Ran the low-budget stress test on the same channels as the main benchmark.
Reduced the energy budget per subcarrier from 1.0 to 0.001.

The runtime differences were close to zero under the low budget for both
true and estimated channel information.

##12
Measured heap construction separately on the main benchmark channels.
The measurement includes creating the initial cost list and calling heapify.
Mean setup time increased from about 0.007 ms for 64 subcarriers to
about 0.113 ms for 1024 subcarriers.