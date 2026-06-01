# Find Median from Data Stream

**Platform**: LeetCode 295 · **Difficulty**: Hard · **Topics**: Two Pointers, Design, Sorting, Heap (Priority Queue), Data Stream · **Pattern**: Two balanced heaps

---

## 📜 Problem Statement

The **median** is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.

- For example, for `arr = [2,3,4]`, the median is `3`.
- For example, for `arr = [2,3]`, the median is `(2 + 3) / 2 = 2.5`.

Implement the `MedianFinder` class:

- `MedianFinder()` initializes the `MedianFinder` object.
- `void addNum(int num)` adds the integer `num` from the data stream to the data structure.
- `double findMedian()` returns the median of all elements so far. Answers within `10^-5` of the actual answer will be accepted.

### Examples

**Example 1:**
```
Input:
["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
[[], [1], [2], [], [3], []]

Output:
[null, null, null, 1.5, null, 2.0]

Explanation:
MedianFinder medianFinder = new MedianFinder();
medianFinder.addNum(1);    // arr = [1]
medianFinder.addNum(2);    // arr = [1, 2]
medianFinder.findMedian(); // return 1.5 (i.e., (1 + 2) / 2)
medianFinder.addNum(3);    // arr = [1, 2, 3]
medianFinder.findMedian(); // return 2.0
```

**Example 2:**
```
Input:
["MedianFinder","addNum","findMedian","addNum","findMedian"]
[[],[2],[],[3],[]]

Output:
[null,null,2.0,null,2.5]

Explanation:
After add(2): median of [2] = 2.0.
After add(3): median of [2,3] = 2.5.
```

**Example 3:**
```
Input:
["MedianFinder","addNum","addNum","addNum","addNum","addNum","findMedian"]
[[],[5],[1],[3],[2],[4],[]]

Output:
[null,null,null,null,null,null,3.0]

Explanation: Sorted = [1,2,3,4,5]; the middle value is 3.0.
```

### Constraints
```
-10^5 <= num <= 10^5
There will be at least one element in the data structure before calling findMedian.
At most 5 * 10^4 calls will be made to addNum and findMedian.

Follow up:
- If all integer numbers from the stream are in the range [0, 100], how would you optimize your solution?
- If 99% of all integer numbers from the stream are in the range [0, 100], how would you optimize your solution?
```

---

## 🧠 Understanding the problem

We get a *stream* of numbers and must answer "what's the median so far?" at any time. The median depends only on the **middle of the sorted order** — we never need the elements that are far from the center for the query itself, but we must be ready as new numbers shift the center.

Naive idea: keep a sorted array and binary-search the insertion point on every `addNum`. Lookup is O(1) but the **insert shifts elements**, costing O(n). With 5·10⁴ operations that's up to ~10⁹ shifts — too slow.

The elegant idea: split the data into **two halves** and keep each half in a heap.
- A **max-heap `lo`** holds the **smaller half**; its root is the *largest* of the small numbers.
- A **min-heap `hi`** holds the **larger half**; its root is the *smallest* of the large numbers.

Keep the two heaps **balanced** in size (differ by at most 1). Then:
- If the total count is **odd**, one heap has the extra element and its root **is** the median.
- If **even**, the median is the average of the two roots.

Every `addNum` is O(log n) (a couple of heap pushes/pops), and `findMedian` is O(1) (just read the roots). This is the textbook "two heaps" pattern.

---

## Approach 1 — Sorted array + binary-search insert (baseline)

### Intuition
Maintain the numbers in sorted order. Use binary search to find where a new number belongs, insert it there, and the median is read directly from the middle index/indices.

### Algorithm
1. `addNum(num)`: binary-search the insertion index in the sorted list; insert `num` there.
2. `findMedian()`: if size is odd, return the middle element; if even, average the two middle elements.

### Dry run on add 1, add 2, findMedian, add 3, findMedian
```
add 1 → [1]
add 2 → binary search → insert after 1 → [1,2]
findMedian → even → (1+2)/2 = 1.5
add 3 → insert at end → [1,2,3]
findMedian → odd → middle index 1 → 2.0
```

