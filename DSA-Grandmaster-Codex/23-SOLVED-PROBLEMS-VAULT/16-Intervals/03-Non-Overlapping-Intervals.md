# Non-Overlapping Intervals

**Platform**: LeetCode 435 · **Difficulty**: Medium · **Topics**: Array, Dynamic Programming, Greedy, Sorting · **Pattern**: Activity-selection (sort by end)

---

## 📜 Problem Statement

Given an array of intervals `intervals` where `intervals[i] = [start_i, end_i]`, return *the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping*.

**Note** that intervals which only touch at a point are **non-overlapping**. For example, `[1, 2]` and `[2, 3]` are non-overlapping.

### Examples

**Example 1:**
```
Input:  intervals = [[1,2],[2,3],[3,4],[1,3]]
Output: 1
Explanation: [1,3] can be removed and the rest are non-overlapping.
```

**Example 2:**
```
Input:  intervals = [[1,2],[1,2],[1,2]]
Output: 2
Explanation: You need to remove two [1,2] to make the rest non-overlapping.
```

**Example 3:**
```
Input:  intervals = [[1,2],[2,3]]
Output: 0
Explanation: You don't need to remove any of the intervals since they're already non-overlapping.
```

### Constraints
```
1 <= intervals.length <= 10^5
intervals[i].length == 2
-5 * 10^4 <= start_i < end_i <= 5 * 10^4
```

---

## 🧠 Understanding the problem

"Minimum to remove so the rest don't overlap" is the same as "**maximum number of non-overlapping intervals you can keep**," and removals = `n − kept`. Keeping the most intervals is the classic **activity-selection** problem.

The greedy: to pack the most non-overlapping intervals, always keep the one that **finishes earliest**. An interval that ends sooner leaves the most room on the timeline for the intervals that follow. So sort by **end**, walk through, and keep an interval only if its start is `>=` the end of the last kept interval; otherwise it overlaps and must be removed.

Why "earliest finish" is optimal (exchange argument): suppose an optimal solution's first kept interval finishes later than the earliest-finishing one. Swap in the earliest-finishing interval — it overlaps no more than the original did (it ends sooner), so the rest of the optimal selection still fits. Repeating the swap turns any optimal solution into the greedy one without losing intervals.

---

## Approach 1 — DP (longest non-overlapping chain)

### Intuition
This is "Longest Increasing Subsequence" on intervals: sort by start, then `dp[i]` = max intervals we can keep ending with interval `i`, taking the best earlier interval whose end `<=` interval `i`'s start. Answer = `n − max(dp)`.

### Algorithm
1. Sort by start.
2. `dp[i] = 1`; for each `j < i` with `intervals[j].end <= intervals[i].start`, `dp[i] = max(dp[i], dp[j]+1)`.
3. Return `n − max(dp)`.

### Dry run on `[[1,2],[2,3],[3,4],[1,3]]`
```
sort by start → [[1,2],[1,3],[2,3],[3,4]]
dp[0]=1 ([1,2])
dp[1]=1 ([1,3]; no earlier end<=1)
dp[2]=2 ([2,3]; after [1,2] end2<=2)
dp[3]=3 ([3,4]; after [2,3] → 2+1)
max dp = 3 → remove 4-3 = 1  ✓
```

### Code
```cpp
int eraseOverlapIntervals(vector<vector<int>>& intervals) {
    sort(intervals.begin(), intervals.end());
    int n = intervals.size(), best = 1;
    vector<int> dp(n, 1);
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++)
            if (intervals[j][1] <= intervals[i][0])
                dp[i] = max(dp[i], dp[j] + 1);
        best = max(best, dp[i]);
    }
    return n - best;
}
```
```java
public int eraseOverlapIntervals(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
    int n = intervals.length, best = 1;
    int[] dp = new int[n];
    Arrays.fill(dp, 1);
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++)
            if (intervals[j][1] <= intervals[i][0])
                dp[i] = Math.max(dp[i], dp[j] + 1);
        best = Math.max(best, dp[i]);
    }
    return n - best;
}
```
```python
def eraseOverlapIntervals(intervals):
    intervals.sort()
    n = len(intervals)
    dp = [1] * n
    best = 1
    for i in range(1, n):
        for j in range(i):
            if intervals[j][1] <= intervals[i][0]:
                dp[i] = max(dp[i], dp[j] + 1)
        best = max(best, dp[i])
    return n - best
```

