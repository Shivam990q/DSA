# K Closest Points to Origin

**Platform**: LeetCode 973 · **Difficulty**: Medium · **Topics**: Array, Math, Divide and Conquer, Geometry, Sorting, Heap (Priority Queue), Quickselect · **Pattern**: Size-K max-heap / quickselect

---

## 📜 Problem Statement

Given an array of `points` where `points[i] = [xi, yi]` represents a point on the X-Y plane and an integer `k`, return the `k` closest points to the origin `(0, 0)`.

The distance between two points on the X-Y plane is the Euclidean distance (i.e., `√((x1 - x2)² + (y1 - y2)²)`).

You may return the answer in **any order**. The answer is **guaranteed to be unique** (except for the order that it is in).

### Examples

**Example 1:**
```
Input:  points = [[1,3],[-2,2]], k = 1
Output: [[-2,2]]

Explanation:
The distance between (1, 3) and the origin is √10.
The distance between (-2, 2) and the origin is √8.
Since √8 < √10, (-2, 2) is closer. We only want the closest k = 1 points, so the answer is [[-2,2]].
```

**Example 2:**
```
Input:  points = [[3,3],[5,-1],[-2,4]], k = 2
Output: [[3,3],[-2,4]]

Explanation:
Distances²: (3,3)→18, (5,-1)→26, (-2,4)→20.
The two smallest are 18 and 20 → [[3,3],[-2,4]] (any order accepted).
```

**Example 3:**
```
Input:  points = [[1,1],[2,2],[3,3]], k = 1
Output: [[1,1]]

Explanation: (1,1) has distance² = 2, the smallest.
```

### Constraints
```
1 <= k <= points.length <= 10^4
-10^4 <= xi, yi <= 10^4
```

---

## 🧠 Understanding the problem

We want the k points with the smallest distance to the origin. Two simplifications fall out immediately:

1. **Skip the square root.** Comparing `√(x²+y²)` is order-equivalent to comparing `x²+y²` because √ is monotonic. So use **squared distance** `d = x² + y²` — it's integer, exact, and faster (no floating point, no precision worries).
2. **We don't need the points sorted** — just the k smallest as a set, in any order. That means we can avoid a full O(n log n) sort.

This is a classic **top-K** problem. Three escalating ideas:
- Sort everything by distance and take the first k — simple, O(n log n).
- Keep a **max-heap of size k**: it holds the k smallest seen so far, and its root (the largest of those k) is the one to evict when a closer point arrives. O(n log k).
- **Quickselect**: partition around a pivot until the k smallest occupy the first k slots — O(n) average, the theoretical best.

---

## Approach 1 — Sort by squared distance (baseline)

### Intuition
Compute each point's squared distance, sort ascending by it, return the first k.

### Algorithm
1. Sort `points` by `x² + y²` ascending.
2. Return the first k.

### Dry run on [[3,3],[5,-1],[-2,4]], k=2
```
dists²: (3,3)=18, (5,-1)=26, (-2,4)=20
sort by dist² → [(3,3)=18, (-2,4)=20, (5,-1)=26]
take first 2 → [[3,3],[-2,4]]
```

### Code
```cpp
vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
    sort(points.begin(), points.end(), [](const vector<int>& a, const vector<int>& b) {
        return a[0]*a[0] + a[1]*a[1] < b[0]*b[0] + b[1]*b[1];
    });
    return vector<vector<int>>(points.begin(), points.begin() + k);
}
```
```java
public int[][] kClosest(int[][] points, int k) {
    Arrays.sort(points, (a, b) ->
        (a[0]*a[0] + a[1]*a[1]) - (b[0]*b[0] + b[1]*b[1]));
    return Arrays.copyOfRange(points, 0, k);
}
```
```python
def kClosest(points, k):
    points.sort(key=lambda p: p[0]*p[0] + p[1]*p[1])
    return points[:k]
```

### Complexity
- **Time**: O(n log n) — fully sorts all points.
- **Space**: O(1) or O(n) depending on the sort.

### Verdict
Clean and correct. But it does *more* work than asked: it fully orders all n points when we only need the k smallest as an unordered set. The heap and quickselect cut that down.

---

## Approach 2 — Max-heap of size k ⭐

### Intuition
Maintain a **max-heap keyed by squared distance, capped at size k**. Push each point; whenever the heap exceeds k, pop the farthest (the root of a max-heap). After processing all points, the heap holds exactly the k closest. This is ideal when **k ≪ n** or in a streaming setting where points arrive one at a time.

