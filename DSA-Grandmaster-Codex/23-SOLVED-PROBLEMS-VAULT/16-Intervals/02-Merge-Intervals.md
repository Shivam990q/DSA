# Merge Intervals

**Platform**: LeetCode 56 · **Difficulty**: Medium · **Topics**: Array, Sorting · **Pattern**: Sort by start + sweep

---

## 📜 Problem Statement

Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return *an array of the non-overlapping intervals that cover all the intervals in the input*.

### Examples

**Example 1:**
```
Input:  intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].
```

**Example 2:**
```
Input:  intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: Intervals [1,4] and [4,5] are considered overlapping (they touch).
```

**Example 3:**
```
Input:  intervals = [[1,4],[0,4]]
Output: [[0,4]]
Explanation: After sorting by start → [[0,4],[1,4]], merge into [0,4].
```

### Constraints
```
1 <= intervals.length <= 10^4
intervals[i].length == 2
0 <= start_i <= end_i <= 10^4
```

---

## 🧠 Understanding the problem

Unlike Insert Interval, the input here is **unsorted**. The instant we sort by start, overlapping intervals become **adjacent** — there's no way for an interval to overlap one far down the list without also overlapping its sorted neighbors in between. So after sorting, a single pass that compares each interval to the *last merged* one suffices.

The overlap test after sorting: the current interval `[s, e]` overlaps the last merged interval `[ls, le]` iff `s <= le` (we already know `s >= ls` because it comes later in start order). When they overlap, the merged end becomes `max(le, e)` — note `e` might be *smaller* than `le` if the current interval is nested inside.

---

## Approach 1 — Brute force (repeated pairwise merging)

### Intuition
Repeatedly scan for any two intervals that overlap and merge them, until no overlaps remain. This mirrors the definition but does lots of redundant rescanning.

### Algorithm
1. Loop: find any pair `(i, j)` that overlaps.
2. Merge them into one, remove the other, restart the scan.
3. Stop when a full scan finds no overlap.

### Dry run on `[[1,3],[2,6],[8,10],[15,18]]`
```
[1,3] & [2,6] overlap → merge [1,6]; list = [[1,6],[8,10],[15,18]]
rescan: no more overlaps → done
result = [[1,6],[8,10],[15,18]]
```

### Code
```cpp
vector<vector<int>> merge(vector<vector<int>>& intervals) {
    vector<vector<int>> v = intervals;
    bool changed = true;
    while (changed) {
        changed = false;
        for (int i = 0; i < (int)v.size() && !changed; i++)
            for (int j = i + 1; j < (int)v.size(); j++)
                if (v[i][0] <= v[j][1] && v[j][0] <= v[i][1]) {  // overlap
                    v[i][0] = min(v[i][0], v[j][0]);
                    v[i][1] = max(v[i][1], v[j][1]);
                    v.erase(v.begin() + j);
                    changed = true;
                    break;
                }
    }
    return v;
}
```
```java
public int[][] merge(int[][] intervals) {
    List<int[]> v = new ArrayList<>();
    for (int[] iv : intervals) v.add(iv.clone());
    boolean changed = true;
    while (changed) {
        changed = false;
        outer:
        for (int i = 0; i < v.size(); i++)
            for (int j = i + 1; j < v.size(); j++)
                if (v.get(i)[0] <= v.get(j)[1] && v.get(j)[0] <= v.get(i)[1]) {
                    v.get(i)[0] = Math.min(v.get(i)[0], v.get(j)[0]);
                    v.get(i)[1] = Math.max(v.get(i)[1], v.get(j)[1]);
                    v.remove(j);
                    changed = true;
                    break outer;
                }
    }
    return v.toArray(new int[v.size()][]);
}
```
```python
def merge(intervals):
    v = [iv[:] for iv in intervals]
    changed = True
    while changed:
        changed = False
        for i in range(len(v)):
            for j in range(i + 1, len(v)):
                if v[i][0] <= v[j][1] and v[j][0] <= v[i][1]:
                    v[i][0] = min(v[i][0], v[j][0])
                    v[i][1] = max(v[i][1], v[j][1])
                    v.pop(j)
                    changed = True
                    break
            if changed:
                break
    return v
```

