# 🔬 How Algorithms Are Invented

> *"Knuth, Dijkstra, Tarjan — they did not memorize. They observed, abstracted, generalized, proved."*

---

## I. THE INVENTOR'S METHOD

The historical pattern of every famous algorithm:

### Step 1: A practical problem appears
- Dijkstra: shortest route between Dutch cities (1959)
- Cooley-Tukey: faster FFT for nuclear test detection (1965)
- KMP: efficient string matching for compilers (1977)

### Step 2: The naive solution is too slow
- Floyd-Warshall existed (1962). Dijkstra wanted faster for non-negative weights.
- O(n²) FFT existed. Cooley-Tukey wanted O(n log n).
- O(nm) string matching wanted O(n+m).

### Step 3: A key observation is made
- Dijkstra: closest unvisited node's distance is final (greedy choice)
- Cooley-Tukey: even/odd index decomposition gives recursion
- KMP: failure function captures backward shift info

### Step 4: The observation gets formalized
- Mathematical proof
- Pseudocode
- Complexity analysis

### Step 5: It's published, popularized, refined
- Generations of researchers improve constants, edge cases, generalizations

---

## II. THE FIVE WAYS TO INVENT ALGORITHMS

### 1. **Removing redundancy** in a brute force
> Two-sum O(n²) → noticing inner loop is searchable → hash map → O(n).

### 2. **Reformulating** the problem
> "Largest rectangle in histogram" rewritten as "for each bar, find boundary smaller bars" → monotonic stack.

### 3. **Composition** of existing algorithms
> Topological sort + DP → DAG longest path. Two existing tools combined.

### 4. **Generalization** of a special case
> Solve the problem for trees → generalize to general graphs. Solve for n=2 → induct.

### 5. **Reduction** to a known problem
> "Optimal scheduling" reduces to bipartite matching, which is solved.

---

## III. THE OBSERVATIONS THAT BIRTHED ALGORITHMS

### Floyd's cycle detection (tortoise-and-hare)
**Observation**: if there's a cycle, two pointers (one at speed 1, one at speed 2) will eventually meet inside the cycle.
**Why this matters**: O(1) extra space cycle detection.

### Quickselect
**Observation**: to find the kth element, we don't need to sort the whole array — only partition once and recurse into the relevant half.
**Insight**: Quicksort's partition step is more powerful than just sorting.

### KMP's failure function
**Observation**: when a mismatch occurs, the work done so far isn't wasted — it tells us where to continue.
**Insight**: the pattern's structure (its prefix-suffix overlaps) carries information.

### Union-Find with path compression
**Observation**: amortizing path compression across multiple finds gives near-O(1) per operation.
**Insight**: amortized analysis can reveal hidden efficiency.

### FFT (Cooley-Tukey)
**Observation**: a polynomial of degree 2n can be evaluated at n complex roots of unity using only n/2 multiplications + recursion.
**Insight**: divide-and-conquer + roots of unity = O(n log n).

### Manacher's algorithm
**Observation**: palindrome around center i tells you a lower bound on palindrome around mirror centers.
**Insight**: amortized linear time via reuse.

---

## IV. THE INVENTOR'S CHECKLIST

Before claiming "I invented an algorithm":
1. **Is it simpler than existing?** (Knuth: simplicity is gold)
2. **Is it faster than existing?** (asymptotic improvement?)
3. **Does it use less memory?**
4. **Does it solve a strictly more general problem?**
5. **Is it cleaner / easier to implement?**

If yes to ≥1: probably worth publishing.

---

## V. THE FORM OF AN ORIGINAL CONTRIBUTION

In a research paper:
1. Problem definition (precise)
2. Prior work (cite, contrast)
3. Main idea (the observation/trick)
4. Algorithm (pseudocode)
5. Correctness proof
6. Complexity analysis
7. Experiments / comparisons
8. Limitations / open questions

Even if you never publish, structure your thinking this way.

---

## VI. EXERCISES — INVENT MINI-ALGORITHMS

For each, design from scratch (don't look up):

### 1. Find majority element in O(n) time, O(1) space
*(Hint: the Boyer-Moore voting algorithm. Try inventing it.)*

### 2. Detect cycle in linked list with O(1) space
*(Hint: Floyd's tortoise-and-hare.)*

### 3. Find a duplicate in array of n+1 integers in [1, n], with O(1) space
*(Hint: treat array as a function; find cycle.)*

### 4. Compute exponentiation in O(log n)
*(Hint: binary exponentiation.)*

### 5. Stable random shuffle in O(n)
*(Hint: Fisher-Yates.)*

### 6. Find min sliding window in O(n)
*(Hint: monotonic deque.)*

### 7. Inverse-Ackermann time DSU operations
*(Hint: path compression + union by rank.)*

These problems have published, named algorithms. Try to invent them WITHOUT reference. The struggle is the practice.

---

## VII. THE GRANDMASTER'S DAILY HABIT

For 30 minutes a day:
1. Pick a problem you don't immediately know
2. Try to invent something — anything
3. Compare your idea with existing solutions
4. Note: did you converge? where did you diverge?

Over years, this trains the *inventor's mind*.

---

## VIII. RECOMMENDED READING

- **Knuth, *Selected Papers on Analysis of Algorithms***
- **Tarjan, *Data Structures and Network Algorithms*** ⭐
- **Erickson, *Algorithms*** (free) — proofs everywhere
- **Williamson & Shmoys, *Approximation Algorithms***
- **The Art of Algorithm Design** (Manber)

---

**→ Next:** [`02-Algorithmic-Reduction.md`](./02-Algorithmic-Reduction.md)
