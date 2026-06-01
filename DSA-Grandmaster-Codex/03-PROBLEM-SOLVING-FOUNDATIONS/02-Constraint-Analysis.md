# 🔍 Constraint Analysis — The Whisper of Algorithms

> *"The constraints don't limit you. They guide you."*

Constraints are the **first-class citizens** of every problem. They're rarely arbitrary; they encode the problem-setter's intended algorithm class.

---

## I. THE MASTER TABLE

| n            | Time budget per operation | Suggested complexity            | Typical algorithms                      |
|--------------|--------------------------|----------------------------------|------------------------------------------|
| n ≤ 10       | n!, n^n                   | Anything goes                   | Brute, full permutation, bitmask         |
| n ≤ 12       | 12! ≈ 5×10⁸              | O(n!)                            | Permutations                             |
| n ≤ 18-20    | 2²⁰ ≈ 10⁶                | O(2ⁿ × n)                        | Bitmask DP                               |
| n ≤ 25       | 2²⁵ ≈ 3×10⁷              | O(2ⁿ) or O(2^(n/2)) MITM         | Subset enumeration, meet in middle       |
| n ≤ 50-100   |                          | O(n⁴)                            | DP with 4 dimensions                     |
| n ≤ 500      |                          | O(n³)                            | Floyd-Warshall, matrix chain DP          |
| n ≤ 5000     |                          | O(n²)                            | DP, all-pair distances                   |
| n ≤ 10⁵      |                          | O(n √n) or O(n log² n)           | Mo's, heavy-light, square root           |
| n ≤ 10⁶      |                          | O(n log n)                       | Sort, segtree, BIT, KMP                  |
| n ≤ 10⁷      |                          | O(n)                             | Linear sieve, two pointers, prefix sums  |
| n ≤ 10⁹      |                          | O(log n) or O(√n)                | Binary search, math, primality testing   |
| n ≤ 10¹⁸     |                          | O(1) or O(log n)                 | Closed forms, log-exp, matrix exp        |

---

## II. RULE OF THUMB: 10⁸ OPERATIONS / SECOND

A modern CPU runs ~10⁸ simple operations per second of competitive programming code.

For 1-second TL: budget = 10⁸ ops.
For 2-second TL: budget = 2×10⁸ ops.

**Note**: this is for tight loops. Hash map operations are ~10× slower per op (memory access). String operations vary. Don't over-trust this number for complex code.

---

## III. WHEN MULTIPLE PARAMETERS

When you have n, m, k, q, etc., consider their *product or sum*:

> n ≤ 10⁵, q ≤ 10⁵ → can do O((n+q) log n) — segtree per query.
> n ≤ 1000, m ≤ 1000 → can do O(nm log(nm)) — segtree on grid.
> n ≤ 100, m ≤ 100 → can do O(n² m²) — naive.

> n ≤ 5000, k ≤ 50 → can do O(n × k) — knapsack-like DP.

The *product* of bounds tells you the work budget.

---

## IV. SPACE CONSTRAINTS

| Memory limit | What you can afford                     |
|--------------|-----------------------------------------|
| 256 MB       | ~6×10⁷ ints, ~3×10⁷ long longs          |
| 64 MB        | ~1.5×10⁷ ints                           |

For n=10⁵, you can have an O(n²) bool table (10¹⁰... wait, that's 10 GB. NO.)

Actually n=10⁵ means O(n) is fine (10⁵ ints = 400 KB), O(n log n) might be tight, O(n²) is too much (10¹⁰ ints = 40 GB).

**Trick**: when DP state is too big in memory, look for "rolling" reductions (e.g., 2D → 1D when only previous row matters).

---

## V. VALUE RANGE CONSTRAINTS

Beyond size, value ranges matter:

- **`a[i] ≤ 10⁹`**: fits in int. No overflow on individual values.
- **`a[i] ≤ 10¹⁸`**: needs long long.
- **Sum can overflow**: even int values can sum to long long territory. Use `long long` for sums.
- **`a[i] ≥ 0`**: enables Dijkstra's, certain DP optimizations.
- **`a[i]` can be negative**: forces Bellman-Ford for shortest paths, careful with prefix sums.
- **`distinct`**: simplifies hashing, may enable hash sets.
- **`sorted`**: enables binary search, two pointers.

---

## VI. SPECIAL CONSTRAINT PATTERNS

### Pattern 1: "n ≤ 20" → Bitmask
Subsets of n=20 are 10⁶, fits in bitmask DP.

### Pattern 2: "n ≤ 40" → Meet in the Middle
Split into halves of 20 each, enumerate each (2²⁰ = 10⁶), combine.

### Pattern 3: "n ≤ 5000" with O(n²) → DP table
Often interval DP, LCS, etc.

### Pattern 4: "n ≤ 10⁵ but k ≤ 20" → 2D DP with small k
States × transitions = 10⁵ × 20 × 20 = 4×10⁷, fine.

### Pattern 5: "Many test cases (T ≤ 10⁴)" with sum of n ≤ 10⁶
Total work across cases is bounded; can do O(sum n).

### Pattern 6: "Output may be large; print mod 10⁹+7"
Counting / combinatorial problem. Modular arithmetic.

### Pattern 7: "Coordinates up to 10⁹"
Coordinate compression to indices 0..n.

### Pattern 8: "Tree" with n ≤ 10⁵
Tree DP O(n) or LCA O(log n) per query — never O(n²)!

### Pattern 9: "Online queries" (must answer immediately)
Persistent structures, segment tree, treap.

### Pattern 10: "Offline queries" (can preprocess)
Sort queries, Mo's algorithm, sweep line.

---

## VII. THE CONSTRAINT-ALGORITHM REVERSE LOOKUP

Sometimes you know the algorithm class; check if constraints fit:

- BFS/DFS: O(V+E). Need V+E ≤ 10⁶ for 1s.
- Dijkstra: O((V+E) log V). Need (V+E) log V ≤ 10⁷.
- Floyd-Warshall: O(V³). Need V ≤ 500.
- Bellman-Ford: O(VE). Need VE ≤ 10⁸.
- Segment tree: O((N+Q) log N). Need (N+Q) log N ≤ 10⁷.
- Mo's: O((N+Q) √N). Need (N+Q) √N ≤ 10⁸.
- Bitmask DP: O(2ⁿ × n). Need n ≤ 22.

---

## VIII. EXERCISES

For each, identify the algorithm class:

1. n ≤ 18, m ≤ 18 (TSP-like) → ?
2. n ≤ 1000, q queries with sum query in range → ?
3. Find shortest path; n ≤ 10⁵, all weights = 1 → ?
4. Find longest increasing subsequence; n ≤ 10⁶ → ?
5. Find Kth smallest in range [l, r] for q queries; n, q ≤ 10⁵ → ?
6. n elements with values up to 10¹⁸, find any two summing to k → ?
7. Tree with n ≤ 10⁵, q LCA queries → ?
8. n × m grid, n,m ≤ 1000, count distinct islands → ?

(Sample answers: 1) Bitmask DP, 2) Segment tree / BIT, 3) BFS, 4) O(n log n) patience sort / segtree on values, 5) Persistent segment tree or Mo's offline, 6) Hash set / two pointers if sorted, 7) Binary lifting LCA, 8) DFS + canonical encoding)

---

## IX. THE FINAL TRUTH

> **"When you read 'n ≤ 10⁵' and feel nothing — you're not reading the problem.  
>  When you read 'n ≤ 20' and your bitmask alarm rings — you're reading the problem."**

---

**→ Next:** [`03-Observation-Extraction.md`](./03-Observation-Extraction.md)
