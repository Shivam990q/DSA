# Meeting Rooms II

**Platform**: LeetCode 253 · **Difficulty**: Medium · **Topics**: Array, Two Pointers, Greedy, Sorting, Heap (Priority Queue) · **Pattern**: Min-heap of end times / chronological sweep

---

## 📜 Problem Statement

Given an array of meeting time intervals `intervals` where `intervals[i] = [start_i, end_i]`, return *the minimum number of conference rooms required*.

> This is a LeetCode **premium** problem. The signature is `int minMeetingRooms(int[][] intervals)`.

### Examples

**Example 1:**
```
Input:  intervals = [[0,30],[5,10],[15,20]]
Output: 2
Explanation: [0,30] runs the whole time; [5,10] needs a second room; [15,20]
reuses that second room after [5,10] ends. Peak concurrency = 2.
```

**Example 2:**
```
Input:  intervals = [[7,10],[2,4]]
Output: 1
Explanation: The two meetings don't overlap; one room suffices.
```

**Example 3:**
```
Input:  intervals = [[1,5],[5,10],[2,7]]
Output: 2
Explanation: At time 2..5, [1,5] and [2,7] overlap → 2 rooms. [5,10] reuses a room.
```

### Constraints
```
1 <= intervals.length <= 10^4
0 <= start_i < end_i <= 10^6
```

---

## 🧠 Understanding the problem

The number of rooms needed is the **maximum number of meetings happening at the same instant** (peak concurrency). At any moment, every ongoing meeting must occupy its own room; the busiest moment dictates the count.

Two clean ways to compute peak concurrency:

1. **Min-heap of end times** — process meetings in start order. The heap holds the end times of currently-occupied rooms. Before assigning a room to the next meeting, free any room whose meeting has already ended (`heap top <= this meeting's start`). The heap's size is the number of rooms in use; its maximum over the run is the answer. (Equivalently: if the earliest-ending room is free, reuse it; else open a new one.)

2. **Chronological sweep** — separate all start times and all end times, sort each. Walk a two-pointer sweep: each start increments the running room count, each end decrements it. Track the maximum.

Both are O(n log n) and rest on the same insight.

---

## Approach 1 — Brute force (count overlaps at each start)

### Intuition
For each meeting, count how many meetings are active at its start time; the maximum such count is the rooms needed.

### Algorithm
1. For each meeting `m`: count meetings `k` with `k.start <= m.start < k.end`.
2. Track the maximum count.

### Dry run on `[[0,30],[5,10],[15,20]]`
```
at start 0: only [0,30] active → 1
at start 5: [0,30],[5,10] active → 2
at start 15:[0,30],[15,20] active → 2
max = 2  ✓
```

### Code
```cpp
int minMeetingRooms(vector<vector<int>>& intervals) {
    int n = intervals.size(), best = 0;
    for (int i = 0; i < n; i++) {
        int t = intervals[i][0], active = 0;
        for (int j = 0; j < n; j++)
            if (intervals[j][0] <= t && t < intervals[j][1]) active++;
        best = max(best, active);
    }
    return best;
}
```
```java
public int minMeetingRooms(int[][] intervals) {
    int n = intervals.length, best = 0;
    for (int i = 0; i < n; i++) {
        int t = intervals[i][0], active = 0;
        for (int j = 0; j < n; j++)
            if (intervals[j][0] <= t && t < intervals[j][1]) active++;
        best = Math.max(best, active);
    }
    return best;
}
```
```python
def minMeetingRooms(intervals):
    n = len(intervals)
    best = 0
    for i in range(n):
        t = intervals[i][0]
        active = sum(1 for j in range(n)
                     if intervals[j][0] <= t < intervals[j][1])
        best = max(best, active)
    return best
```

### Complexity
- **Time**: O(n²).
- **Space**: O(1).

### Verdict
Correct baseline that captures "peak concurrency," but quadratic. Sorting drops it to O(n log n).

---

## Approach 2 — Min-heap of end times (optimal) ⭐

### Intuition
Sort by start. Keep a min-heap of end times of in-use rooms. For each meeting, if the soonest-freeing room ends at or before this meeting starts, reuse it (pop). Always push this meeting's end. The heap size = rooms currently needed; its max is the answer (and equals the final size if you never shrink below peak — but to be safe, the size after processing all *can* be the peak because we only pop one per meeting; the standard trick is the heap size itself which never exceeds the peak).

### Algorithm
1. Sort by start.
2. Min-heap `pq` of end times.
3. For each `[s, e]`:
   - If `pq` non-empty and `pq.top() <= s` → pop (a room freed).
   - Push `e`.
4. Return `pq.size()`.

### Dry run on `[[0,30],[5,10],[15,20]]`
```
sort → [[0,30],[5,10],[15,20]]
[0,30]: pq empty → push 30. pq={30}
[5,10]: top 30 > 5 → no free → push 10. pq={10,30}
[15,20]: top 10 <= 15 → pop → push 20. pq={20,30}
final size = 2  ✓
```

