# 🧬 DP Cheatsheet — Recognition & Recall

> *"The grandmaster recognizes the DP type in 30 seconds. Here's the lookup table."*

---

## I. THE RECOGNITION TABLE
| You see...                                  | DP type | File |
|---------------------------------------------|---------|------|
| "ways to climb / reach", single sequence    | 1D DP | [`02-1D-DP.md`](./02-1D-DP.md) |
| grid paths, two coords                       | 2D/Grid | [`03-2D-DP-Grids.md`](./03-2D-DP-Grids.md) |
| "pick items under capacity/budget"           | Knapsack | [`04-Knapsack-Family.md`](./04-Knapsack-Family.md) |
| "longest increasing subsequence"             | LIS | [`05-LIS-Family.md`](./05-LIS-Family.md) |
| two strings/sequences                        | LCS | [`06-LCS-Family.md`](./06-LCS-Family.md) |
| "min edits to transform"                     | Edit Distance | [`07-Edit-Distance-Family.md`](./07-Edit-Distance-Family.md) |
| buy/sell with states                         | Stocks (state machine) | [`08-Stocks-DP.md`](./08-Stocks-DP.md) |
| "on range (i,j), split/last element"          | Interval DP | [`09-Interval-DP.md`](./09-Interval-DP.md) |
| tree, subtree aggregates                     | Tree DP | [`10-Tree-DP.md`](./10-Tree-DP.md) |
| DAG, "longest/count paths"                   | DAG DP | [`11-Graph-DP-DAG.md`](./11-Graph-DP-DAG.md) |
| n ≤ 20, "subsets/visit all"                  | Bitmask DP | [`12-Bitmask-DP.md`](./12-Bitmask-DP.md) |
| "count numbers in [L,R] with property"        | Digit DP | [`13-Digit-DP.md`](./13-Digit-DP.md) |
| "expected value / probability"               | Prob/Exp DP | [`14-Probability-Expected-DP.md`](./14-Probability-Expected-DP.md) |
| O(n²) DP too slow, linear transitions         | DP optimizations | [`15-DP-Optimizations.md`](./15-DP-Optimizations.md) |
| "aggregate over submasks"                     | SOS DP | [`16-SOS-DP.md`](./16-SOS-DP.md) |
| "tile/fill an n×m grid", small m              | Profile DP | [`17-Profile-DP.md`](./17-Profile-DP.md) |
| "best dp[j] over a range"                     | DP + data structure | [`18-DP-with-Data-Structures.md`](./18-DP-with-Data-Structures.md) |

---

## II. THE 5-STEP FRAMEWORK (always)
1. **State**: what does `dp[...]` mean? (one sentence)
2. **Transition**: how does it depend on smaller states?
3. **Base case**: smallest subproblem's answer.
4. **Order**: fill so dependencies are ready (or memoize top-down).
5. **Answer**: which cell holds it?

(Full framework: [`01-DP-Foundations.md`](./01-DP-Foundations.md))

---

## III. CONSTRAINT → DP TYPE HINTS
- n ≤ 20 → bitmask DP
- n ≤ 500 → O(n³) interval DP possible
- n ≤ 5000 → O(n²) DP
- n ≤ 10⁵-10⁶ → O(n log n) DP (need optimization/data structure)
- L, R up to 10¹⁸, digit property → digit DP

---

## IV. COUNTING vs OPTIMIZING vs FEASIBILITY
- max/min → `dp = best(...)`
- count ways → `dp += ...`
- can/can't → `dp = dp || ...`
Same skeleton, swap the combine operation.

---

## V. SPACE OPTIMIZATION REMINDERS
- Only last row/few states used → rolling array (O(n)→O(1) dimensions).
- 2D depending on prev row → two rows or in-place (careful with direction).
- Knapsack 1D: 0/1 iterates capacity DOWN, unbounded iterates UP.

---

## VI. COMMON BUGS
- Wrong loop order (knapsack direction, interval by length)
- Forgetting base cases / first row & column
- Off-by-one in state bounds
- Memoizing tight states in digit DP (don't!)
- Integer overflow in counting (use long long / mod)
- Order matters vs not (combination vs permutation loops)

---

## VII. THE 50-PROBLEM CANON
See [`COMPENDIUM-Classical-DP.md`](./COMPENDIUM-Classical-DP.md) §20 for the full curated list, and the **[AtCoder](https://atcoder.jp) [Educational DP Contest](https://atcoder.jp/contests/dp) (EDPC)** — 26 problems (A-Z) covering every foundational pattern.

---

**→ Next:** [`20-50-Classic-DP-Problems.md`](./20-50-Classic-DP-Problems.md)
