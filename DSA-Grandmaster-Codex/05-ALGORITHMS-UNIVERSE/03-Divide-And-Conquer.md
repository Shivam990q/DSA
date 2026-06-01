# ⚔️ Divide and Conquer — The Recursive Worldview

> *"To conquer a giant: divide it. To conquer a problem: divide it the same way."*

---

## I. THE PARADIGM

Three steps:
1. **Divide** the problem into smaller subproblems (usually of size n/b)
2. **Conquer** subproblems recursively
3. **Combine** subproblem solutions into the original

Recurrence: T(n) = a · T(n/b) + f(n) (a subproblems of size n/b, plus combine cost f(n))

---

## II. THE MASTER THEOREM

For T(n) = a·T(n/b) + Θ(n^c):

| Case | Condition          | Result                |
|------|--------------------|-----------------------|
| 1    | c < log_b(a)       | Θ(n^log_b(a))         |
| 2    | c = log_b(a)       | Θ(n^c · log n)        |
| 3    | c > log_b(a)       | Θ(n^c)                |

### Examples
- T(n) = 2T(n/2) + O(n) → c=1, log_b(a)=1, case 2 → O(n log n) (merge sort)
- T(n) = T(n/2) + O(1) → c=0, log_b(a)=0, case 2 → O(log n) (binary search)
- T(n) = 7T(n/2) + O(n²) → c=2, log_b(a)=log₂7 ≈ 2.81, case 1 → O(n^2.81) (Strassen)
- T(n) = 4T(n/2) + O(n) → c=1, log_b(a)=2, case 1 → O(n²)

---

## III. CLASSIC D&C ALGORITHMS

### Merge Sort — O(n log n)
Split array in half; sort each; merge.

### Quick Sort — O(n log n) avg, O(n²) worst
Partition around pivot; sort each half.

### Binary Search — O(log n)
Halve the search space.

### Quickselect — O(n) avg
Quicksort partition; recurse only into the side containing kth element.

### Karatsuba multiplication — O(n^log₂3) ≈ O(n^1.585)
n-digit × n-digit multiplication via 3 (n/2)-digit multiplications.

### Strassen's matrix multiplication — O(n^log₂7) ≈ O(n^2.81)
2×2 matrix multiplication via 7 (instead of 8) sub-multiplications.

### Fast Fourier Transform (FFT) — O(n log n)
Polynomial multiplication / convolution via D&C in frequency domain.

### Closest pair of points — O(n log n)
Split plane; recurse; check strip.

### Largest rectangle in histogram — O(n log n) (also doable in O(n) with stack)

### Counting inversions — O(n log n) via merge sort

---

## IV. WHEN D&C SHINES

- Problem decomposes naturally into independent subproblems
- Combine step is cheap relative to subproblem solving
- Recursion depth is bounded (log n typically)

---

## V. WHEN NOT D&C

- Subproblems overlap heavily → use DP, not D&C
- Combine step is expensive → may not gain
- Recursion overhead matters (small n)

---

## VI. PROBLEMS

1. Merge sort (LC 912)
2. Quick sort
3. Quickselect: Kth largest element (LC 215)
4. Maximum subarray (D&C version, LC 53)
5. Median of two sorted arrays (LC 4)
6. Count of smaller numbers after self (LC 315) — merge sort
7. Reverse pairs (LC 493) — merge sort
8. Different ways to add parentheses (LC 241)
9. Convex hull (D&C version)
10. Closest pair of points
11. K-th smallest in two sorted arrays
12. Skyline problem (D&C variant)

---

**→ Next:** [`04-Greedy-Algorithms.md`](./04-Greedy-Algorithms.md)
