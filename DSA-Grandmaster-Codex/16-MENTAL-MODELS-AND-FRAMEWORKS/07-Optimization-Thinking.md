# 🚀 Optimization Thinking

> *"All speed comes from one source: doing less work. Optimization is the discovery of redundancy."*

---

## THE WORLDVIEW
Every brute force has redundancy. Find it. Eliminate it. Replace expensive operations with cheap ones.

## THE TRIGGERS
- "This recomputes the same thing" → memoize
- "This searches linearly" → hash / binary search
- "This re-checks all pairs" → two pointers / monotonic structure
- "This re-sorts repeatedly" → priority queue

## THE 7 SOURCES OF REDUNDANCY
1. Repeated computation → memoize / DP
2. Redundant search → hash / sort / index
3. Re-doing aggregates → prefix sums / sliding window
4. Considering impossible cases → pruning
5. Redundant state → smaller state
6. Unnecessary sorting → different structure
7. Examining all pairs → two pointers / sweep

## THE OPTIMIZATION HIERARCHY
```
O(n!) → O(2ⁿ) [pruning, DP]
O(2ⁿ) → O(n²) [bitmask DP, MITM]
O(n³) → O(n²) [smarter transitions]
O(n²) → O(n log n) [sort + scan, D&C]
O(n²) → O(n) [hash, two pointers, monotonic stack]
O(log n) → O(1) [precompute]
```

## THE METHOD
1. Write brute force.
2. Identify the bottleneck (most expensive repeated step).
3. Ask: what information am I throwing away? recomputing?
4. Choose a structure/technique to eliminate the waste.

## EXERCISE
Optimize:
1. Two-sum O(n²) → O(n) with hash
2. Range sum queries O(n) each → O(1) with prefix sums
3. Max subarray O(n²) → O(n) with Kadane
4. Next greater element O(n²) → O(n) with monotonic stack

---

**→ Next:** [`08-State-Thinking.md`](./08-State-Thinking.md) | Deep dive: [`../03-PROBLEM-SOLVING-FOUNDATIONS/06-Optimization-Thinking.md`](../03-PROBLEM-SOLVING-FOUNDATIONS/06-Optimization-Thinking.md)