### Code
```cpp
class MedianFinder {
    vector<int> arr;
public:
    MedianFinder() {}
    void addNum(int num) {
        int pos = lower_bound(arr.begin(), arr.end(), num) - arr.begin();
        arr.insert(arr.begin() + pos, num);   // O(n) shift
    }
    double findMedian() {
        int n = arr.size();
        if (n % 2 == 1) return arr[n / 2];
        return (arr[n / 2 - 1] + arr[n / 2]) / 2.0;
    }
};
```
```java
class MedianFinder {
    private List<Integer> arr = new ArrayList<>();

    public MedianFinder() {}
    public void addNum(int num) {
        int pos = Collections.binarySearch(arr, num);
        if (pos < 0) pos = -(pos + 1);          // insertion point
        arr.add(pos, num);                       // O(n) shift
    }
    public double findMedian() {
        int n = arr.size();
        if (n % 2 == 1) return arr.get(n / 2);
        return (arr.get(n / 2 - 1) + arr.get(n / 2)) / 2.0;
    }
}
```
```python
import bisect

class MedianFinder:
    def __init__(self):
        self.arr = []

    def addNum(self, num: int) -> None:
        bisect.insort(self.arr, num)             # O(n) shift under the hood

    def findMedian(self) -> float:
        n = len(self.arr)
        if n % 2 == 1:
            return float(self.arr[n // 2])
        return (self.arr[n // 2 - 1] + self.arr[n // 2]) / 2.0
```

### Complexity
- **Time**: `addNum` O(n) (binary search O(log n) but the array shift dominates at O(n)); `findMedian` O(1).
- **Space**: O(n).

### Verdict
Simple and exact, but the O(n) insertion per add makes the whole sequence O(n²) — too slow at the upper constraint. The two-heap approach drops `addNum` to O(log n).

---

## Approach 2 — Two balanced heaps (optimal) ⭐

### Intuition
Hold the smaller half in a **max-heap `lo`** and the larger half in a **min-heap `hi`**. The two roots straddle the median. Keep `|size(lo) - size(hi)| ≤ 1`, with `lo` allowed to hold the extra element. Then the median is `lo.top()` (odd total) or the average of both tops (even total).

The balancing trick on each `addNum`: push to `lo`, then move `lo`'s top to `hi` (this guarantees every element of `lo` ≤ every element of `hi`), then if `hi` got bigger than `lo`, move `hi`'s top back to `lo`. Two heaps, always sorted relative to each other.

### Algorithm
1. `addNum(num)`:
   - Push `num` onto `lo` (max-heap).
   - Move `lo.top()` to `hi` (min-heap) — keeps the value-ordering invariant `max(lo) ≤ min(hi)`.
   - If `hi.size() > lo.size()`, move `hi.top()` back to `lo` — keeps `lo` as the (possibly) larger heap.
2. `findMedian()`:
   - If `lo.size() > hi.size()` → return `lo.top()`.
   - Else → return `(lo.top() + hi.top()) / 2`.

### Dry run on add 1, add 2, findMedian, add 3, findMedian
```
add 1: lo.push(1) → lo=[1]; move top to hi → lo=[], hi=[1];
       hi.size(1) > lo.size(0) → move back → lo=[1], hi=[]
add 2: lo.push(2) → lo=[2,1] (max-top 2); move top 2 to hi → lo=[1], hi=[2];
       hi.size(1) == lo.size(1) → no rebalance
findMedian: sizes equal → (lo.top 1 + hi.top 2)/2 = 1.5 ✓
add 3: lo.push(3) → lo=[3,1]; move top 3 to hi → lo=[1], hi=[2,3] (min-top 2);
       hi.size(2) > lo.size(1) → move back hi.top 2 → lo=[2,1], hi=[3]
findMedian: lo.size(2) > hi.size(1) → lo.top = 2 → 2.0 ✓
```

