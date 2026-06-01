# 🧬 DP Optimizations

> *"When O(n²) DP is too slow, these techniques cut it to O(n log n) or O(n)."*

These are elite-CP techniques (Level 6-7). Each turns a specific DP transition structure into something faster.

---

## I. CONVEX HULL TRICK (CHT) ⭐
**When**: `dp[i] = min/max over j of (m[j]·x[i] + b[j])` — transitions are **linear functions** evaluated at a query point.

**Idea**: each j contributes a line `y = m[j]·x + b[j]`. The optimum at x[i] lies on the **lower (or upper) envelope** of these lines. Maintain the envelope; query in O(log n) (binary search) or O(1) (if queries/slopes are monotonic).

**Result**: O(n²) → O(n log n) or O(n).

**Generalization**: **Li Chao Tree** handles arbitrary insertion/query order in O(log) per op.

---

## II. DIVIDE & CONQUER DP ⭐
**When**: `dp[i][j] = min over k of (dp[i-1][k] + cost(k, j))` AND the optimal split `opt(i, j)` is **monotonic** in j (opt(i,j) ≤ opt(i,j+1)).

**Idea**: recursively compute a row; for the middle column, find its optimum, which bounds the optimum range for the halves.

**Result**: O(k·n²) → **O(k·n log n)**.

---

## III. KNUTH'S OPTIMIZATION ⭐
**When**: `dp[i][j] = min over k in (i,j) of (dp[i][k] + dp[k][j]) + cost(i,j)` AND cost satisfies the **quadrangle inequality** + monotonicity → `opt(i,j-1) ≤ opt(i,j) ≤ opt(i+1,j)`.

**Idea**: restrict the k-search to the narrow range between neighboring optima.

**Result**: O(n³) → **O(n²)**.

**Applies to**: optimal BST, some merge/partition problems.

---

## IV. ALIENS TRICK (Lagrangian Relaxation) ⭐
**When**: "do exactly k operations/partitions" AND the cost as a function of k is **convex**.

**Idea**: drop the "exactly k" constraint; add a penalty λ per operation. Solve the unconstrained (easier, often O(n) or O(n log n)) problem; **binary search λ** until the optimal solution uses exactly k operations.

**Result**: removes a factor of k. (Named after IOI 2016 "Aliens". See [`../15-CASE-STUDIES-LEGENDARY/04-IOI-Aliens-and-Beyond.md`](../15-CASE-STUDIES-LEGENDARY/04-IOI-Aliens-and-Beyond.md).)

---

## V. MONOTONIC QUEUE / DEQUE OPTIMIZATION ⭐
**When**: `dp[i] = min/max over j in [i-k, i-1] of dp[j] + f(i,j)` where the window is a sliding range.

**Idea**: maintain a monotonic deque of candidate j's; the front is always the optimum for the current window.

**Result**: O(n·k) → **O(n)**.

**Example**: Constrained Subsequence Sum (LC 1425), sliding-window max DP, bounded knapsack.

---

## VI. PREFIX-SUM / DATA-STRUCTURE OPTIMIZATION
**When**: the transition sums or takes max/min over a range of previous states.
- **Prefix sums** for range-sum transitions → O(1) per transition.
- **Segment tree / BIT** for range-max or range-update transitions → O(log n) per transition.
- **Example**: LIS in O(n log n) via segment tree on values; counting DP with prefix sums.

---

## VII. THE DECISION GUIDE
| Transition form | Optimization |
|-----------------|--------------|
| linear in query point (m·x+b) | Convex Hull Trick / Li Chao |
| dp[i-1][k] + cost(k,j), opt monotone | Divide & Conquer DP |
| dp[i][k]+dp[k][j], quadrangle ineq | Knuth's |
| "exactly k", convex in k | Aliens trick |
| sliding window min/max | Monotonic deque |
| range sum/max over prev states | prefix sums / segment tree |

---

## VIII. COMPLEXITY GAINS
- CHT: O(n²) → O(n log n) / O(n)
- D&C DP: O(kn²) → O(kn log n)
- Knuth: O(n³) → O(n²)
- Aliens: removes the k factor
- Monotonic deque: O(nk) → O(n)

---

## IX. PROBLEMS
- Constrained Subsequence Sum (LC 1425) — monotonic deque
- Frog Jump style with CHT (CF)
- IOI "Aliens" — Aliens trick
- Optimal BST — Knuth
- CF problems tagged "dp" + "data structures" / "divide and conquer"

---

## X. NOTE
These are advanced. First master plain DP (state + transition). Reach for optimizations only when constraints force sub-O(n²). Recognize the transition STRUCTURE to pick the right tool.

---

**→ Next:** [`16-SOS-DP.md`](./16-SOS-DP.md)