### Algorithm
1. For each point, push `(dist², point)` into a max-heap.
2. If heap size > k, pop the max (the current farthest among the kept set).
3. Drain the heap into the result.

### Dry run on [[3,3],[5,-1],[-2,4]], k=2
```
push (18,(3,3))            → heap top dist 18
push (26,(5,-1))           → heap {18,26}, size 2 == k
push (20,(-2,4))           → heap {18,20,26}, size 3 > 2 → pop max 26
heap = {18:(3,3), 20:(-2,4)} → result [[3,3],[-2,4]]
```

### Code
```cpp
vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
    priority_queue<pair<int, vector<int>>> maxHeap;   // max-heap by dist²
    for (auto& p : points) {
        int d = p[0]*p[0] + p[1]*p[1];
        maxHeap.push({d, p});
        if ((int)maxHeap.size() > k) maxHeap.pop();
    }
    vector<vector<int>> res;
    while (!maxHeap.empty()) { res.push_back(maxHeap.top().second); maxHeap.pop(); }
    return res;
}
```
```java
public int[][] kClosest(int[][] points, int k) {
    // max-heap by squared distance
    PriorityQueue<int[]> maxHeap = new PriorityQueue<>(
        (a, b) -> (b[0]*b[0] + b[1]*b[1]) - (a[0]*a[0] + a[1]*a[1]));
    for (int[] p : points) {
        maxHeap.offer(p);
        if (maxHeap.size() > k) maxHeap.poll();
    }
    int[][] res = new int[k][2];
    for (int i = 0; i < k; i++) res[i] = maxHeap.poll();
    return res;
}
```
```python
import heapq

def kClosest(points, k):
    max_heap = []
    for x, y in points:
        d = -(x*x + y*y)             # negate → simulate max-heap of size k
        heapq.heappush(max_heap, (d, x, y))
        if len(max_heap) > k:
            heapq.heappop(max_heap)
    return [[x, y] for _, x, y in max_heap]
```

### Complexity
- **Time**: O(n log k) — each push/pop on a size-k heap is O(log k).
- **Space**: O(k) for the heap.

### Verdict
The go-to when **k is much smaller than n** or points stream in. Bounded memory and better than a full sort when k ≪ n. This is the most commonly expected interview answer for the "Heap" topic.

---

## Approach 3 — Quickselect (optimal average) ⭐⭐

### Intuition
We don't need the k closest *sorted* — we just need them in the first k slots. **Quickselect** partitions the array around a pivot's squared distance so that everything smaller sits left. Recurse only into the side that contains index k. On average each partition halves the work, giving **O(n)** expected time.

### Algorithm
1. Define `dist(p) = x² + y²`.
2. Partition `[lo, hi]` around a pivot distance (Lomuto): elements with smaller distance move left; return the pivot's final index `p`.
3. If `p == k` → the first k slots are the answer. If `p < k` → recurse right `[p+1, hi]`. If `p > k` → recurse left `[lo, p-1]`.
4. Return the first k points.

### Dry run on [[3,3],[5,-1],[-2,4]], k=2
```
dists²: idx0=18, idx1=26, idx2=20 ; want first 2 smallest in slots [0,1]
pivot = last (idx2, dist 20):
  partition: 18<20 → keep left; 26<20? no.
  → smaller element 18 goes to front; pivot 20 lands at index 1.
  store index p=1.
p == k? k=2, p=1 → p < k → recurse right [2,2] (single element) → settled.
first 2 = [(3,3)=18, (-2,4)=20] → [[3,3],[-2,4]]
```