### Code
```cpp
class MedianFinder {
    priority_queue<int> lo;                                  // max-heap (smaller half)
    priority_queue<int, vector<int>, greater<int>> hi;       // min-heap (larger half)
public:
    MedianFinder() {}
    void addNum(int num) {
        lo.push(num);
        hi.push(lo.top()); lo.pop();           // enforce max(lo) <= min(hi)
        if (hi.size() > lo.size()) {           // keep lo >= hi in size
            lo.push(hi.top()); hi.pop();
        }
    }
    double findMedian() {
        if (lo.size() > hi.size()) return lo.top();
        return (lo.top() + hi.top()) / 2.0;
    }
};
```
```java
class MedianFinder {
    private PriorityQueue<Integer> lo;   // max-heap (smaller half)
    private PriorityQueue<Integer> hi;   // min-heap (larger half)

    public MedianFinder() {
        lo = new PriorityQueue<>(Collections.reverseOrder());
        hi = new PriorityQueue<>();
    }
    public void addNum(int num) {
        lo.offer(num);
        hi.offer(lo.poll());                 // enforce max(lo) <= min(hi)
        if (hi.size() > lo.size()) {         // keep lo >= hi in size
            lo.offer(hi.poll());
        }
    }
    public double findMedian() {
        if (lo.size() > hi.size()) return lo.peek();
        return (lo.peek() + hi.peek()) / 2.0;
    }
}
```
```python
import heapq

class MedianFinder:
    def __init__(self):
        self.lo = []     # max-heap (store negatives), smaller half
        self.hi = []     # min-heap, larger half

    def addNum(self, num: int) -> None:
        heapq.heappush(self.lo, -num)
        # move the largest of lo into hi
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        # keep lo at least as large as hi in size
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self) -> float:
        if len(self.lo) > len(self.hi):
            return float(-self.lo[0])
        return (-self.lo[0] + self.hi[0]) / 2.0
```

### Complexity
- **Time**: `addNum` O(log n) (a constant number of heap pushes/pops); `findMedian` O(1).
- **Space**: O(n) across the two heaps.

### Verdict
**The intended Hard answer.** O(log n) inserts, O(1) median reads, and a clean invariant (`max(lo) ≤ min(hi)`, sizes within 1). The "push-then-shuffle" balancing keeps both correctness conditions — value ordering and size balance — in just three lines.

---

## 📎 Follow-up answers

- **All numbers in `[0, 100]`**: use **counting / a bucket array** of size 101. `addNum` increments a counter in O(1); `findMedian` scans the 101 buckets to find the middle position in O(100) = O(1). No heaps needed.
- **99% of numbers in `[0, 100]`**: use the bucket array for the in-range 99%, and keep two small overflow structures (e.g., a sorted list or two heaps) for the rare out-of-range values below 0 and above 100. Combine the bucket counts with the overflow sizes to locate the median. The common case stays O(1).

---

## ⚖️ Approach comparison

| Approach | addNum | findMedian | Space | When to mention |
|----------|--------|------------|-------|-----------------|
| Sorted array + insert | O(n) | O(1) | O(n) | baseline / small inputs |
| Two heaps | **O(log n)** | **O(1)** | O(n) | the optimal answer ⭐ |
| Bucket counts (bounded range) | O(1) | O(1) | O(range) | follow-up when values are bounded |

The two-heap solution is the general optimum; bucketing wins only when the value range is small and known, trading generality for O(1) everything.

---

## 🧪 Edge cases & pitfalls
- **Single element**: after one `addNum`, that heap (lo) holds it; `findMedian` returns it as a `double`.
- **Even vs odd count**: odd → the bigger heap's root; even → average both roots. Decide by comparing heap sizes, not by a separate counter.
- **Integer overflow on the average**: `lo.top() + hi.top()` can reach ~2·10⁵ here (safe in `int`), but in general compute the average in `double` / `long` to avoid overflow. The shown code divides by `2.0`, promoting to floating point.
- **Negative numbers**: handled naturally; in Python remember `lo` stores **negated** values, so read `-lo[0]`.
- **Pitfall — wrong heap polarity**: `lo` must be a **max**-heap (largest small value on top) and `hi` a **min**-heap (smallest large value on top). Swapping them breaks the median read.
- **Pitfall — forgetting to rebalance**: you must both (a) move `lo`'s top into `hi` to keep values ordered, and (b) move back if `hi` outgrows `lo`. Skipping either lets the heaps drift and the roots stop bracketing the median.
- **Pitfall — letting sizes differ by more than 1**: then no single root represents the median. The two-step shuffle guarantees the difference stays ≤ 1.

---

## 🔗 Related problems
- **Sliding Window Median** (LC 480) — median over a moving window; two heaps plus lazy deletion.
- **IPO** (LC 502) — two heaps used for greedy selection.
- **Design Twitter** (LC 355) — another heap-centric streaming design. *(previous file)*
- **Kth Largest Element in a Stream** (LC 703) — single-heap streaming order statistic. *(file 01)*

---

**→ Next topic:** [`../10-Backtracking/00-Index.md`](../10-Backtracking/00-Index.md) | **← Prev:** [`06-Design-Twitter.md`](./06-Design-Twitter.md) | Back to [`00-Index.md`](./00-Index.md)