### Complexity
- **Time**: O(n³) in the worst case (each merge triggers a fresh O(n²) scan).
- **Space**: O(n).

### Verdict
Correct but wasteful. Sorting removes all the rescanning.

---

## Approach 2 — Sort by start, then sweep (optimal) ⭐

### Intuition
Sort by start. Maintain a result list; for each interval, either extend the last result interval (if they overlap) or append it as a fresh interval.

### Algorithm
1. Sort `intervals` by start (ties by end, naturally via lexicographic sort).
2. For each `cur`:
   - If `res` non-empty and `cur.start <= res.back().end` → `res.back().end = max(res.back().end, cur.end)`.
   - Else → `res.push_back(cur)`.
3. Return `res`.

### Dry run on `[[1,3],[2,6],[8,10],[15,18]]`
```
sort → [[1,3],[2,6],[8,10],[15,18]]
[1,3] → res=[[1,3]]
[2,6] → 2<=3 → extend → res=[[1,6]]
[8,10]→ 8>6 → append → res=[[1,6],[8,10]]
[15,18]→15>10 → append → res=[[1,6],[8,10],[15,18]]  ✓
```

### Code
```cpp
vector<vector<int>> merge(vector<vector<int>>& intervals) {
    sort(intervals.begin(), intervals.end());
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
public int[][] merge(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
    List<int[]> res = new ArrayList<>();
    for (int[] cur : intervals) {
        if (!res.isEmpty() && cur[0] <= res.get(res.size() - 1)[1])
            res.get(res.size() - 1)[1] = Math.max(res.get(res.size() - 1)[1], cur[1]);
        else
            res.add(cur);
    }
    return res.toArray(new int[res.size()][]);
}
```
```python
def merge(intervals):
    intervals.sort()
    res = []
    for cur in intervals:
        if res and cur[0] <= res[-1][1]:
            res[-1][1] = max(res[-1][1], cur[1])
        else:
            res.append(cur)
    return res
```

### Complexity
- **Time**: O(n log n) — dominated by the sort.
- **Space**: O(n) for the output (O(log n) to O(n) for the sort itself).

### Verdict
**Optimal.** The sort is the only superlinear step, and the sweep is five lines. This is the canonical interval template.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Repeated pairwise | O(n³) | O(n) | baseline; never use in practice |
| Sort + sweep | **O(n log n)** | O(n) | optimal, the template ⭐ |

You generally can't beat O(n log n) here in the comparison model, because merging lets you sort numbers (a reduction from sorting), so the sort is inherent.

---

## 🧪 Edge cases & pitfalls
- **Touching endpoints** (`[1,4],[4,5]`) → **merge** to `[1,5]` (the condition `cur[0] <= res.back()[1]` is `4 <= 4`). If a variant says touching does *not* merge, use `<`.
- **Nested interval** (`[1,10],[2,3]`) → after sorting, `max(10, 3)` keeps the larger end `10`. Don't blindly assign `cur.end`.
- **Single interval** → returned unchanged.
- **Already sorted / all disjoint** → each interval appended once.
- **Pitfall**: assigning `res.back().end = cur.end` instead of `max(...)` corrupts nested intervals.
- **Pitfall**: sorting by end instead of start breaks the adjacency guarantee for merging.

---

## 🔗 Related problems
- **Insert Interval** (LC 57) — merge a single new interval into a sorted list (previous).
- **Non-Overlapping Intervals** (LC 435) — count removals (next).
- **Meeting Rooms / II** (LC 252/253) — feasibility and room count.
- **Interval List Intersections** (LC 986) — intersect two sorted lists.

---

**→ Next:** [`03-Non-Overlapping-Intervals.md`](./03-Non-Overlapping-Intervals.md) | **Prev:** [`01-Insert-Interval.md`](./01-Insert-Interval.md) | [Problem set index](./00-Index.md)
