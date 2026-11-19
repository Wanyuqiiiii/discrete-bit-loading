Implemented the scan-based bit allocation method.

The two-subcarrier example returned [2, 1], using 2.5 energy
units under a budget of 3. The zero-budget check also passed.

Next: verify small cases using exhaustive enumeration.


Checked the scan method against exhaustive enumeration.
For three subcarriers with a cap of 3 bits each, all 64
allocations were examined at each of six energy budgets.
The scan method matched the optimal total bits in every case
and stayed within the energy budget and bit limits.

Next: implement the min-heap version.