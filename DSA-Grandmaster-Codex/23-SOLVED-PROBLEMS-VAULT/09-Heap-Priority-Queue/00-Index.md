# 🗂️ Heap / Priority Queue — Problem Set

> Each problem below is a **complete editorial**: full statement (platform-style) → every approach from brute force to optimal → intuition, algorithm, dry run, C++ / Java / Python code, complexity, edge cases, pitfalls, and related problems.

> **How to use**: open a problem, read ONLY the statement, attempt it cold (30–45 min). Then read the approaches in order — feel WHY each one improves on the last. Re-derive the optimal from the key insight after 7 days.

> A heap gives you the minimum (or maximum) element in O(1) and lets you remove it or insert a new element in O(log n). That single capability — *always know the current extreme* — solves an astonishing range of problems: "top K", "K closest", "merge K", "running median", and greedy scheduling.

---

## 📋 Problems

| # | Problem | LC # | Difficulty | Core Approaches |
|---|---------|------|------------|-----------------|
| 01 | [Kth Largest Element in a Stream](./01-Kth-Largest-In-Stream.md) | 703 | Easy | sort-each-add → min-heap of size k |
| 02 | [Last Stone Weight](./02-Last-Stone-Weight.md) | 1046 | Easy | sort-each-round → max-heap |
| 03 | [K Closest Points to Origin](./03-K-Closest-Points.md) | 973 | Medium | sort all → max-heap size k → quickselect |
| 04 | [Kth Largest Element in an Array](./04-Kth-Largest-Element-In-Array.md) | 215 | Medium | sort → min-heap size k → quickselect |
| 05 | [Task Scheduler](./05-Task-Scheduler.md) | 621 | Medium | max-heap simulation → greedy formula |
| 06 | [Design Twitter](./06-Design-Twitter.md) | 355 | Medium | merge with max-heap |
| 07 | [Find Median from Data Stream](./07-Find-Median-From-Data-Stream.md) | 295 | Hard | sorted insert → two heaps |

---

## 🧱 The heap primitives in each language

Internalize these so the solution code reads naturally. A **min-heap** keeps the smallest on top; a **max-heap** keeps the largest on top.

**C++** — `priority_queue` is a **max-heap** by default. For a min-heap pass `greater<T>`.
```cpp
priority_queue<int> maxHeap;                                   // max-heap
priority_queue<int, vector<int>, greater<int>> minHeap;        // min-heap
maxHeap.push(x); int t = maxHeap.top(); maxHeap.pop();         // O(log n) push/pop, O(1) top
```

**Java** — `PriorityQueue` is a **min-heap** by default. For a max-heap pass `Collections.reverseOrder()` or a comparator.
```java
PriorityQueue<Integer> minHeap = new PriorityQueue<>();                       // min-heap
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder()); // max-heap
minHeap.offer(x); int t = minHeap.peek(); minHeap.poll();                     // O(log n) offer/poll, O(1) peek
```

**Python** — `heapq` provides a **min-heap** only. For a max-heap, **negate** the values (or use tuples with negated keys).
```python
import heapq
h = []
heapq.heappush(h, x)        # push, O(log n)
top = h[0]                  # peek smallest, O(1)
val = heapq.heappop(h)      # pop smallest, O(log n)
heapq.heapify(arr)          # build heap in O(n)
# max-heap trick: push -x, read -h[0]
```

---

## 🎯 The pattern family

The unifying move: *"I repeatedly need the current minimum or maximum of a changing set."* A heap maintains that extreme under insertions and deletions in O(log n), which beats re-sorting (O(n log n)) every time the set changes.

**1. Top-K / Kth element → a heap of size K.**
Keep a heap bounded to size K. For the **K-th largest**, use a **min-heap of size K**: its root is exactly the K-th largest, and anything smaller gets discarded. For **K closest / K smallest**, use a **max-heap of size K**: pop whenever it overflows so only the K best survive. Cost is O(n log K), better than sorting when K ≪ n.
- Kth Largest in a Stream, Kth Largest in an Array, K Closest Points.

**2. Greedy "process the current extreme" → repeated pop.**
When each step must act on the largest (or smallest) remaining element and may push a new one back, a heap is the natural engine.
- Last Stone Weight (smash the two heaviest), Task Scheduler (schedule the most frequent task first).

**3. Merge / select most-recent across many sources → max-heap.**
Pull the next element from whichever source currently has the best key.
- Design Twitter (merge recent tweets across followees by timestamp).

**4. Running median / balance → two heaps.**
A max-heap for the lower half and a min-heap for the upper half, kept balanced, expose the median(s) at their tops in O(1).
- Find Median from Data Stream.

> **When NOT to use a heap**: if you need the K-th element of a *static* array just once, **quickselect** gives O(n) average — better than the heap's O(n log K). If you need *all* elements in order, just sort. The heap shines when the set **changes over time** or you only need the **extremes**, not a full ordering.

---

**→ Start:** [`01-Kth-Largest-In-Stream.md`](./01-Kth-Largest-In-Stream.md) | Back to [vault index](../00-Index.md)
