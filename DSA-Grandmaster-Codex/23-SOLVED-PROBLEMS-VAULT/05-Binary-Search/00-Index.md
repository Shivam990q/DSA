# 🗂️ Binary Search — Problem Set

> Each problem below is a **complete editorial**: full statement (platform-style) → every approach from brute force to optimal → intuition, algorithm, dry run, C++ / Java / Python code, complexity, edge cases, pitfalls, and related problems.

> **How to use**: open a problem, read ONLY the statement, attempt it cold (30–45 min). Then read the approaches in order — feel WHY each one improves on the last. Re-derive the optimal from the key insight after 7 days.

---

## 📋 Problems

| # | Problem | LC # | Difficulty | Core Approaches |
|---|---------|------|------------|-----------------|
| 01 | [Binary Search](./01-Binary-Search.md) | 704 | Easy | linear scan → classic two-bound search |
| 02 | [Search a 2D Matrix](./02-Search-2D-Matrix.md) | 74 | Medium | full scan → row+col search → flattened binary search |
| 03 | [Koko Eating Bananas](./03-Koko-Eating-Bananas.md) | 875 | Medium | linear scan on k → binary search on the answer |
| 04 | [Find Minimum in Rotated Sorted Array](./04-Find-Minimum-Rotated-Sorted-Array.md) | 153 | Medium | linear scan → pivot binary search |
| 05 | [Search in Rotated Sorted Array](./05-Search-Rotated-Sorted-Array.md) | 33 | Medium | linear scan → find-pivot+search → one-pass sorted-half |
| 06 | [Time Based Key-Value Store](./06-Time-Based-Key-Value-Store.md) | 981 | Medium | linear scan → binary search on timestamps |
| 07 | [Median of Two Sorted Arrays](./07-Median-of-Two-Sorted-Arrays.md) | 4 | Hard | merge → merge-halfway → partition binary search |

---

## 🎯 The pattern family

**Binary search** is the art of *halving the search space every step*. The recurring move: *"there is an ordering or a monotonic property; instead of checking every candidate, I jump to the middle and discard half."* That single idea turns O(n) into O(log n).

There are two distinct flavors, and recognizing which one you're in is half the battle.

### 1. Binary search on an **index** (search a sorted array)
The array itself is sorted, so the comparison `a[mid] vs target` tells you which half to keep.

- **Plain sorted array** → compare `a[mid]` to `target`, move a bound (Binary Search, LC 704).
- **Sorted-by-flattening** → a 2D matrix that reads like one long sorted array; map `idx → (idx/n, idx%n)` (Search a 2D Matrix, LC 74).
- **Rotated sorted array** → the array isn't globally sorted, but *one half always is*. Detect the sorted half, then decide direction (Find Minimum LC 153, Search Rotated LC 33).
- **Find the boundary in a stored timeline** → binary search for the rightmost timestamp ≤ query (Time Based Store, LC 981).

### 2. Binary search on the **answer** (binary search on a monotonic predicate)
The array isn't what you search — you search the *space of possible answers*. This works whenever a feasibility test `feasible(x)` is **monotonic**: false, false, …, false, true, true, … (or the reverse). You binary search for the boundary.

- **Minimize a rate / capacity** → "what is the smallest speed `k` such that we finish in time?" `feasible(k)` is monotonic in `k` (Koko Eating Bananas, LC 875).

The mental checklist for "binary search on the answer":
1. Can I phrase the answer as "the smallest/largest `x` such that `P(x)` holds"?
2. Is `P` monotonic (once true, always true as `x` grows, or vice-versa)?
3. What are the natural lo/hi bounds for `x`?

### 3. The boundary-search template (lower/upper bound)
Most binary search bugs come from off-by-one errors and infinite loops. Two reliable templates:

- **`while (lo <= hi)`** with `lo = mid + 1` / `hi = mid - 1` — used when you return *as soon as you find* the target (LC 704, LC 33).
- **`while (lo < hi)`** with `hi = mid` / `lo = mid + 1` — used when you're *converging onto a boundary* and want `lo == hi` at the end (LC 153, LC 875). Always make sure one branch strictly shrinks the range to avoid infinite loops.

The unifying invariant: **the answer always lives inside `[lo, hi]`**. Every step must preserve that while shrinking the window.

---

**→ Start:** [`01-Binary-Search.md`](./01-Binary-Search.md) | Back to [vault index](../00-Index.md)
