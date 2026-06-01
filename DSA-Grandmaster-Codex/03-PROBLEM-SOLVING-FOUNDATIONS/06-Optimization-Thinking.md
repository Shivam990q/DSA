# 🚀 Optimization Thinking — From Naive to Optimal

> *"Optimization is the discovery of redundancy."*

---

## I. THE SEVEN SOURCES OF REDUNDANCY

Every brute force has redundancy. Find it, eliminate it, optimize.

### 1. **Repeated computation** → Memoize / DP
The same subproblem solved multiple times.

> Fibonacci: `fib(5)` recomputes `fib(2)` three times → memoize.

### 2. **Redundant search** → Index / Hash / Sort
Linear scan for something findable in O(1) or O(log n).

> Two-sum: scan for `target - x` → use hash map.

### 3. **Re-doing aggregates** → Prefix sums / Sliding window
Recomputing range sums or counts.

> Max sum subarray: prefix sums, then S[r] − S[l−1] in O(1).

### 4. **Considering impossible cases** → Pruning / Constraints
Trying paths that are clearly invalid.

> Backtracking with bounds: if partial cost ≥ best so far, prune.

### 5. **Maintaining redundant state** → Smaller state
DP state with extra dimensions that don't matter.

> "Coin change with order": same answer regardless of order; state is just (amount).

### 6. **Sorting unnecessarily** → Use a different structure
Repeatedly sorting → priority queue.

> Top-K with stream: don't re-sort all; maintain a heap.

### 7. **Examining all pairs** → Two pointers / Sweep
O(n²) pair-checking when both indices have monotonic relationship.

> Pair sum in sorted array: two pointers from ends.

---

## II. THE OPTIMIZATION HIERARCHY

```
O(n!) → O(2ⁿ) [pruning, DP]
O(2ⁿ) → O(n²) [bitmask DP, MITM]
O(n³) → O(n²) [smarter DP transitions]
O(n²) → O(n log n) [sort + scan, divide-conquer]
O(n²) → O(n) [hash map, two pointers, monotonic stack]
O(n log n) → O(n) [hashing, counting sort, linear-time selection]
O(log² n) → O(log n) [smarter DS]
O(log n) → O(1) [precomputed table, hash]
```

Most "interview" problems sit at O(n²) → O(n log n) or O(n²) → O(n). Master these transitions.

---

## III. THE OPTIMIZATION RECIPES

### Recipe 1: **Memoize repeated subproblems**
```
slow_fn(x):
    if x is base: return base_val
    return f(slow_fn(smaller))    # SLOW: recomputes

fast_fn(x):
    if memo[x]: return memo[x]
    if x is base: return memo[x] = base_val
    return memo[x] = f(fast_fn(smaller))    # FAST
```

### Recipe 2: **Replace linear scan with hash**
```
# Slow: O(n²)
for i: for j: if a[j] == something_about_i: ...

# Fast: O(n)
hash = {}
for i: 
    if a[i] in hash: ...
    hash[a[i]] = i
```

### Recipe 3: **Prefix sum**
```
# Slow: O(n) per range query
sum_l_r = 0
for i in range(l, r+1): sum_l_r += a[i]

# Fast: O(n) preprocess, O(1) per query
P = [0]
for x in a: P.append(P[-1] + x)
sum_l_r = P[r+1] - P[l]
```

### Recipe 4: **Sliding window**
```
# Slow: O(n²)
for i: for j: check a[i..j]

# Fast: O(n) when window monotonic
l = 0
for r in range(n):
    expand_window(a[r])
    while not_valid(): shrink_window(a[l]); l += 1
    record_answer(l, r)
```

### Recipe 5: **Sort + scan**
```
# Many problems become trivial after sort.
# E.g., interval scheduling, pairing, etc.
```

### Recipe 6: **Binary search the answer**
```
# When predicate "is X feasible?" is monotonic in X:
def search():
    lo, hi = MIN, MAX
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid): hi = mid
        else: lo = mid + 1
    return lo
```

### Recipe 7: **Two pointers**
```
# Sorted/monotonic arrays:
i, j = 0, n-1
while i < j:
    if condition(a[i], a[j]): record; i += 1
    else: j -= 1
```

### Recipe 8: **Monotonic stack/deque**
For "next greater" / "sliding window max" / "max rectangle"

### Recipe 9: **Divide and conquer**
T(n) = aT(n/b) + f(n) — when overlapping isn't needed.

### Recipe 10: **Greedy + Proof**
When local choices give global optimum (proven by exchange argument).

---

## IV. THE OPTIMIZATION QUESTIONS

For any brute force, ask:

1. **What is the most expensive step?** (the bottleneck)
2. **What information do I have at this step but am throwing away?** (state to maintain)
3. **What computations am I doing twice?** (memoize)
4. **What ordering would simplify things?** (sort)
5. **What's the structure of the answer space?** (search space)
6. **Is there monotonicity I can exploit?** (binary search)
7. **Can I solve a smaller related problem first?** (divide-conquer / DP)

---

## V. THE EXAMPLE: KADANE'S ALGORITHM

**Problem**: Maximum sum subarray.

**Brute O(n²):** for each (i, j), compute sum, track max. O(n²).

**Bottleneck**: sum is recomputed for overlapping subarrays.

**Optimization 1 (prefix sums)**: precompute P[i] = sum to i. Now sum(l..r) = P[r] - P[l-1] in O(1). Total: O(n²).

**Optimization 2 (clever observation)**:
- For each end r, max sum subarray ending at r either uses r alone (sum = a[r]) or extends a previous one (sum = max_ending_at(r-1) + a[r]).
- Define `dp[r]` = max sum subarray ending at r.
- Recurrence: `dp[r] = max(a[r], dp[r-1] + a[r])`.
- Answer: max(dp[*]).

**Total: O(n)** with O(1) extra space (just track running max).

This is **Kadane's algorithm**. The leap: notice that the max subarray ending at r is determined by the max subarray ending at r-1. Subproblem structure → DP.

---

## VI. WHEN OPTIMIZATION DOESN'T HELP

Sometimes the brute force IS optimal:

- For small n, constants matter more than asymptotics.
- For one-shot computations, simplicity > speed.
- For correctness, simple > clever.

**Don't optimize what doesn't need optimization.** Profile first.

---

## VII. THE OPTIMIZATION HIERARCHY (PROFESSIONAL)

When optimizing production code (Level 8):

1. **Algorithmic** (best Big-O class) — biggest gains
2. **Data structure** (right structure for access pattern)
3. **Memory layout** (cache-friendly)
4. **SIMD / parallelism** (multi-core / AVX)
5. **Compiler hints** (likely/unlikely, restrict)
6. **Micro-optimizations** (loop unrolling, branch elimination)

Apply in order. Don't micro-optimize before fixing algorithmic issues.

---

## VIII. THE FINAL TRUTH

> **"Optimization is not making code faster.  
>  It's making code do less work.  
>  All speed comes from one source: doing less."**

---

**→ Next:** [`07-State-Design.md`](./07-State-Design.md)
