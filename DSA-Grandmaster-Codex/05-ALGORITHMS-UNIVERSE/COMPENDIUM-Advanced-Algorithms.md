# ⚙️ Advanced Algorithm Paradigms Compendium

> Compact reference for the rest of the algorithms universe.

---

## 06 — BRANCH AND BOUND

### Concept
Backtracking + bounds. At each node of the search tree, compute a **lower bound** (for minimization) on what's achievable. If lower bound ≥ best found, prune.

### Use cases
- TSP (exact)
- Integer programming
- 0/1 Knapsack (when DP space is too big)
- Job assignment

### Distinction from backtracking
- **Backtracking**: prunes only by validity constraints
- **Branch & bound**: prunes by *bounds* on objective

---

## 07 — TWO POINTERS & SLIDING WINDOW

### Two pointers (opposite direction)
For sorted arrays / palindrome / pair sum:
```
l = 0; r = n - 1;
while (l < r) {
    if (condition) { record(l, r); }
    if (...) l++; else r--;
}
```

### Two pointers (same direction = sliding window)
```
l = 0;
for (r = 0; r < n; r++) {
    add(a[r]);
    while (window_invalid()) remove(a[l++]);
    answer = max(answer, r - l + 1);  // or sum, count, etc.
}
```

### Patterns
- Fixed-size window (e.g., max sum of k elements)
- Variable window with at-most-k-distinct constraint
- Window with sum/product constraint
- Pair finding in sorted array

### Top problems
LC 3, 11, 15, 16, 26, 27, 76, 121, 159, 209, 239, 340, 424, 438, 567, 658, 713, 904, 992, 1004, 1248, 1358, 1493

---

## 08 — BIT MANIPULATION

See [`../02-PROGRAMMING-FOUNDATIONS/`](../02-PROGRAMMING-FOUNDATIONS/) for foundations. Key tricks:

| Trick                          | Code                              |
|--------------------------------|-----------------------------------|
| Check bit i set                | `n & (1 << i)`                    |
| Set bit i                      | `n \|= (1 << i)`                  |
| Clear bit i                    | `n &= ~(1 << i)`                  |
| Toggle bit i                   | `n ^= (1 << i)`                   |
| Count set bits                 | `__builtin_popcount(n)`           |
| Lowest set bit                 | `n & -n`                          |
| Clear lowest set bit           | `n & (n-1)`                       |
| Power of 2 check               | `n && !(n & (n-1))`               |
| Iterate subsets of mask        | `for (int s = mask; s; s = (s-1)&mask)` |
| Highest bit                    | `__builtin_clz(n)` / `__lg(n)`    |
| XOR cancellation               | `a ^ a = 0`, `a ^ 0 = a`          |

### Top problems
- Single number I, II, III
- Counting bits
- Power of two/three/four
- Reverse bits
- Subsets via bitmask
- Maximum XOR of two numbers (with binary trie)
- Sum of two integers without `+`

---

## 09 — RANDOMIZED ALGORITHMS

### Two flavors
- **Las Vegas**: always correct, expected runtime random (e.g., randomized quicksort)
- **Monte Carlo**: bounded runtime, may give wrong answer with small probability (e.g., Miller-Rabin primality)

### Famous randomized algorithms
- Randomized quicksort (avoids worst case)
- Skip list (probabilistic balancing)
- Treap (probabilistic balancing)
- Miller-Rabin primality (Monte Carlo)
- Randomized incremental construction (computational geometry)
- Karger's min-cut (Monte Carlo)
- Reservoir sampling
- Bloom filter

### When to use
- Adversarial worst-case is unacceptable but average-case is fine
- Simpler code than deterministic equivalent
- Need approximate / sampling-based solution

---

## 10 — APPROXIMATION ALGORITHMS

When exact is NP-hard, settle for "close to optimal."

### Approximation ratio
For minimization: A(input) / OPT(input) ≤ ρ where ρ ≥ 1.

### Famous results
- **Vertex cover**: 2-approximation (greedy edge picking)
- **TSP (metric)**: 1.5-approx (Christofides)
- **Set cover**: O(log n)-approximation (greedy)
- **Knapsack (FPTAS)**: (1+ε)-approximation in poly(n, 1/ε)
- **Max-cut**: 0.878 (Goemans-Williamson via SDP)

### Use case
Production where exact solution is computationally infeasible.

---

## 11 — ONLINE ALGORITHMS

Make decisions **without knowing future input**.

### Competitive ratio
A's cost / OPT's cost (with hindsight) ≤ c.

### Famous online problems
- Paging (LRU, FIFO, etc.; LRU is k-competitive)
- List update problem (move-to-front, transpose)
- Online bipartite matching (Karp-Vazirani-Vazirani)
- Ski rental (rent vs buy: 2-competitive)
- Bin packing online

---

## 12 — STREAMING ALGORITHMS

Single (or few) pass over data; bounded memory (typically polylog n).

### Famous streaming
- **Reservoir sampling**: uniform random sample
- **Heavy hitters** (Misra-Gries, Count-Min)
- **HyperLogLog** (cardinality)
- **Frequency moments** (AMS sketch)
- **Sliding window aggregates**
- **Bloom filter** for membership

### Use case
Big data: terabytes/petabytes through a system; can't store all.

---

## 13 — PARALLEL ALGORITHMS

Multi-core / SIMD / GPU.

### Key concepts
- **Work-span model**: T_p = work + span (for p processors)
- **Parallel for** (data parallelism)
- **Parallel reduce** (sum, min, max in O(log n) span)
- **Parallel scan/prefix** (Hillis-Steele or Blelloch)
- **Parallel sort** (bitonic, sample sort, radix)