### Code
```cpp
class Solution {
    int dist(const vector<int>& p) { return p[0]*p[0] + p[1]*p[1]; }
    int partition(vector<vector<int>>& pts, int lo, int hi) {
        int pivot = dist(pts[hi]), i = lo;
        for (int j = lo; j < hi; j++)
            if (dist(pts[j]) < pivot) swap(pts[i++], pts[j]);
        swap(pts[i], pts[hi]);
        return i;
    }
public:
    vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
        int lo = 0, hi = points.size() - 1;
        while (lo <= hi) {
            int p = partition(points, lo, hi);
            if (p == k) break;          // first k slots are settled
            else if (p < k) lo = p + 1;
            else hi = p - 1;
        }
        return vector<vector<int>>(points.begin(), points.begin() + k);
    }
};
```
```java
class Solution {
    public int[][] kClosest(int[][] points, int k) {
        int lo = 0, hi = points.length - 1;
        while (lo <= hi) {
            int p = partition(points, lo, hi);
            if (p == k) break;
            else if (p < k) lo = p + 1;
            else hi = p - 1;
        }
        return Arrays.copyOfRange(points, 0, k);
    }
    private int partition(int[][] pts, int lo, int hi) {
        int pivot = dist(pts[hi]), i = lo;
        for (int j = lo; j < hi; j++)
            if (dist(pts[j]) < pivot) { swap(pts, i++, j); }
        swap(pts, i, hi);
        return i;
    }
    private int dist(int[] p) { return p[0]*p[0] + p[1]*p[1]; }
    private void swap(int[][] a, int i, int j) { int[] t = a[i]; a[i] = a[j]; a[j] = t; }
}
```
```python
def kClosest(points, k):
    def dist(p):
        return p[0]*p[0] + p[1]*p[1]

    def partition(lo, hi):
        pivot = dist(points[hi])
        i = lo
        for j in range(lo, hi):
            if dist(points[j]) < pivot:
                points[i], points[j] = points[j], points[i]
                i += 1
        points[i], points[hi] = points[hi], points[i]
        return i

    lo, hi = 0, len(points) - 1
    while lo <= hi:
        p = partition(lo, hi)
        if p == k:
            break
        elif p < k:
            lo = p + 1
        else:
            hi = p - 1
    return points[:k]
```

### Complexity
- **Time**: O(n) average, O(n²) worst case (pathological pivots). A randomized pivot makes the worst case astronomically unlikely.
- **Space**: O(1) — partitions in place.

### Verdict
**The theoretical optimum** for a one-shot query on a static array. Mention it when the interviewer pushes past O(n log n). The trade-offs vs. the heap: quickselect mutates the array, has a worse worst case, and isn't suited to streaming — but it's O(n) average and O(1) space.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Mutates input | When to mention |
|----------|------|-------|---------------|-----------------|
| Sort by dist² | O(n log n) | O(1)/O(n) | yes | simplest correct answer |
| Max-heap size k | O(n log k) | O(k) | no | k ≪ n, streaming ⭐ |
| Quickselect | **O(n) avg** | O(1) | yes | one-shot static array, push for optimum ⭐⭐ |

The classic dialogue: heap trades a tiny bit of speed for **bounded O(k) memory** and **streaming** support; quickselect gives **O(n) average** but mutates the array and has an O(n²) worst case.

---

## 🧪 Edge cases & pitfalls
- **k == n**: every point qualifies; all approaches return all points.
- **Skip the sqrt**: always compare squared distances. Taking the root invites floating-point error and is pure waste.
- **Overflow**: with `|coord| ≤ 10⁴`, `x²+y²` ≤ 2·10⁸ — fits comfortably in 32-bit `int`. With larger coordinates, use 64-bit.
- **Ties / non-unique distances**: the problem guarantees a unique answer set, so tie-breaking order doesn't matter; return any valid set.
- **Pitfall (Java heap comparator)**: for a *max*-heap by distance, the comparator must order **larger distance first** (`b - a` on distances). Reversing it turns it into a min-heap and keeps the wrong k.
- **Pitfall (Python)**: comparing raw point lists in the tuple can throw if distances tie; include coordinates as tiebreakers (as done) or store an index to keep tuples comparable.
- **Pitfall (quickselect)**: using `p == k` vs `p == k-1` — here index `k` is the first *excluded* slot, so stopping at `p == k` leaves slots `[0, k-1]` settled. Off-by-one here is the most common bug.

---

## 🔗 Related problems
- **Kth Largest Element in an Array** (LC 215) — the pure quickselect / size-k heap sibling. *(file 04)*
- **Top K Frequent Elements** (LC 347) — top-K by frequency (heap or bucket sort).
- **Kth Largest Element in a Stream** (LC 703) — streaming size-k heap. *(file 01)*
- **Sort Array by Increasing Frequency** (LC 1636) — sorting with a custom key.

---

**→ Next:** [`04-Kth-Largest-Element-In-Array.md`](./04-Kth-Largest-Element-In-Array.md) | **← Prev:** [`02-Last-Stone-Weight.md`](./02-Last-Stone-Weight.md) | Back to [`00-Index.md`](./00-Index.md)
