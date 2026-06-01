# 📚 Legendary Patterns — Compendium of Famous Problems

> Famous problems from ICPC, IOI, Codeforces, and FAANG, dissected via:
> **Problem → Brute → Better → Optimal → Why → Complexity → Mental Model → Pattern.**

---

## 1. THE TWO SUM (FAANG entry-level legend)
- **Problem**: find two indices summing to target.
- **Brute**: O(n²) all pairs.
- **Optimal**: hash map of value→index, O(n).
- **Mental model**: "have I seen the complement?" → hash.
- **Pattern**: complement search.

## 2. MAXIMUM SUBARRAY / KADANE (the DP gateway)
- **Problem**: max sum contiguous subarray.
- **Brute**: O(n²) all subarrays.
- **Optimal**: dp[i] = max(a[i], dp[i-1]+a[i]), O(n).
- **Mental model**: "extend or restart."
- **Pattern**: 1D DP.

## 3. LARGEST RECTANGLE IN HISTOGRAM (the monotonic stack legend)
- **Problem**: max area rectangle in histogram.
- **Brute**: O(n²) expand each bar.
- **Optimal**: monotonic stack, O(n).
- **Why**: each bar's left/right smaller boundaries found in amortized O(1).
- **Pattern**: monotonic stack.

## 4. MEDIAN OF TWO SORTED ARRAYS (the binary search legend)
- **Problem**: median of two sorted arrays.
- **Brute**: merge, O(n+m).
- **Optimal**: binary search on partition, O(log min(n,m)).
- **Why**: find partition where left halves ≤ right halves.
- **Pattern**: binary search on a clever quantity.

## 5. THE SKYLINE PROBLEM (the sweep line legend)
- **Problem**: building outlines → skyline keypoints.
- **Brute**: O(n²) per x-coordinate.
- **Optimal**: sweep + max-heap, O(n log n).
- **Pattern**: sweep line + heap.

## 6. WORD LADDER (the BFS legend)
- **Problem**: shortest transformation chain between words.
- **Brute**: DFS all paths (exponential).
- **Optimal**: BFS on word graph, O(N·L²·26).
- **Mental model**: words = vertices, 1-letter edits = edges.
- **Pattern**: BFS shortest path on implicit graph.

## 7. BURST BALLOONS (the interval DP legend)
- **Problem**: max coins bursting balloons.
- **Brute**: O(n!) all orders.
- **Optimal**: interval DP, "last balloon to burst," O(n³).
- **Mental model**: reverse the perspective — think LAST, not first.
- **Pattern**: interval DP.

## 8. TRAPPING RAIN WATER (the two-pointer legend)
- **Problem**: water trapped between bars.
- **Brute**: O(n²) for each bar.
- **Optimal**: two pointers, O(n), O(1) space.
- **Mental model**: water at i = min(maxLeft, maxRight) − height[i].
- **Pattern**: two pointers with running maxima.

## 9. LRU CACHE (the design legend)
- **Problem**: O(1) get/put with LRU eviction.
- **Optimal**: HashMap + Doubly Linked List.
- **Mental model**: hash for lookup, DLL for ordering.
- **Pattern**: composite data structure design.

## 10. EDIT DISTANCE (the 2D DP legend)
- **Problem**: min edits to transform A → B.
- **Brute**: O(3^(n+m)) recursion.
- **Optimal**: dp[i][j], O(nm).
- **Pattern**: 2D string DP.

## 11. N-QUEENS (the backtracking legend)
- **Problem**: place n non-attacking queens.
- **Optimal**: backtracking with column/diagonal pruning.
- **Pattern**: backtracking with constraint propagation.

## 12. DIJKSTRA ON A GRID (the shortest-path legend)
- Used in countless problems (path with min effort, swim in water).
- **Pattern**: Dijkstra on implicit grid graph.

## 13. SLIDING WINDOW MAXIMUM (the monotonic deque legend)
- **Problem**: max in each window of size k.
- **Brute**: O(nk).
- **Optimal**: monotonic deque, O(n).
- **Pattern**: monotonic deque.

## 14. TSP (the bitmask DP legend)
- **Problem**: shortest tour visiting all cities.
- **Brute**: O(n!).
- **Optimal**: Held-Karp bitmask DP, O(2ⁿ·n²).
- **Pattern**: bitmask DP.

## 15. MO'S ALGORITHM PROBLEMS (the offline-query legend)
- **Problem**: many range queries (distinct count, etc.).
- **Optimal**: sort queries cleverly, O((n+q)√n).
- **Pattern**: offline query reordering.

---

## THE META-LESSONS

Across all legends:
1. **Brute force always exists** — it's the baseline.
2. **The leap to optimal is ONE observation** — find it.
3. **Reverse perspective** often helps (burst balloons, LAST not FIRST).
4. **The right data structure makes it trivial** (LRU, skyline).
5. **Implicit graphs** are everywhere (word ladder, grids).
6. **Monotonicity → binary search or monotonic stack/deque.**
7. **Overlapping subproblems → DP.**

Study these 15. They are the archetypes. Most problems are variations.

---

## RESEARCH-LEVEL LEGENDS (for the ambitious)
- **AKS Primality** (2002) — primality in deterministic polynomial time
- **Babai's Graph Isomorphism** (2016) — quasipolynomial
- **Chen et al. Max Flow** (2022) — almost-linear time
- **Strassen** (1969) — sub-cubic matrix multiplication
- **PCP Theorem** — hardness of approximation

These reshaped the field. Study them at Level 9-10.

---

**→ Back to:** [`00-Index.md`](./00-Index.md) | [`../14-ALGORITHM-DESIGN-SCIENCE/00-Index.md`](../14-ALGORITHM-DESIGN-SCIENCE/00-Index.md)
