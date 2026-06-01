# Meeting Rooms

**Platform**: LeetCode 252 · **Difficulty**: Easy · **Topics**: Array, Sorting · **Pattern**: Sort by start + adjacent conflict check

---

## 📜 Problem Statement

Given an array of meeting time `intervals` where `intervals[i] = [start_i, end_i]`, determine if a person could attend **all** meetings.

> This is a LeetCode **premium** problem. The signature is `boolean canAttendMeetings(int[][] intervals)`.

### Examples

**Example 1:**
```
Input:  intervals = [[0,30],[5,10],[15,20]]
Output: false
Explanation: [0,30] overlaps [5,10] (and [15,20]); the person can't attend all.
```

**Example 2:**
```
Input:  intervals = [[7,10],[2,4]]
Output: true
Explanation: Sorted → [[2,4],[7,10]]; 4 <= 7, no overlap.
```

**Example 3:**
```
Input:  intervals = [[1,5],[5,8]]
Output: true
Explanation: Meetings touching at a point (5) don't conflict.
```

### Constraints
```
0 <= intervals.length <= 10^4
intervals[i].length == 2
0 <= start_i < end_i <= 10^6
```

---

## 🧠 Understanding the problem

One person, one room: they can attend everything iff **no two meetings overlap**. After sorting by start time, a conflict can only happen between **consecutive** meetings — if meeting `i` starts before meeting `i−1` ends. (If consecutive meetings don't overlap, no non-consecutive pair can either, since starts only increase.)

So: sort by start, then check each adjacent pair. The touching case (`end == nextStart`) is **not** a conflict — back-to-back meetings are fine.

---

## Approach 1 — Brute force (all pairs)

### Intuition
Directly test every pair of meetings for overlap.

### Algorithm
1. For every pair `(i, j)`: if they overlap (`a.start < b.end && b.start < a.end`) → return `false`.
2. Return `true`.

### Dry run on `[[0,30],[5,10],[15,20]]`
```
[0,30] vs [5,10]: 0<10 && 5<30 → overlap → return false
```

### Code
```cpp
bool canAttendMeetings(vector<vector<int>>& intervals) {
    int n = intervals.size();
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (intervals[i][0] < intervals[j][1] &&
                intervals[j][0] < intervals[i][1])
                return false;
    return true;
}
```
```java
public boolean canAttendMeetings(int[][] intervals) {
    int n = intervals.length;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (intervals[i][0] < intervals[j][1] &&
                intervals[j][0] < intervals[i][1])
                return false;
    return true;
}
```
```python
def canAttendMeetings(intervals):
    n = len(intervals)
    for i in range(n):
        for j in range(i + 1, n):
            if intervals[i][0] < intervals[j][1] and intervals[j][0] < intervals[i][1]:
                return False
    return True
```

### Complexity
- **Time**: O(n²).
- **Space**: O(1).

### Verdict
Correct, but the O(n²) pairwise testing is unnecessary once you realize sorting localizes conflicts to neighbors.

---

## Approach 2 — Sort by start, check adjacent (optimal) ⭐

### Intuition
Sort by start. A clash exists iff some meeting begins before its predecessor ends. One linear scan over adjacent pairs decides it.

### Algorithm
1. Sort `intervals` by start.
2. For `i` from `1` to `n−1`: if `intervals[i].start < intervals[i−1].end` → return `false`.
3. Return `true`.

### Dry run on `[[0,30],[5,10],[15,20]]`
```
sort → [[0,30],[5,10],[15,20]] (already by start)
i=1: 5 < 30 → conflict → false  ✓
```

### Code
```cpp
bool canAttendMeetings(vector<vector<int>>& intervals) {
    sort(intervals.begin(), intervals.end());
    for (int i = 1; i < (int)intervals.size(); i++)
        if (intervals[i][0] < intervals[i-1][1]) return false;
    return true;
}
```
```java
public boolean canAttendMeetings(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
    for (int i = 1; i < intervals.length; i++)
        if (intervals[i][0] < intervals[i-1][1]) return false;
    return true;
}
```
```python
def canAttendMeetings(intervals):
    intervals.sort()
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False
    return True
```

### Complexity
- **Time**: O(n log n) — the sort dominates; the scan is O(n).
- **Space**: O(1) extra.

### Verdict
**Optimal.** Sort + adjacent check is the cleanest possible solution. This is also the warm-up for Meeting Rooms II.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute force pairs | O(n²) | O(1) | baseline |
| Sort + adjacent | **O(n log n)** | O(1) | optimal ⭐ |

---

## 🧪 Edge cases & pitfalls
- **Empty or single meeting** → `true` (nothing to conflict).
- **Touching meetings** (`[1,5],[5,8]`) → no conflict; the test is strict `<` (`5 < 5` is false).
- **Pitfall**: using `<=` would wrongly flag back-to-back meetings as conflicting.
- **Pitfall**: forgetting to sort — adjacency only localizes conflicts after sorting by start.
- **Duplicate meetings** (`[1,5],[1,5]`) → conflict (`1 < 5`).

---

## 🔗 Related problems
- **Meeting Rooms II** (LC 253) — minimum rooms when overlaps are allowed (next).
- **Merge Intervals** (LC 56) — merge instead of detect.
- **Non-Overlapping Intervals** (LC 435) — minimum removals.
- **Car Pooling** (LC 1094) — capacity over overlapping trips.

---

**→ Next:** [`05-Meeting-Rooms-II.md`](./05-Meeting-Rooms-II.md) | **Prev:** [`03-Non-Overlapping-Intervals.md`](./03-Non-Overlapping-Intervals.md) | [Problem set index](./00-Index.md)