### Complexity
- **Time**: O(n²) — will TLE at n = 10^5.
- **Space**: O(n).

### Verdict
Useful for understanding the "keep the most" framing, but the O(n²) DP is too slow for the constraints. The greedy is exponentially better.

---

## Approach 2 — Greedy, sort by end (optimal) ⭐

### Intuition
Sort by end. Track `end` = end of the last kept interval (start at `−∞`). For each interval: if its start `>= end`, it doesn't overlap → keep it and advance `end`. Otherwise it overlaps → count a removal (and crucially, keep the earlier-finishing interval, which we already did).

### Algorithm
1. Sort intervals by `end` ascending.
2. `removed = 0`, `end = −∞`.
3. For each `[s, e]`:
   - If `s >= end` → keep: `end = e`.
   - Else → `removed++`.
4. Return `removed`.

### Dry run on `[[1,2],[2,3],[3,4],[1,3]]`
```
sort by end → [[1,2],[1,3],[2,3],[3,4]]
end=-inf
[1,2]: 1>=-inf → keep, end=2
[1,3]: 1>=2? no → removed=1   (we keep [1,2], which ends earlier)
[2,3]: 2>=2 → keep, end=3
[3,4]: 3>=3 → keep, end=4
removed = 1  ✓
```

### Code
```cpp
int eraseOverlapIntervals(vector<vector<int>>& intervals) {
    sort(intervals.begin(), intervals.end(),
         [](const vector<int>& a, const vector<int>& b){ return a[1] < b[1]; });
    int removed = 0, end = INT_MIN;
    for (auto& iv : intervals) {
        if (iv[0] >= end) end = iv[1];   // keep
        else removed++;                   // overlaps → drop
    }
    return removed;
}
```
```java
public int eraseOverlapIntervals(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> Integer.compare(a[1], b[1]));
    int removed = 0, end = Integer.MIN_VALUE;
    for (int[] iv : intervals) {
        if (iv[0] >= end) end = iv[1];
        else removed++;
    }
    return removed;
}
```
```python
def eraseOverlapIntervals(intervals):
    intervals.sort(key=lambda x: x[1])
    removed, end = 0, float('-inf')
    for s, e in intervals:
        if s >= end:
            end = e
        else:
            removed += 1
    return removed
```

### Complexity
- **Time**: O(n log n) — the sort.
- **Space**: O(1) extra.

### Verdict
**Optimal.** Sort by end + one comparison per interval. The exchange-argument proof makes it bullet-proof.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| DP (LIS-style) | O(n²) | O(n) | good intuition, TLE at scale |
| Greedy (sort by end) | **O(n log n)** | O(1) | optimal ⭐ |

The subtle point: **sort by end, not by start**. Sorting by start and greedily keeping the first one fails (a long early interval can block many short ones). When forced to drop on overlap, you should drop the one ending *later* — which sorting by end handles automatically.

---

## 🧪 Edge cases & pitfalls
- **Touching endpoints** (`[1,2],[2,3]`) → **not** overlapping (`2 >= 2`), keep both. Use `>=`, not `>`.
- **Identical intervals** (`[[1,2],[1,2],[1,2]]`) → keep one, remove two.
- **Single interval** → `0`.
- **Pitfall**: sorting by start. If you must sort by start, the correct greedy keeps the interval with the smaller end on conflict — more bookkeeping. Sorting by end avoids this entirely.
- **Pitfall**: using `>` for the keep test would wrongly drop touching intervals (the problem explicitly says touching is fine).

---

## 🔗 Related problems
- **Merge Intervals** (LC 56) — sort by start instead (previous).
- **Maximum Length of Pair Chain** (LC 646) — the "keep" version of this exact greedy.
- **Minimum Number of Arrows to Burst Balloons** (LC 452) — sort by end, count groups.
- **Meeting Rooms** (LC 252) — feasibility check (next).

---

**→ Next:** [`04-Meeting-Rooms.md`](./04-Meeting-Rooms.md) | **Prev:** [`02-Merge-Intervals.md`](./02-Merge-Intervals.md) | [Problem set index](./00-Index.md)
