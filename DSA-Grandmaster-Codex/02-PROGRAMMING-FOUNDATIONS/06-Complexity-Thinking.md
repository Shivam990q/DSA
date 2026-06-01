# 📈 Complexity Thinking — The Asymptotic Worldview

> *"Big-O is not a number. It's a way of seeing growth."*

---

## I. WHY COMPLEXITY MATTERS

A computer at 10⁸ operations/second:
- O(n) at n=10⁹ → 10 seconds
- O(n log n) at n=10⁹ → ~300 seconds
- O(n²) at n=10⁹ → ~10¹⁰ seconds = 300+ years
- O(2ⁿ) at n=64 → universe-age

**Complexity decides whether your algorithm finishes before your funeral.**

---

## II. BIG-O, BIG-Ω, BIG-Θ

- **Big-O**: upper bound. `f(n) = O(g(n))` ⟺ ∃c, n₀ s.t. f(n) ≤ c·g(n) for n ≥ n₀
- **Big-Ω**: lower bound
- **Big-Θ**: tight bound (both)

In practice, "Big-O" is used loosely to mean tight. Don't be a pedant; be understood.

---

## III. THE COMPLEXITY ZOO

| Class       | Name             | Example                         | n=10⁶ feasibility |
|-------------|------------------|---------------------------------|-------------------|
| O(1)        | Constant         | Hash lookup, array access       | ✅ instant        |
| O(log n)    | Logarithmic      | Binary search                   | ✅ instant        |
| O(√n)       | Square root      | Trial division for primality    | ✅ fast (1000)    |
| O(n)        | Linear           | Single loop                     | ✅ ~10 ms         |
| O(n log n)  | Linearithmic     | Merge sort, FFT                 | ✅ ~200 ms        |
| O(n^1.5)    | Sublinear-quad   | Mo's algorithm                  | ✅ ~10 s          |
| O(n²)       | Quadratic        | Bubble sort                     | ❌ ~3 hours       |
| O(n² log n) | Quadlog          | Some segtree variants           | ❌                |
| O(n³)       | Cubic            | Floyd-Warshall                  | ❌                |
| O(2ⁿ)       | Exponential      | Subset enumeration              | ❌ at n=30        |
| O(n!)       | Factorial        | Permutations                    | ❌ at n=12        |

---

## IV. THE CONSTRAINT-COMPLEXITY MAP

In contests, the constraint dictates the algorithm class:

| n            | Allowed Complexity                    |
|--------------|---------------------------------------|
| n ≤ 12       | O(n!) — full permutations             |
| n ≤ 18       | O(2ⁿ × n) — bitmask DP                |
| n ≤ 25       | O(2ⁿ) or O(2^(n/2)) MITM              |
| n ≤ 100      | O(n⁴) — sparse use                    |
| n ≤ 500      | O(n³) — Floyd-Warshall, etc           |
| n ≤ 5,000    | O(n²) — DP, naive interval            |
| n ≤ 100,000  | O(n log n) — sort, segtree            |
| n ≤ 1,000,000 | O(n) or O(n log log n) — sieve, KMP  |
| n ≤ 10⁹      | O(log n) — binary search, math        |
| n ≤ 10¹⁸     | O(1) or O(log n) — formulas only      |

---

## V. THE MASTER THEOREM

For recurrences of form `T(n) = a·T(n/b) + f(n)`:

- If `f(n) = O(n^c)` and `c < log_b(a)`, T(n) = Θ(n^log_b(a))
- If `f(n) = Θ(n^c)` and `c = log_b(a)`, T(n) = Θ(n^c · log n)
- If `f(n) = Ω(n^c)` and `c > log_b(a)`, T(n) = Θ(f(n))

**Examples:**
- Merge sort: T(n) = 2T(n/2) + O(n) → c=1, log_b(a)=1, equal → O(n log n)
- Binary search: T(n) = T(n/2) + O(1) → c=0, log_b(a)=0, equal → O(log n)
- Strassen: T(n) = 7T(n/2) + O(n²) → c=2, log_b(a)=log₂7 ≈ 2.81 → O(n^2.81)