### Where used
- Linear algebra (BLAS, LAPACK)
- ML training (batch parallelism)
- Real-time graphics (GPU)

---

## 14 — DISTRIBUTED ALGORITHMS

Multiple machines, network communication.

### Famous distributed algorithms
- **Paxos**: consensus
- **Raft**: simpler consensus (Etcd, Consul)
- **PBFT** / **PoW** / **PoS** (Byzantine fault tolerance)
- **Gossip** (epidemic protocols, eventually consistent)
- **MapReduce** (parallel batch processing)
- **Vector clocks** / **Lamport clocks** (logical time)
- **Chandy-Lamport** (snapshots)
- **2PC, 3PC** (transactions)

For Level 8+. See [`../01-LEVELS-PROGRESSION/Level-08-Algorithm-Engineering.md`](../01-LEVELS-PROGRESSION/Level-08-Algorithm-Engineering.md).

---

## 15 — SWEEP LINE

### Concept
Imagine a vertical line sweeping left-to-right across the plane. At each event (point), update a data structure. Compute aggregates.

### Use cases
- Skyline problem (LC 218)
- Closest pair of points
- Line segment intersections (Bentley-Ottmann)
- Rectangle union area
- Largest empty rectangle

### Top problems
1. The skyline problem
2. Number of intersections of horizontal and vertical lines
3. Rectangle area II (LC 850)
4. Maximum number of overlapping intervals
5. Falling squares

---

## 16 — COORDINATE COMPRESSION

### Concept
When values can be up to 10⁹ but there are only n distinct values, map them to indices 0..n-1.

```cpp
vector<int> values = ...;  // original
sort(values.begin(), values.end());
values.erase(unique(values.begin(), values.end()), values.end());
// Now use lower_bound(values.begin(), values.end(), x) - values.begin() as the compressed index
```

### Use cases
- Segment tree on values (avoid 10⁹ size)
- Counting distinct values
- Range queries on sparse data

---

## 17 — MEET IN THE MIDDLE

### Concept
For n=40 problems where 2ⁿ is too big, split into halves: 2^(n/2) = ~10⁶ each. Enumerate each half; combine.

### Use cases
- Subset sum with n=40
- 4-sum
- Closest subset sum
- Hard knapsack variants

### Template
```cpp
// Generate all subset sums of left half: A
// Generate all subset sums of right half: B
// Sort B
// For each a in A, find target - a in B (binary search or two pointers)
```

---

## 18 — SQUARE ROOT DECOMPOSITION

### Concept
Break array into blocks of √n. Operations:
- Within-block: O(√n)
- Across blocks: O(√n) blocks each O(1) → O(√n)

### Use cases
- Range queries with updates (alternative to segtree)
- Heavy/light vertices in graphs (degree threshold √m)
- Mo's algorithm (offline range queries)

---

## 19 — MO'S ALGORITHM

### Concept
**Offline** range queries. Sort queries cleverly; transition from query to query in O(1) amortized.

### Setup
- Sort queries: by `(l / √n, r)` (or Hilbert curve order for better practice)
- Maintain answer for current [l, r] window
- Move pointers; recompute incrementally

### Complexity
O((N + Q) × √N) per query; amortized.

### Use cases
- Distinct elements in [l, r]
- Number of pairs (i, j) with a[i] = a[j] in [l, r]
- Mode of [l, r]

### Variants
- Mo's on trees (with Euler tour)
- Mo's with updates (3D Mo's)

---

## 20 — HEAVY-LIGHT DECOMPOSITION (HLD)

### Concept
Decompose tree into "chains" such that any root-to-leaf path crosses ≤ O(log n) chains. For each chain, build a segment tree.

### Operations
- Path query / path update on tree: O(log² n)
- Subtree query / subtree update: O(log n) (with Euler-tour-based ordering)

### Use cases
- Path sum / max / xor on tree with updates
- Path-vs-subtree queries
- Combined with Lazy Segtree, supports almost any tree operation

---

## 21 — CENTROID DECOMPOSITION

### Concept
Find tree centroid (node whose removal leaves subtrees of size ≤ n/2). Recurse. Decomposition has O(log n) depth.

### Use cases
- Path queries on trees with updates
- "Distance to set X" type queries
- Counting paths with property

### Memory
O(n log n) — each node appears in O(log n) levels.

---

## 22 — ALGORITHM PARADIGMS — MASTER INDEX

### Quick lookup

| Paradigm                     | When to use                                     |
|------------------------------|-------------------------------------------------|
| Brute force                  | Tiny n, baseline                                |
| Divide & conquer             | Independent subproblems                         |
| DP                           | Overlapping subproblems                         |
| Greedy                       | Greedy choice property + optimal substructure   |
| Backtracking                 | Enumerate solutions with constraints            |
| Branch & bound               | Optimization with bounds                        |
| Randomization                | Avoid worst case / probabilistic                |
| Approximation                | NP-hard, need close-to-optimal                  |
| Two pointers / sliding window| Sequence problems with monotonic windows        |
| Bit manipulation             | Subsets, parity, XOR, integer tricks            |
| BFS / DFS                    | Graph traversal                                 |
| Sweep line                   | 2D plane, intervals                             |
| Coordinate compression       | Big values, sparse                              |
| Meet in the middle           | n ≈ 40                                          |
| Square root decomposition    | n ≈ 10⁵, range queries                          |
| Mo's                         | Offline range queries                           |
| HLD / Centroid               | Tree path queries                               |

---

**→ Next universe:** [`../06-DYNAMIC-PROGRAMMING-UNIVERSE/00-Index.md`](../06-DYNAMIC-PROGRAMMING-UNIVERSE/00-Index.md)
