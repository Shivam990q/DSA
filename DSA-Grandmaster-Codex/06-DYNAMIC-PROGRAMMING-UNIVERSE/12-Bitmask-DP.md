# 🧬 Bitmask DP

> *"When n ≤ 20, a subset becomes an integer, and the integer becomes a DP state."*

---

## I. THE IDEA
Represent a subset of n elements as an n-bit integer (bit i set ⟺ element i in the subset). With n ≤ ~20, there are 2ⁿ ≤ ~10⁶ subsets — small enough to be a DP dimension.

---

## II. BIT OPERATIONS CHEAT-SHEET
```
mask & (1<<i)        // is element i in the set?
mask | (1<<i)        // add element i
mask & ~(1<<i)       // remove element i
mask ^ (1<<i)        // toggle element i
__builtin_popcount(mask)   // count set bits
mask == (1<<n) - 1   // full set?
// iterate submasks of mask:
for (int s = mask; s; s = (s-1) & mask) { ... }   // O(3^n) total over all masks
```

---

## III. TRAVELING SALESMAN PROBLEM (TSP) — the flagship ⭐
`dp[mask][i]` = min cost to start at 0, visit exactly the cities in `mask`, ending at city i.
```cpp
dp[1][0] = 0;
for (int mask = 1; mask < (1<<n); mask++)
  for (int i = 0; i < n; i++) if (mask & (1<<i))
    for (int j = 0; j < n; j++) if (!(mask & (1<<j)))
        dp[mask|(1<<j)][j] = min(dp[mask|(1<<j)][j], dp[mask][i] + dist[i][j]);
// answer: min over i of dp[full][i] + dist[i][0]
```
O(2ⁿ · n²). Feasible for n ≤ ~20.

---

## IV. CLASSIC BITMASK DPs
- **Assignment problem** (n tasks to n people, min cost): `dp[mask]` = min cost to assign the first popcount(mask) people to the tasks in mask. O(2ⁿ · n).
- **Partition into K equal-sum subsets (LC 698)**: `dp[mask]` over used elements.
- **Number of ways to wear hats (LC 1434)**: iterate hats outer, masks of people inner.
- **Shortest Superstring (LC 943)**: TSP-style over overlaps.
- **Minimum incompatibility (LC 1681)**, **Maximum students taking exam (LC 1349)**, **Smallest Sufficient Team (LC 1125)**.
- **Hamiltonian path/cycle counting**.

---

## V. PROFILE / BROKEN-PROFILE DP (bitmask over a frontier)
For tiling/grid problems (e.g., tile a board with dominoes): the mask encodes the "profile" of filled cells at the boundary between processed and unprocessed columns. See [`17-Profile-DP.md`](./17-Profile-DP.md).

---

## VI. SUBSET-SUM OVER SUBMASKS (SOS DP)
Compute, for each mask, an aggregate over all its submasks in O(n·2ⁿ) instead of O(3ⁿ). See [`16-SOS-DP.md`](./16-SOS-DP.md).

---

## VII. CONSTRAINT RECOGNITION ⭐
The tell-tale sign of bitmask DP:
- **n ≤ 20** (or k ≤ 20 for some small parameter)
- "subset", "assign", "visit all", "cover all", "each used once"

If you see small n + "subsets/permutations of everything," think bitmask DP.

---

## VIII. COMPLEXITY
- TSP-style: O(2ⁿ · n²)
- Assignment / simple subset DP: O(2ⁿ · n)
- Submask enumeration: O(3ⁿ)

Memory O(2ⁿ · n) can be the binding constraint (n ≤ ~20-22).

---

## IX. PROBLEMS
- TSP ([CSES](https://cses.fi/problemset/) "Hamiltonian Flights", classic)
- Partition to K Equal Sum Subsets (698)
- Number of Ways to Wear Different Hats (1434)
- Shortest Superstring (943), Smallest Sufficient Team (1125)
- Maximum Students Taking Exam (1349), Minimum Incompatibility (1681)
- Beautiful Arrangement (526), Campus Bikes II (1066)

---

**→ Next:** [`13-Digit-DP.md`](./13-Digit-DP.md)
