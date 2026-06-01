# 🔬 Observation Extraction — Finding the Hidden Insight

> *"Every hard problem hides one observation. Find it, and the problem dissolves."*

---

## I. WHAT IS AN OBSERVATION?

An **observation** is a non-obvious property of the problem that, once seen, dramatically simplifies the solution. Observations are the soul of competitive programming.

### Examples
- *"The optimal answer is always achieved when the array is sorted."*
- *"Two adjacent elements are swapped at most once."*
- *"The answer is monotonic in k."*
- *"The structure is bipartite."*
- *"The answer can never exceed log n."*
- *"Every valid configuration corresponds to a permutation."*
- *"There's always an optimal solution where the first element is the smallest."*

---

## II. WHERE TO LOOK

### Look 1: **Small Cases**
Compute the answer for n=1, 2, 3, 4, 5. Find a pattern.

### Look 2: **Extremes**
What's the min answer? Max? When is it 0? When does it overflow?

### Look 3: **Symmetries**
Does swapping rows/columns preserve answer? Reversing? Negating?

### Look 4: **Invariants**
What stays the same under operations? (Parity, sum, product, max, etc.)

### Look 5: **Monotonicity**
Is the answer monotonic in some parameter? (Enables binary search.)

### Look 6: **Structure**
Is the input a tree? Forest? DAG? Bipartite? Sparse?

### Look 7: **Reduction**
Can this problem be transformed into a known one?

---

## III. SMALL-CASE EXPLORATION

When stuck, **compute by hand** for n=1..5.

> Problem: count number of binary strings of length n without "11" substring.
>
> n=1: "0", "1" → 2
> n=2: "00", "01", "10" (no "11") → 3
> n=3: "000", "001", "010", "100", "101" → 5
> n=4: ... → 8
> n=5: ... → 13
>
> Pattern: 2, 3, 5, 8, 13 — Fibonacci! → recurrence f(n) = f(n-1) + f(n-2).

**This is how 80% of constructive/observation problems are cracked.**

---

## IV. EXTREMES & EDGE INSIGHTS

> Problem: given array, find longest subarray with sum > 0.
>
> Insight from extreme: if all elements are positive, the answer is n.
> Insight from extreme: if all elements are negative, the answer is 0 (or 1 if any non-negative).
> Insight from extreme: a long subarray needs more positive than negative weight.
> → Use prefix sums; find min prefix to the left, look for difference > 0.

---

## V. THE INVARIANT HUNT

When operations are allowed (e.g., "swap adjacent," "increment a row," etc.), ask:

- What property of the state is **preserved** by each operation?
- What property **changes by a known amount** with each operation?

> Example: 8-puzzle. Operation: slide a tile. Invariant: parity of permutation + parity of empty's row distance from goal. Half of all configurations are reachable; half aren't.

> Example: array problem with operation "add to a, subtract from b." Invariant: a + b is constant. Therefore, must check sum at start equals sum at goal.

---

## VI. MONOTONICITY DISCOVERY

**Monotonicity** = the answer (or feasibility) doesn't reverse when a parameter increases.

> Example: "is it possible to ship all packages in d days with ship capacity c?"
> If c works, c+1 works. → Monotonic in c. → Binary search on c.

> Example: "longest subarray with sum ≤ k"?
> If a window of size w works (sum ≤ k starting at some i), does a window of size w-1 starting at the same i work? Not always. So not directly monotonic, but... if window grows, sum grows (positive elements). → Two pointers.

Monotonicity often hides in "feasibility predicates."

---

## VII. SYMMETRY EXPLOITATION

> Problem: count pairs (i, j) such that a[i] + a[j] = target.
> Symmetric in i, j. So count unordered pairs, multiply by 2 (or 1 if i=j case).

> Problem: 2D matrix transformation.
> Often row-column symmetric → reduce to 1D problem.

---

## VIII. STRUCTURE DISCOVERY

> Problem: given graph, partition into two sets minimizing some cost.
> Insight: if the graph is bipartite, the partition is forced.

> Problem: given numbers, queries about sum / xor / gcd in range.
> Insight: gcd has the structure of an idempotent monoid → sparse table works (O(1) queries after O(n log n) build).

---

## IX. THE OBSERVATION CHEAT-SHEET

Common observation types:

1. **The answer is always achievable with ≤ k operations** (k often log n or √n)
2. **The optimal sorts the input**
3. **The optimal is monotonic**
4. **The answer equals (formula) for some derived quantity**
5. **A greedy that picks the largest/smallest first works**
6. **The problem is a hidden BFS/DFS/MST/flow**
7. **Modulo arithmetic / parity argument cuts cases**
8. **One side of the inequality is tight**
9. **There's a unique optimal up to symmetry**
10. **The answer is a sum/product over independent subproblems**

---

## X. WHEN YOU CAN'T FIND THE OBSERVATION

After 30 minutes:

1. **Read the editorial** (or hint, if available)
2. **Find similar problems** online; observe their patterns
3. **Think about what algorithm class fits the constraints** — work backward
4. **Sketch the brute force**; can you optimize step-by-step?
5. **Sleep on it**. Sometimes 8 hours later, the insight pops in the shower.

---

## XI. THE OBSERVATION JOURNAL

Maintain a log:

```
PROBLEM: [name]
DIFFICULTY: 1800 CF
KEY OBSERVATION: "Whenever you have a contiguous block of '0's between '1's, you must use exactly one operation."
HOW I FOUND IT: Computed n=4, 5, 6 by hand, noticed counts.
PATTERN CATEGORY: Constructive + counting via blocks.
```

After 100 entries, you'll see a meta-pattern: how observations are typically found in your weakest categories.

---

## XII. EXERCISES

For each, find the key observation:

1. Given a binary array, in one move you can flip any subarray. Min moves to make it all 0s? *(Hint: count "1 → 0 boundaries" and "0 → 1 boundaries".)*
2. Given array, count subarrays whose XOR equals 0. *(Hint: prefix XOR; equal prefix XORs mean zero subarray XOR.)*
3. You have n stones, each pair you remove gives |a-b| as new stone. Final stone? *(Hint: parity of total sum invariant.)*
4. Given a permutation, count number of adjacent swaps to sort it. *(Hint: number of inversions.)*

---

**→ Next:** [`04-Pattern-Recognition.md`](./04-Pattern-Recognition.md)
