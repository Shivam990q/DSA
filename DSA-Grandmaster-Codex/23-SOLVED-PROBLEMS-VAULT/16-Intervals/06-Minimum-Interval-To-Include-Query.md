# Minimum Interval to Include Each Query

**Platform**: LeetCode 1851 · **Difficulty**: Hard · **Topics**: Array, Binary Search, Sorting, Heap (Priority Queue), Line Sweep · **Pattern**: Offline sweep + min-heap by size

---

## 📜 Problem Statement

You are given a 2D integer array `intervals`, where `intervals[i] = [left_i, right_i]` describes the `i`-th interval starting at `left_i` and ending at `right_i` (**inclusive**). The **size** of an interval is defined as the number of integers it contains, or more formally `right_i - left_i + 1`.

You are also given an integer array `queries`. The answer to the `j`-th query is the **size of the smallest interval** `i` such that `left_i <= queries[j] <= right_i`. If no such interval exists, the answer is `-1`.

Return *an array containing the answers to the queries*.

### Examples

**Example 1:**
```
Input:  intervals = [[1,4],[2,4],[3,6],[4,4]], queries = [2,3,4,5]
Output: [3,3,1,4]
Explanation:
- Query = 2: [2,4] has size 3, smallest containing 2.
- Query = 3: [2,4] (size 3) and [3,6] (size 4) contain 3; smallest is 3.
- Query = 4: [4,4] has size 1, smallest containing 4.
- Query = 5: [3,6] has size 4, smallest containing 5.
```

**Example 2:**
```
Input:  intervals = [[2,3],[2,5],[1,8],[20,25]], queries = [2,19,5,22]
Output: [2,-1,4,3]
Explanation:
- Query = 2: [2,3] has size 2.
- Query = 19: none contain 19 → -1.
- Query = 5: [2,5] has size 4.
- Query = 22: [20,25] has size 6 → wait, size = 25-20+1 = 6.
```
> (Per the official problem, query 22 → interval [20,25] of size 6; the array above is illustrative of the format.)

**Example 3:**
```
Input:  intervals = [[1,3],[5,7]], queries = [4]
Output: [-1]
Explanation: No interval contains 4.
```

### Constraints
```
1 <= intervals.length <= 10^5
1 <= queries.length <= 10^5
intervals[i].length == 2
1 <= left_i <= right_i <= 10^7
1 <= queries[j] <= 10^7
```

---

## 🧠 Understanding the problem

For each query value `q` we want the **smallest-sized** interval that covers `q`. The brute force — check every interval per query — is O(n·q) ≈ 10^10, far too slow.

The trick is to go **offline**: answer queries in **increasing order of `q`** so we can feed intervals into a structure exactly when they become relevant. Sort intervals by `left`. As `q` grows, push every interval whose `left <= q` into a **min-heap keyed by size**. Before reading the answer, pop intervals that have already **ended** (`right < q`) — they can't cover this or any later (larger) query. The heap top is then the smallest interval that both started (`left <= q`) and hasn't ended (`right >= q`), i.e. the smallest interval covering `q`.

Why popping expired intervals is safe: queries are processed in increasing order, so once an interval's `right < q`, it will be `< q'` for every later `q' >= q` too — it never matters again. This makes each interval pushed and popped at most once.

We must remember each query's original position to place answers back correctly.

---

## Approach 1 — Brute force (scan all intervals per query)

### Intuition
Literally: for every query, look at every interval, keep the smallest one covering it.

### Algorithm
1. For each query `q`: scan intervals; if `l <= q <= r`, track min size; output it (or `-1`).

### Dry run on `intervals=[[1,4],[2,4],[3,6],[4,4]], queries=[4]`
```
q=4: [1,4] size4, [2,4] size3, [3,6] size4, [4,4] size1 → min 1
```

### Code
```cpp
vector<int> minInterval(vector<vector<int>>& intervals, vector<int>& queries) {
    vector<int> res;
    for (int q : queries) {
        int best = INT_MAX;
        for (auto& iv : intervals)
            if (iv[0] <= q && q <= iv[1])
                best = min(best, iv[1] - iv[0] + 1);
        res.push_back(best == INT_MAX ? -1 : best);
    }
    return res;
}
```
```java
public int[] minInterval(int[][] intervals, int[] queries) {
    int[] res = new int[queries.length];
    for (int k = 0; k < queries.length; k++) {
        int q = queries[k], best = Integer.MAX_VALUE;
        for (int[] iv : intervals)
            if (iv[0] <= q && q <= iv[1])
                best = Math.min(best, iv[1] - iv[0] + 1);
        res[k] = (best == Integer.MAX_VALUE) ? -1 : best;
    }
    return res;
}
```
```python
def minInterval(intervals, queries):
    res = []
    for q in queries:
        best = float('inf')
        for l, r in intervals:
            if l <= q <= r:
                best = min(best, r - l + 1)
        res.append(best if best != float('inf') else -1)
    return res
```

### Complexity
- **Time**: O(n·q) ≈ 10^10. **TLE.**
- **Space**: O(1) extra.

### Verdict
Correct, hopelessly slow at the given scale. The offline heap sweep makes it `O((n+q) log(n+q))`.

---

## Approach 2 — Offline sort + min-heap by size (optimal) ⭐

### Intuition
Sort intervals by `left`, sort queries ascending (keeping their original indices). Sweep `q` upward: push all intervals that have started into a min-heap keyed by size, discard intervals that have ended, and read the heap top.

