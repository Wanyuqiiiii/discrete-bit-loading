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
