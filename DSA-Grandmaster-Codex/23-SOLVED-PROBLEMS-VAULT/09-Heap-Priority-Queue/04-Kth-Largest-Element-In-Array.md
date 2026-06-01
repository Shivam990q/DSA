# Kth Largest Element in an Array

**Platform**: LeetCode 215 · **Difficulty**: Medium · **Topics**: Array, Divide and Conquer, Sorting, Heap (Priority Queue), Quickselect · **Pattern**: Order statistic — heap / quickselect

---

## 📜 Problem Statement

Given an integer array `nums` and an integer `k`, return the `kth` largest element in the array.

Note that it is the `kth` largest element in the sorted order, **not** the `kth` distinct element.

Can you solve it without sorting?

### Examples

**Example 1:**
```
Input:  nums = [3,2,1,5,6,4], k = 2
Output: 5

Explanation: Sorted descending → [6,5,4,3,2,1]. The 2nd largest is 5.
```

**Example 2:**
```
Input:  nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4

Explanation: Sorted descending → [6,5,5,4,3,3,2,2,1]. The 4th largest is 4.
(Duplicates count — the two 5s occupy ranks 2 and 3.)
```

**Example 3:**
```
Input:  nums = [1], k = 1
Output: 1

Explanation: Only one element; it is the 1st largest.
```

### Constraints
```
1 <= k <= nums.length <= 10^5
-10^4 <= nums[i] <= 10^4
```

---

## 🧠 Understanding the problem

We want a single **order statistic**: the value that would sit at position `k` from the top if the array were sorted descending. Equivalently, in an **ascending** sort it's at index `n - k`.

Crucially, duplicates count by position, not by distinct value. In `[5,5,6]` with k=2, the answer is 5 (ranks: 6 is 1st, the first 5 is 2nd) — we are *not* looking for the 2nd distinct value.

Three tiers of solution:
- **Sort** and index — O(n log n), trivially correct, the "can you do better?" prompt is hinting we can.
- **Min-heap of size k** — keep the k largest; the root is the answer. O(n log k), great when k ≪ n.
- **Quickselect** — partition toward index `n - k`; **O(n) average**, the intended "without sorting" answer.

---

## Approach 1 — Sort and index (baseline)

### Intuition
Sort ascending; the k-th largest sits at index `n - k`.

### Algorithm
1. Sort `nums` ascending.
2. Return `nums[n - k]`.

### Dry run on [3,2,1,5,6,4], k=2
```
sort asc → [1,2,3,4,5,6], n=6
index n-k = 4 → nums[4] = 5 → return 5
```

### Code
```cpp
int findKthLargest(vector<int>& nums, int k) {
    sort(nums.begin(), nums.end());
    return nums[nums.size() - k];
}
```
```java
public int findKthLargest(int[] nums, int k) {
    Arrays.sort(nums);
    return nums[nums.length - k];
}
```
```python
def findKthLargest(nums, k):
    nums.sort()
    return nums[len(nums) - k]
```

### Complexity
- **Time**: O(n log n).
- **Space**: O(1) in-place (or O(n) for the library sort).

### Verdict
Always correct and one line. But it fully orders the array for a single value — the prompt's "without sorting" nudges us toward O(n log k) or O(n).

---

## Approach 2 — Min-heap of size k ⭐

### Intuition
Keep a **min-heap holding the k largest elements** seen so far. After scanning everything, the heap's root (its minimum) is the k-th largest overall. Each insertion past size k pops the smallest, which can't be in the top k.

### Algorithm
1. For each `x` in `nums`: push `x`; if heap size > k, pop the minimum.
2. Return the root.

### Dry run on [3,2,1,5,6,4], k=2
```
push 3 → {3}
push 2 → {2,3}             size 2 == k
push 1 → {1,2,3} pop 1     → {2,3}
push 5 → {2,3,5} pop 2     → {3,5}
push 6 → {3,5,6} pop 3     → {5,6}
push 4 → {4,5,6} pop 4     → {5,6}
root (min) = 5 → return 5
```

### Code
```cpp
int findKthLargest(vector<int>& nums, int k) {
    priority_queue<int, vector<int>, greater<int>> minHeap;   // min-heap
    for (int x : nums) {
        minHeap.push(x);
        if ((int)minHeap.size() > k) minHeap.pop();
    }
    return minHeap.top();
}
```
```java
public int findKthLargest(int[] nums, int k) {
    PriorityQueue<Integer> minHeap = new PriorityQueue<>();    // min-heap (default)
    for (int x : nums) {
        minHeap.offer(x);
        if (minHeap.size() > k) minHeap.poll();
    }
    return minHeap.peek();
}
```
```python
import heapq

def findKthLargest(nums, k):
    min_heap = []
    for x in nums:
        heapq.heappush(min_heap, x)
        if len(min_heap) > k:
            heapq.heappop(min_heap)
    return min_heap[0]
```

> **One-liner (Python)**: `heapq.nlargest(k, nums)[-1]` does the same thing — it returns the k largest in descending order, and the last is the k-th largest.

### Complexity
- **Time**: O(n log k).
- **Space**: O(k).

### Verdict
Excellent when **k is small** relative to n, and the natural choice for a *streaming* version of the problem. Bounded memory, simple, hard to get wrong.

---

## Approach 3 — Quickselect (optimal average) ⭐⭐

### Intuition
The k-th largest = the element at index `target = n - k` in ascending order. **Quickselect** partitions around a pivot so that smaller elements go left; the pivot lands at its final sorted index `p`. If `p == target` we're done; otherwise recurse into **only** the side containing `target`. Average O(n) because each partition discards roughly half.