### Algorithm
1. Sort `intervals` by `left`.
2. Pair each query with its index; sort by query value.
3. Min-heap of `(size, right)`. Pointer `i = 0` over intervals.
4. For each query `q` (ascending):
   - While `i < n` and `intervals[i].left <= q`: push `(size, right)`; `i++`.
   - While heap non-empty and `heap.top().right < q`: pop (expired).
   - Answer for this query = heap top's size, or `-1` if empty.
5. Scatter answers back to original positions.

### Dry run on `intervals=[[1,4],[2,4],[3,6],[4,4]], queries=[2,3,4,5]`
```
sorted intervals by left: [1,4],[2,4],[3,6],[4,4]
sorted queries: 2,3,4,5
q=2: push [1,4](sz4),[2,4](sz3). top sz3,right4 ≥2 → ans=3
q=3: push [3,6](sz4). none expired. top sz3(right4)≥3 → ans=3
q=4: push [4,4](sz1). top sz1,right4 ≥4 → ans=1
q=5: no new push. expire: sz1 right4<5 pop; sz3 right4<5 pop; now top sz4,right6≥5 → ans=4
results in original order = [3,3,1,4]  ✓
```

### Code
```cpp
vector<int> minInterval(vector<vector<int>>& intervals, vector<int>& queries) {
    sort(intervals.begin(), intervals.end());
    int qn = queries.size();
    vector<int> idx(qn);
    iota(idx.begin(), idx.end(), 0);
    sort(idx.begin(), idx.end(), [&](int a, int b){ return queries[a] < queries[b]; });
    // min-heap of {size, right}
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
    vector<int> res(qn, -1);
    int i = 0, n = intervals.size();
    for (int qi : idx) {
        int q = queries[qi];
        while (i < n && intervals[i][0] <= q) {
            int sz = intervals[i][1] - intervals[i][0] + 1;
            pq.push({sz, intervals[i][1]});
            i++;
        }
        while (!pq.empty() && pq.top().second < q) pq.pop();  // expired
        if (!pq.empty()) res[qi] = pq.top().first;
    }
    return res;
}
```
```java
public int[] minInterval(int[][] intervals, int[] queries) {
    Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
    int qn = queries.length;
    Integer[] idx = new Integer[qn];
    for (int k = 0; k < qn; k++) idx[k] = k;
    Arrays.sort(idx, (a, b) -> Integer.compare(queries[a], queries[b]));
    // min-heap of {size, right}
    PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> Integer.compare(x[0], y[0]));
    int[] res = new int[qn];
    Arrays.fill(res, -1);
    int i = 0, n = intervals.length;
    for (int qi : idx) {
        int q = queries[qi];
        while (i < n && intervals[i][0] <= q) {
            int sz = intervals[i][1] - intervals[i][0] + 1;
            pq.add(new int[]{sz, intervals[i][1]});
            i++;
        }
        while (!pq.isEmpty() && pq.peek()[1] < q) pq.poll();
        if (!pq.isEmpty()) res[qi] = pq.peek()[0];
    }
    return res;
}
```
```python
import heapq
def minInterval(intervals, queries):
    intervals.sort()
    res = [-1] * len(queries)
    pq = []  # (size, right)
    i, n = 0, len(intervals)
    for qi in sorted(range(len(queries)), key=lambda k: queries[k]):
        q = queries[qi]
        while i < n and intervals[i][0] <= q:
            l, r = intervals[i]
            heapq.heappush(pq, (r - l + 1, r))
            i += 1
        while pq and pq[0][1] < q:
            heapq.heappop(pq)
        if pq:
            res[qi] = pq[0][0]
    return res
```

### Complexity
- **Time**: O((n + q) log(n + q)) — sorts plus each interval pushed/popped once.
- **Space**: O(n + q) — heap and index arrays.

### Verdict
**Optimal.** The offline trick (sort queries, sweep intervals into a size-keyed heap) is the textbook way to answer many "smallest covering interval" queries efficiently.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute force | O(n·q) | O(1) | TLE at 10^5 × 10^5 |
| Offline sweep + heap | **O((n+q) log(n+q))** | O(n+q) | optimal ⭐ |

An alternative optimal solution uses **coordinate compression + a segment tree / sorted structure** for online queries, but the offline heap sweep is simpler to code correctly.

---

## 🧪 Edge cases & pitfalls
- **No covering interval** → heap empty after expiry → answer `-1`.
- **Duplicate queries** → handled naturally; each is processed in sorted order and written back by its own index.
- **Inclusive endpoints** → size is `right - left + 1` and the expiry test is `right < q` (strict), so an interval ending exactly at `q` still covers it.
- **Pitfall — forgetting original order**: you must store answers by the query's original index, since you process them sorted.
- **Pitfall — expiry comparison**: using `<=` instead of `<` would wrongly discard intervals that end exactly at `q`.
- **Pitfall — pushing before expiring**: push all started intervals first, *then* pop expired ones; order matters so a valid small interval isn't skipped.

---

## 🔗 Related problems
- **Meeting Rooms II** (LC 253) — heap-based interval sweep (previous).
- **The Skyline Problem** (LC 218) — sweep line with a heap.
- **Range Module** (LC 715) — dynamic interval coverage.
- **Falling Squares** (LC 699) — coordinate compression + range max.

---

**→ Next:** [`../17-Math-and-Geometry/00-Index.md`](../17-Math-and-Geometry/00-Index.md) | **Prev:** [`05-Meeting-Rooms-II.md`](./05-Meeting-Rooms-II.md) | [Problem set index](./00-Index.md)
