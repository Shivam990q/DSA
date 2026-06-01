# Insert Interval

**Platform**: LeetCode 57 · **Difficulty**: Medium · **Topics**: Array · **Pattern**: Three-phase linear merge

---

## 📜 Problem Statement

You are given an array of non-overlapping intervals `intervals` where `intervals[i] = [start_i, end_i]` represent the start and the end of the `i`-th interval and `intervals` is sorted in ascending order by `start_i`. You are also given an interval `newInterval = [start, end]` that represents the start and end of another interval.

Insert `newInterval` into `intervals` such that `intervals` is still sorted in ascending order by `start_i` and `intervals` still does not have any overlapping intervals (merge overlapping intervals if necessary).

Return `intervals` *after the insertion*.

**Note** that you don't need to modify `intervals` in-place. You can make a new array and return it.

### Examples

**Example 1:**
```
Input:  intervals = [[1,3],[6,9]], newInterval = [2,5]
Output: [[1,5],[6,9]]
Explanation: [2,5] overlaps [1,3], merging to [1,5]; [6,9] is untouched.
```

**Example 2:**
```
Input:  intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
Output: [[1,2],[3,10],[12,16]]
Explanation: [4,8] overlaps [3,5],[6,7],[8,10], merging into [3,10].
```

**Example 3:**
```
Input:  intervals = [], newInterval = [5,7]
Output: [[5,7]]
```

### Constraints
```
0 <= intervals.length <= 10^4
intervals[i].length == 2
0 <= start_i <= end_i <= 10^5
intervals is sorted by start_i in ascending order.
newInterval.length == 2
0 <= start <= end <= 10^5
```

---

## 🧠 Understanding the problem

The input is **already sorted and non-overlapping** — that's a gift. We don't need to re-sort; we only need to slot `newInterval` into place and absorb any neighbors it touches.

Picture the number line. Every existing interval falls into exactly one of three buckets relative to `newInterval`:

1. **Entirely before** it — ends strictly before `newInterval` starts (`interval.end < newInterval.start`). Copy as-is.
2. **Overlapping** it — starts at or before `newInterval` ends (`interval.start <= newInterval.end`). Absorb into `newInterval` by taking the min start / max end.
3. **Entirely after** it — starts strictly after `newInterval` ends. Copy as-is.

Because the list is sorted, these three groups appear in exactly that order, so three sequential `while` loops handle them cleanly.

---

## Approach 1 — Three-phase linear scan (optimal) ⭐

### Intuition
Walk the sorted list once. First emit all intervals that finish before the new one begins. Then merge the run of overlapping intervals into `newInterval`, expanding its bounds. Finally emit everything left.

### Algorithm
1. Phase 1 — while `intervals[i].end < newInterval.start`: push `intervals[i]`, `i++`.
2. Phase 2 — while `intervals[i].start <= newInterval.end`: `newInterval.start = min(...)`, `newInterval.end = max(...)`, `i++`. Then push the merged `newInterval`.
3. Phase 3 — push the rest.

### Dry run on `intervals=[[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval=[4,8]`
```
Phase 1: [1,2].end=2 < 4 → push [1,2]. [3,5].end=5 >= 4 → stop. i=1
Phase 2: [3,5].start=3 <= 8 → new=[min(4,3),max(8,5)]=[3,8]; i=2
         [6,7].start=6 <= 8 → new=[3,max(8,7)]=[3,8]; i=3
         [8,10].start=8 <= 8 → new=[3,max(8,10)]=[3,10]; i=4
         [12,16].start=12 > 10 → stop. push [3,10]
Phase 3: push [12,16]
result = [[1,2],[3,10],[12,16]]  ✓
```

### Code
```cpp
vector<vector<int>> insert(vector<vector<int>>& intervals, vector<int>& newInterval) {
    vector<vector<int>> res;
    int i = 0, n = intervals.size();
    while (i < n && intervals[i][1] < newInterval[0]) res.push_back(intervals[i++]);
    while (i < n && intervals[i][0] <= newInterval[1]) {
        newInterval[0] = min(newInterval[0], intervals[i][0]);
        newInterval[1] = max(newInterval[1], intervals[i][1]);
        i++;
    }
    res.push_back(newInterval);
    while (i < n) res.push_back(intervals[i++]);
    return res;
}
```
```java
public int[][] insert(int[][] intervals, int[] newInterval) {
    List<int[]> res = new ArrayList<>();
    int i = 0, n = intervals.length;
    while (i < n && intervals[i][1] < newInterval[0]) res.add(intervals[i++]);
    while (i < n && intervals[i][0] <= newInterval[1]) {
        newInterval[0] = Math.min(newInterval[0], intervals[i][0]);
        newInterval[1] = Math.max(newInterval[1], intervals[i][1]);
        i++;
    }
    res.add(newInterval);
    while (i < n) res.add(intervals[i++]);
    return res.toArray(new int[res.size()][]);
}
```
```python
def insert(intervals, newInterval):
    res = []
    i, n = 0, len(intervals)
    while i < n and intervals[i][1] < newInterval[0]:
        res.append(intervals[i]); i += 1
    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    res.append(newInterval)
    while i < n:
        res.append(intervals[i]); i += 1
    return res
```