### Algorithm
1. `target = n - k`.
2. Partition `[lo, hi]` (Lomuto): pick `pivot = nums[hi]`, move all smaller elements left, place pivot at index `i`, return `i`.
3. If `i == target` → `nums[i]` is the answer. If `i < target` → search right `[i+1, hi]`. Else → search left `[lo, i-1]`.

### Dry run on [3,2,1,5,6,4], k=2
```
n=6, target = n-k = 4
[lo,hi]=[0,5], pivot = nums[5]=4:
  move elements < 4 left: 3,2,1 → front; 5,6 stay right
  array → [3,2,1,4,6,5], pivot 4 placed at index i=3
i=3 < target=4 → search right [4,5], pivot = nums[5]=5:
  6 < 5? no → pivot 5 placed at index i=4
  array → [3,2,1,4,5,6]
i=4 == target=4 → return nums[4] = 5
```

### Code
```cpp
class Solution {
    int partition(vector<int>& a, int lo, int hi) {
        int pivot = a[hi], i = lo;
        for (int j = lo; j < hi; j++)
            if (a[j] < pivot) swap(a[i++], a[j]);
        swap(a[i], a[hi]);
        return i;
    }
public:
    int findKthLargest(vector<int>& nums, int k) {
        int target = nums.size() - k;
        int lo = 0, hi = nums.size() - 1;
        while (lo <= hi) {
            int p = partition(nums, lo, hi);
            if (p == target) return nums[p];
            else if (p < target) lo = p + 1;
            else hi = p - 1;
        }
        return -1;   // unreachable for valid input
    }
};
```
```java
class Solution {
    public int findKthLargest(int[] nums, int k) {
        int target = nums.length - k;
        int lo = 0, hi = nums.length - 1;
        while (lo <= hi) {
            int p = partition(nums, lo, hi);
            if (p == target) return nums[p];
            else if (p < target) lo = p + 1;
            else hi = p - 1;
        }
        return -1;   // unreachable for valid input
    }
    private int partition(int[] a, int lo, int hi) {
        int pivot = a[hi], i = lo;
        for (int j = lo; j < hi; j++)
            if (a[j] < pivot) { int t = a[i]; a[i] = a[j]; a[j] = t; i++; }
        int t = a[i]; a[i] = a[hi]; a[hi] = t;
        return i;
    }
}
```
```python
import random

def findKthLargest(nums, k):
    target = len(nums) - k

    def partition(lo, hi):
        # randomized pivot guards against the O(n^2) worst case
        r = random.randint(lo, hi)
        nums[r], nums[hi] = nums[hi], nums[r]
        pivot = nums[hi]
        i = lo
        for j in range(lo, hi):
            if nums[j] < pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        nums[i], nums[hi] = nums[hi], nums[i]
        return i

    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        p = partition(lo, hi)
        if p == target:
            return nums[p]
        elif p < target:
            lo = p + 1
        else:
            hi = p - 1
    return -1   # unreachable for valid input
```

### Complexity
- **Time**: O(n) average; O(n²) worst (degenerate pivots). A **randomized pivot** makes the worst case practically impossible.
- **Space**: O(1) — in-place partitioning (iterative loop, no recursion stack).

### Verdict
**The intended "without sorting" answer.** O(n) average and O(1) extra space. The trade-off vs. the heap: quickselect mutates the array and has an O(n²) worst case, while the heap is stable at O(n log k) and supports streaming. In an interview, randomize the pivot to defend the worst case.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Mutates input | When to mention |
|----------|------|-------|---------------|-----------------|
| Sort + index | O(n log n) | O(1) | yes | simplest, the baseline |
| Min-heap size k | O(n log k) | O(k) | no | k ≪ n, streaming ⭐ |
| Quickselect | **O(n) avg** | O(1) | yes | "without sorting", optimum ⭐⭐ |

The recurring trade-off: heap gives bounded memory and predictable O(n log k); quickselect gives O(n) average but a worse worst case and array mutation. Sorting is the safe default if neither is required.

---

## 🧪 Edge cases & pitfalls
- **k == 1** → the maximum; **k == n** → the minimum. Both fall out of the index `n - k`.
- **Duplicates count by position**: `[2,2,2]`, k=2 → 2. The heap and quickselect handle this naturally; do *not* dedup.
- **Single element**: `[1]`, k=1 → 1; loops/heap handle it.
- **Negative numbers**: ordered like any integer; no special handling.
- **Pitfall — heap polarity**: for k-th *largest*, use a **min**-heap of size k (root = answer). Using a max-heap would require popping k−1 times.
- **Pitfall — quickselect index**: the k-th *largest* maps to ascending index `n - k`, not `k - 1`. Mixing these up is the #1 bug.
- **Pitfall — quickselect worst case**: a sorted input with last-element pivots degrades to O(n²). Randomize the pivot (shown in Python) to avoid adversarial inputs.

---

## 🔗 Related problems
- **K Closest Points to Origin** (LC 973) — the same heap/quickselect machinery keyed by distance. *(file 03)*
- **Kth Largest Element in a Stream** (LC 703) — streaming size-k heap. *(file 01)*
- **Top K Frequent Elements** (LC 347) — order statistic on frequencies.
- **Median of Two Sorted Arrays** (LC 4) — a different (binary-search) order-statistic problem.
- **Wiggle Sort II** (LC 324) — uses quickselect to find the median as a building block.

---

**→ Next:** [`05-Task-Scheduler.md`](./05-Task-Scheduler.md) | **← Prev:** [`03-K-Closest-Points.md`](./03-K-Closest-Points.md) | Back to [`00-Index.md`](./00-Index.md)