---

## VI. AMORTIZED ANALYSIS

When operations have varying cost, **average over a sequence**.

**Example**: dynamic array (vector) push_back.
- Most pushes: O(1)
- Occasional resize: O(n)
- But amortized over n pushes: O(n) total → **O(1) amortized per push**.

**Three methods**:
1. **Aggregate**: total cost / number of ops
2. **Accounting**: charge cheap ops a "savings" used by expensive ops
3. **Potential function**: define Φ; amortized = actual + ΔΦ

DSU with path compression + union-by-rank: amortized α(n) per op (essentially O(1)).

---

## VII. SPACE COMPLEXITY

Often forgotten until you OOM at n=10⁹.

- O(1) — a few variables
- O(log n) — recursion depth (BS, segtree query)
- O(n) — single array
- O(n²) — adjacency matrix, 2D DP table
- O(2ⁿ) — bitmask DP table

**Rule of thumb**: n=10⁵ allows O(n²) ≈ 10¹⁰ bool entries... no wait, 10¹⁰ bytes is 10GB. Nope. Use O(n) memory wherever possible.

**1 GB ≈ 10⁹ bytes ≈ 2.5×10⁸ ints ≈ 1.25×10⁸ long longs.**

---

## VIII. AVERAGE VS WORST VS BEST CASE

- **Best case**: minimum work over all inputs of size n
- **Average case**: expected work over distribution of inputs
- **Worst case**: maximum work over all inputs of size n

**For algorithms**: usually quote worst-case.
**For data structures**: amortized worst-case + worst-case-per-op separately.

> Quicksort: best O(n log n), avg O(n log n), worst O(n²).
> Hash map: avg O(1), worst O(n).
> DSU: amortized O(α(n)), worst-case O(α(n)) per op (with path compression + union by rank).

---

## IX. ANALYZING NESTED LOOPS

```cpp
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= n; j *= 2)
        do_work();
```

- Outer: n iterations
- Inner: log n iterations
- **Total: O(n log n)**

```cpp
for (int i = 1; i <= n; i++)
    for (int j = i; j <= n; j++)
        do_work();
```

- Sum: n + (n-1) + (n-2) + ... + 1 = n(n+1)/2
- **Total: O(n²)** (the constant 1/2 doesn't matter asymptotically)

```cpp
for (int i = 1; i <= n; i *= 2)
    for (int j = 1; j <= i; j++)
        do_work();
```

- Outer: log n iterations: i = 1, 2, 4, ..., n
- Inner: i iterations
- Sum: 1 + 2 + 4 + ... + n = 2n - 1
- **Total: O(n)**

---

## X. RECURRENCE COMPLEXITY (without Master Theorem)

Sometimes recursions don't fit Master Theorem.

**Example**: T(n) = T(n-1) + O(n) → expand: O(1) + O(2) + ... + O(n) = O(n²)

**Example**: T(n) = T(√n) + 1 → height of recursion = log log n, so O(log log n)

**Example**: T(n) = T(n/2) + T(n/4) + n
→ Use **Akra-Bazzi** or expansion. Result: O(n).

---

## XI. TIPS FOR ESTIMATING COMPLEXITY ON THE FLY

1. **Count loops**: nested loops multiply
2. **Note divisions/halvings**: each contributes log n
3. **Recursion**: count branches × depth
4. **Identify the bottleneck**: usually the dominant nested loop
5. **Don't worry about constants** (but for very tight problems, do)

---

## XII. RECOMMENDED READING

- **CLRS** Chapter 3 (asymptotic notation)
- **Kleinberg & Tardos** Chapter 2
- **Knuth, TAOCP** Vol 1 (asymptotic analysis in depth)

---

**→ Next:** [`07-Mathematics-for-Programmers.md`](./07-Mathematics-for-Programmers.md)
