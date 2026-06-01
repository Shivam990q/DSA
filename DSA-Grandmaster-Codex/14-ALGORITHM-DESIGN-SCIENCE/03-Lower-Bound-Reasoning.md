# ⬇️ Lower-Bound Reasoning — Proving "No Faster Algorithm Exists"

> *"An upper bound says 'we can do this fast.' A lower bound says 'we can never do faster.' The second is harder, and more profound."*

---

## I. WHAT IS A LOWER BOUND?

A **lower bound** proves that **no algorithm** (in some model) can solve a problem faster than some limit.

- Upper bound: "There EXISTS an algorithm running in O(f(n))." (Just exhibit one.)
- Lower bound: "EVERY algorithm requires Ω(g(n))." (Must reason about all possible algorithms.)

Lower bounds are intellectually deeper because they quantify over infinitely many algorithms.

---

## II. THE COMPARISON-SORT LOWER BOUND (the classic)

**Theorem**: Any comparison-based sorting algorithm requires Ω(n log n) comparisons in the worst case.

**Proof** (decision tree argument):
1. A comparison sort is a decision tree: each internal node is a comparison (a[i] < a[j]?), each leaf is a permutation.
2. There are n! possible permutations of n distinct elements. The tree must have ≥ n! leaves (to distinguish all).
3. A binary tree with L leaves has height ≥ log₂(L).
4. Height = worst-case number of comparisons.
5. So height ≥ log₂(n!) = Θ(n log n) (by Stirling's approximation).

Therefore: no comparison sort beats n log n. □

**Implication**: counting sort, radix sort (non-comparison) CAN beat n log n — they don't fit this model.

---

## III. THE MODELS OF COMPUTATION

Lower bounds are always **relative to a model**:

| Model                  | What it allows                              |
|------------------------|---------------------------------------------|
| Comparison model       | Only comparisons between elements           |
| Algebraic decision tree| Arithmetic + comparisons                    |
| Cell-probe model       | Memory accesses (for data structure bounds) |
| Communication model    | Bits exchanged between parties              |
| Turing machine         | General computation                         |

A lower bound in a weak model may not hold in a stronger one.

---

## IV. TYPES OF LOWER-BOUND ARGUMENTS

### 1. **Information-theoretic** (counting)
The output requires distinguishing among N possibilities → need ≥ log N bits of info → ≥ log N operations.

> Sorting: n! outputs → log(n!) = Ω(n log n).

### 2. **Adversary argument**
An adversary answers queries to maximize the algorithm's work, maintaining consistency.

> Finding max of n elements requires n-1 comparisons: adversary ensures each non-max element loses exactly once.

### 3. **Reduction-based**
Reduce a problem with a known lower bound to your problem.

> If problem A (known Ω(f)) reduces to B, then B is Ω(f) too.

### 4. **Communication complexity**
Lower-bound the bits two parties must exchange → implies time/space bounds.

---

## V. FAMOUS LOWER BOUNDS

### Element distinctness: Ω(n log n) (algebraic decision tree)
Determining if n numbers are all distinct.

### Convex hull: Ω(n log n)
Reduces from sorting.

### Finding median: Ω(n) comparisons (and exactly ~3n/2 with clever algorithms)

### Matrix multiplication: Ω(n²) (trivial — must read all input)
Best known upper bound: O(n^2.371). The gap is OPEN — a famous open problem.

### 3SUM: conjectured Ω(n²)
Believed but unproven. Many "3SUM-hard" problems rely on this conjecture.

### Comparison-based search in sorted array: Ω(log n)
Binary search is optimal.

---

## VI. CONDITIONAL LOWER BOUNDS (modern)

Some lower bounds are conditional on conjectures:

### SETH (Strong Exponential Time Hypothesis)
"SAT can't be solved much faster than 2^n."

If SETH holds, then:
- Edit distance can't be done in O(n^(2-ε))
- Many problems have conditional quadratic lower bounds

### 3SUM Conjecture
"3SUM requires Ω(n²)."

If true, many computational geometry problems are quadratically hard.

These conditional bounds are the frontier of fine-grained complexity.

---

## VII. WHY LOWER BOUNDS MATTER

1. **Stop wasting time**: if a problem has an Ω(n²) lower bound, don't search for O(n log n).
2. **Know when you're optimal**: binary search is provably optimal for sorted search.
3. **Understand the problem's intrinsic difficulty.**
4. **Guide algorithm design**: lower bounds reveal where the difficulty lives.

---

## VIII. THE ADVERSARY ARGUMENT — A WORKED EXAMPLE

**Claim**: finding the maximum of n elements requires ≥ n-1 comparisons.

**Proof** (adversary):
- Think of each element as a "player." The max is the "winner."
- For an element to be ruled out as the max, it must "lose" at least one comparison.
- There are n-1 non-max elements, each needs ≥ 1 loss.
- Each comparison produces exactly 1 loser.
- So ≥ n-1 comparisons needed. □

This proves the obvious algorithm (n-1 comparisons) is optimal.

---

## IX. EXERCISES

1. Prove that finding both min and max requires ~3n/2 comparisons (not 2n).
2. Prove searching an unsorted array requires Ω(n) in the worst case.
3. Why can radix sort beat the comparison-sort lower bound?
4. Prove that merging two sorted lists of size n requires Ω(n) comparisons.
5. Show that any algorithm to find the median needs Ω(n) comparisons.

---

## X. RECOMMENDED READING

- **CLRS Chapter 8** — sorting lower bounds
- **Arora & Barak**, *Computational Complexity* — deep lower bounds
- **Fine-grained complexity** survey papers (Virginia Vassilevska Williams)

---

**→ Next:** [`04-Discovering-Invariants.md`](./04-Discovering-Invariants.md)