### Complexity
- **Time**: O(n) — each interval is visited once.
- **Space**: O(n) for the output (O(1) extra beyond the result).

### Verdict
**Optimal.** Linear and elegant once you see the three phases. This is the expected answer.

---

## Approach 2 — Binary search for the insertion point

### Intuition
Since the starts are sorted, you can binary-search where `newInterval` belongs, then merge locally. It doesn't beat O(n) (the merge can still touch many intervals), but it's worth knowing when the merge region is tiny relative to `n`, or when this is a building block of a larger sorted structure.

### Algorithm
1. Binary search for the first interval whose `start >= newInterval.start` (insertion index).
2. Insert `newInterval` there.
3. Run a standard merge pass over the (still sorted) list.

### Dry run on `intervals=[[1,3],[6,9]], newInterval=[2,5]`
```
binary search: [2,5] inserts at index 1 → [[1,3],[2,5],[6,9]]
merge pass: [1,3] & [2,5] overlap (2<=3) → [1,5]; [6,9] separate
result = [[1,5],[6,9]]  ✓
```

### Code
```cpp
vector<vector<int>> insert(vector<vector<int>>& intervals, vector<int>& newInterval) {
    int pos = lower_bound(intervals.begin(), intervals.end(), newInterval,
        [](const vector<int>& a, const vector<int>& b){ return a[0] < b[0]; }) - intervals.begin();
    intervals.insert(intervals.begin() + pos, newInterval);
    vector<vector<int>> res;
    for (auto& cur : intervals) {
        if (!res.empty() && cur[0] <= res.back()[1])
            res.back()[1] = max(res.back()[1], cur[1]);
        else
            res.push_back(cur);
    }
    return res;
}
```
```java
public int[][] insert(int[][] intervals, int[] newInterval) {
    List<int[]> list = new ArrayList<>(Arrays.asList(intervals));
    int lo = 0, hi = list.size();
    while (lo < hi) {                       // first index with start >= newInterval[0]
        int mid = (lo + hi) / 2;
        if (list.get(mid)[0] < newInterval[0]) lo = mid + 1;
        else hi = mid;
    }
    list.add(lo, newInterval);
    List<int[]> res = new ArrayList<>();
    for (int[] cur : list) {
        if (!res.isEmpty() && cur[0] <= res.get(res.size() - 1)[1])
            res.get(res.size() - 1)[1] = Math.max(res.get(res.size() - 1)[1], cur[1]);
        else
            res.add(cur);
    }
    return res.toArray(new int[res.size()][]);
}
```
```python
import bisect
def insert(intervals, newInterval):
    starts = [iv[0] for iv in intervals]
    pos = bisect.bisect_left(starts, newInterval[0])
    intervals = intervals[:pos] + [newInterval] + intervals[pos:]
    res = []
    for cur in intervals:
        if res and cur[0] <= res[-1][1]:
            res[-1][1] = max(res[-1][1], cur[1])
        else:
            res.append(cur)
    return res
```

### Complexity
- **Time**: O(n) — the merge pass dominates even though the search is O(log n).
- **Space**: O(n).

### Verdict
A reasonable alternative, but the array insert and full merge cost O(n) anyway, so it isn't faster than Approach 1. Prefer the three-phase scan for clarity.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Three-phase scan | **O(n)** | O(n) | clearest, exploits sorted input ⭐ |
| Binary search + merge | O(n) | O(n) | search is log n but merge still linear |

---

## 🧪 Edge cases & pitfalls
- **Empty `intervals`** → just return `[newInterval]`. The three loops handle it (phases 1 and 3 do nothing).
- **`newInterval` before everything** → phase 1 empty, phase 2 empty, push new, phase 3 copies all.
- **`newInterval` after everything** → phase 1 copies all, push new last.
- **Touching endpoints** (`[1,3]` and `[3,5]`) → here they **merge** because the condition is `start <= newInterval.end` (`3 <= 3`). Insert/Merge problems treat shared endpoints as overlapping.
- **Pitfall**: using `<` instead of `<=` in phase 2 would fail to merge intervals that just touch the new one.
- **Pitfall**: forgetting to push the merged `newInterval` between phases 2 and 3.

---

## 🔗 Related problems
- **Merge Intervals** (LC 56) — the general merge when input isn't pre-sorted (next).
- **Range Module** (LC 715) — repeated insert/remove of ranges (ordered structure).
- **Interval List Intersections** (LC 986) — two-pointer over two sorted lists.
- **My Calendar I/II/III** (LC 729/731/732) — online interval booking.

---

**→ Next:** [`02-Merge-Intervals.md`](./02-Merge-Intervals.md) | [Problem set index](./00-Index.md)