### Code
```cpp
int minMeetingRooms(vector<vector<int>>& intervals) {
    sort(intervals.begin(), intervals.end());
    priority_queue<int, vector<int>, greater<int>> pq;  // end times, min on top
    for (auto& iv : intervals) {
        if (!pq.empty() && pq.top() <= iv[0]) pq.pop();  // reuse a freed room
        pq.push(iv[1]);
    }
    return pq.size();
}
```
```java
public int minMeetingRooms(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
    PriorityQueue<Integer> pq = new PriorityQueue<>();  // min-heap of end times
    for (int[] iv : intervals) {
        if (!pq.isEmpty() && pq.peek() <= iv[0]) pq.poll();
        pq.add(iv[1]);
    }
    return pq.size();
}
```
```python
import heapq
def minMeetingRooms(intervals):
    intervals.sort()
    pq = []  # min-heap of end times
    for s, e in intervals:
        if pq and pq[0] <= s:
            heapq.heappop(pq)
        heapq.heappush(pq, e)
    return len(pq)
```

### Complexity
- **Time**: O(n log n) — sort plus heap operations.
- **Space**: O(n) for the heap.

### Verdict
**Optimal and intuitive.** The heap models rooms directly: the earliest-freeing room is always the best candidate to reuse. Because we pop at most one room per meeting, the heap size only grows when a genuinely new room is required — so its size tracks peak concurrency.

---

## Approach 3 — Chronological sweep (two sorted arrays)

### Intuition
Decouple starts and ends. Sort both. Sweep time forward: whenever the next event is a start, a room is needed (`count++`); whenever it's an end, a room frees (`count--`). The maximum `count` is the answer.

### Algorithm
1. Build `starts` and `ends`, sort both.
2. Two pointers `s`, `e`. While `s < n`:
   - If `starts[s] < ends[e]` → a meeting begins before the next one ends → `count++`, `s++`, update max.
   - Else → `e++`, `count--` (a meeting ended; room freed).
3. Return max count (equivalently track `rooms` and `used`).

### Dry run on `[[0,30],[5,10],[15,20]]`
```
starts = [0,5,15], ends = [10,20,30]
s=0 start0 < end10 → count1 (max1), s=1
s=1 start5 < end10 → count2 (max2), s=2
s=2 start15 < end10? no → e=1, count1
s=2 start15 < end20 → count2 (max2), s=3 done
max = 2  ✓
```

### Code
```cpp
int minMeetingRooms(vector<vector<int>>& intervals) {
    int n = intervals.size();
    vector<int> starts(n), ends(n);
    for (int i = 0; i < n; i++) { starts[i] = intervals[i][0]; ends[i] = intervals[i][1]; }
    sort(starts.begin(), starts.end());
    sort(ends.begin(), ends.end());
    int rooms = 0, best = 0, e = 0;
    for (int s = 0; s < n; ) {
        if (starts[s] < ends[e]) { rooms++; best = max(best, rooms); s++; }
        else { rooms--; e++; }
    }
    return best;
}
```
```java
public int minMeetingRooms(int[][] intervals) {
    int n = intervals.length;
    int[] starts = new int[n], ends = new int[n];
    for (int i = 0; i < n; i++) { starts[i] = intervals[i][0]; ends[i] = intervals[i][1]; }
    Arrays.sort(starts);
    Arrays.sort(ends);
    int rooms = 0, best = 0, e = 0;
    for (int s = 0; s < n; ) {
        if (starts[s] < ends[e]) { rooms++; best = Math.max(best, rooms); s++; }
        else { rooms--; e++; }
    }
    return best;
}
```
```python
def minMeetingRooms(intervals):
    starts = sorted(iv[0] for iv in intervals)
    ends = sorted(iv[1] for iv in intervals)
    rooms = best = 0
    e = 0
    s = 0
    n = len(intervals)
    while s < n:
        if starts[s] < ends[e]:
            rooms += 1
            best = max(best, rooms)
            s += 1
        else:
            rooms -= 1
            e += 1
    return best
```

### Complexity
- **Time**: O(n log n) — two sorts.
- **Space**: O(n).

### Verdict
Equally optimal and avoids a heap. Great to mention as the "event sweep" alternative; some find it clearer than the heap.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute force | O(n²) | O(1) | baseline |
| Min-heap of ends | **O(n log n)** | O(n) | models rooms directly ⭐ |
| Chronological sweep | **O(n log n)** | O(n) | heap-free event counting |

---

## 🧪 Edge cases & pitfalls
- **Touching meetings** (`[1,5],[5,10]`) → reuse the room. Heap pops because `5 <= 5`; sweep treats `end(5)` before `start(5)` via the `<` comparison. So they need only one room.
- **All overlapping** → heap never pops → size = `n`.
- **Single meeting** → `1`.
- **Pitfall — heap comparison**: use `pq.top() <= start` (reuse if the room frees exactly when the meeting starts). Using `<` would over-allocate for back-to-back meetings.
- **Pitfall — sweep comparison**: the `starts[s] < ends[e]` (strict) ensures an end at the same time as a start frees the room first.

---

## 🔗 Related problems
- **Meeting Rooms** (LC 252) — just feasibility (previous).
- **Car Pooling** (LC 1094) — capacity vs concurrent passengers.
- **My Calendar III** (LC 732) — running max concurrency, online.
- **The Skyline Problem** (LC 218) — sweep line with a heap, harder.

---

**→ Next:** [`06-Minimum-Interval-To-Include-Query.md`](./06-Minimum-Interval-To-Include-Query.md) | **Prev:** [`04-Meeting-Rooms.md`](./04-Meeting-Rooms.md) | [Problem set index](./00-Index.md)
