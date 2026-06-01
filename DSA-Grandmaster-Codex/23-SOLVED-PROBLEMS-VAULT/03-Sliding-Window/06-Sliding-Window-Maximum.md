# Sliding Window Maximum

**Platform**: LeetCode 239 · **Difficulty**: Hard · **Topics**: Array, Sliding Window, Deque, Monotonic Queue · **Pattern**: Monotonic decreasing deque

---

## 📜 Problem Statement

You are given an array of integers `nums` and a sliding window of size `k` moving from left to right. Return the max value in each window position.

### Examples
```
Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [3,3,5,5,6,7]
Window positions: [1,3,-1] → 3, [3,-1,-3] → 3, [-1,-3,5] → 5, ...
```

### Constraints
```
1 <= nums.length <= 10^5
-10^4 <= nums[i] <= 10^4
1 <= k <= nums.length
```

---

## Approach 1 — Brute force
For each window, scan k elements for max. O(nk). TLE for large n.

---

## Approach 2 — Max-heap
Push (value, index). Pop expired indices. O(n log n).

---

## Approach 3 — Monotonic deque (optimal) ⭐

### Key insight
Maintain a **decreasing deque** of indices. The front is always the current window's max. When a new element enters:
1. Pop from **back** all indices whose values ≤ new value (they can never be the max while the new element is in the window).
2. Push new index to back.
3. Pop from **front** if it's outside the window.
4. Front = current max.

Each index is pushed/popped at most once → O(n) total.

### Code
```cpp
vector<int> maxSlidingWindow(vector<int>& nums, int k) {
    deque<int> dq;
    vector<int> res;
    for (int i = 0; i < nums.size(); i++) {
        while (!dq.empty() && nums[dq.back()] <= nums[i]) dq.pop_back();
        dq.push_back(i);
        if (dq.front() <= i - k) dq.pop_front();
        if (i >= k - 1) res.push_back(nums[dq.front()]);
    }
    return res;
}
```
```java
public int[] maxSlidingWindow(int[] nums, int k) {
    Deque<Integer> dq = new ArrayDeque<>();
    int n = nums.length;
    int[] res = new int[n - k + 1];
    int idx = 0;
    for (int i = 0; i < n; i++) {
        while (!dq.isEmpty() && nums[dq.peekLast()] <= nums[i]) dq.pollLast();
        dq.addLast(i);
        if (dq.peekFirst() <= i - k) dq.pollFirst();
        if (i >= k - 1) res[idx++] = nums[dq.peekFirst()];
    }
    return res;
}
```
```python
from collections import deque
def maxSlidingWindow(nums, k):
    dq, res = deque(), []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res
```

### Complexity: O(n) time, O(k) space.

### Verdict: **Optimal.** The monotonic deque is the canonical tool for "sliding window min/max."

---

## 🧪 Edge cases
- k=1 → array itself. k=n → single max. All same → all same. Strictly decreasing → deque stays full.

---

## 🔗 Related
- LC 1425: Constrained Subsequence Sum (DP + monotonic deque). LC 862: Shortest Subarray with Sum ≥ K (deque on prefix sums).

---

**→ Done with Sliding Window.** Next: Stack (folder `04-Stack/`). | [Index](./00-Index.md)
