# Trapping Rain Water

**Platform**: LeetCode 42 · **Difficulty**: Hard · **Topics**: Array, Two Pointers, Stack, Dynamic Programming · **Pattern**: Left-max / right-max + two pointers

---

## 📜 Problem Statement

Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

### Examples

**Example 1:**
```
Input:  height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The elevation map traps 6 units of rain water (visualize the bars and water filling the gaps).
```

**Example 2:**
```
Input:  height = [4,2,0,3,2,5]
Output: 9
```

### Constraints
```
n == height.length
1 <= n <= 2 * 10^4
0 <= height[i] <= 10^5
```

---

## 🧠 Understanding the problem

Water above bar `i` = `min(maxLeft[i], maxRight[i]) - height[i]` (if positive). The question is how to compute `maxLeft` and `maxRight` efficiently.

---

## Approach 1 — Brute force (per-bar scan)

### Intuition
For each bar `i`, scan left for max and right for max. Water at `i` = `min(leftMax, rightMax) - h[i]`.

### Complexity
- **Time**: O(n²). **Space**: O(1).

### Verdict
Correct but slow.

---

## Approach 2 — Prefix/suffix arrays

### Intuition
Precompute `leftMax[i]` = max(h[0..i]) and `rightMax[i]` = max(h[i..n-1]). Then water at `i` = `min(leftMax[i], rightMax[i]) - h[i]`.

### Code
```cpp
int trap(vector<int>& h) {
    int n = h.size();
    vector<int> lmax(n), rmax(n);
    lmax[0] = h[0];
    for (int i = 1; i < n; i++) lmax[i] = max(lmax[i-1], h[i]);
    rmax[n-1] = h[n-1];
    for (int i = n-2; i >= 0; i--) rmax[i] = max(rmax[i+1], h[i]);
    int water = 0;
    for (int i = 0; i < n; i++) water += min(lmax[i], rmax[i]) - h[i];
    return water;
}
```
```java
public int trap(int[] h) {
    int n = h.length;
    int[] lmax = new int[n], rmax = new int[n];
    lmax[0] = h[0];
    for (int i = 1; i < n; i++) lmax[i] = Math.max(lmax[i-1], h[i]);
    rmax[n-1] = h[n-1];
    for (int i = n-2; i >= 0; i--) rmax[i] = Math.max(rmax[i+1], h[i]);
    int water = 0;
    for (int i = 0; i < n; i++) water += Math.min(lmax[i], rmax[i]) - h[i];
    return water;
}
```
```python
def trap(h):
    n = len(h)
    lmax, rmax = [0]*n, [0]*n
    lmax[0] = h[0]
    for i in range(1, n):
        lmax[i] = max(lmax[i-1], h[i])
    rmax[n-1] = h[n-1]
    for i in range(n-2, -1, -1):
        rmax[i] = max(rmax[i+1], h[i])
    return sum(min(lmax[i], rmax[i]) - h[i] for i in range(n))
```

### Complexity
- **Time**: O(n). **Space**: O(n).

### Verdict
Correct and fast. But can we do O(1) space?

---

## Approach 3 — Monotonic stack

### Intuition
Maintain a decreasing stack of indices. When a taller bar appears, pop shorter bars and compute the water trapped between the popped bar, the new bar, and the new stack top (the left boundary).

### Code
```cpp
int trap(vector<int>& h) {
    stack<int> st;
    int water = 0;
    for (int i = 0; i < h.size(); i++) {
        while (!st.empty() && h[i] > h[st.top()]) {
            int mid = st.top(); st.pop();
            if (st.empty()) break;
            int left = st.top();
            int width = i - left - 1;
            int height = min(h[left], h[i]) - h[mid];
            water += width * height;
        }
        st.push(i);
    }
    return water;
}
```
```java
public int trap(int[] h) {
    Deque<Integer> st = new ArrayDeque<>();
    int water = 0;
    for (int i = 0; i < h.length; i++) {
        while (!st.isEmpty() && h[i] > h[st.peek()]) {
            int mid = st.pop();
            if (st.isEmpty()) break;
            int left = st.peek();
            int width = i - left - 1;
            int height = Math.min(h[left], h[i]) - h[mid];
            water += width * height;
        }
        st.push(i);
    }
    return water;
}
```
```python
def trap(h):
    st, water = [], 0
    for i, hi in enumerate(h):
        while st and hi > h[st[-1]]:
            mid = st.pop()
            if not st:
                break
            left = st[-1]
            width = i - left - 1
            height = min(h[left], hi) - h[mid]
            water += width * height
        st.append(i)
    return water
```

### Complexity
- **Time**: O(n). **Space**: O(n) for the stack.

### Verdict
Elegant, O(n) time. Space is O(n) worst case (monotonically decreasing input). A different perspective from prefix/suffix.

---

## Approach 4 — Two pointers (optimal) ⭐

### Intuition
The water at position `i` depends on `min(leftMax, rightMax)`. The **smaller** of the two sides is the bottleneck. With two pointers:
- Track `leftMax` (running max from left) and `rightMax` (running max from right).
- The side with the **smaller** max is the bottleneck — its water is fully determined. Advance that pointer.

### Why it works
If `leftMax < rightMax`, then for the current `l`, the water is `leftMax - h[l]` regardless of what's further right (because rightMax is already ≥ leftMax, so the right side can't be the bottleneck). Safe to compute and advance `l`.

### Code
```cpp
int trap(vector<int>& h) {
    int l = 0, r = h.size() - 1;
    int lmax = 0, rmax = 0, water = 0;
    while (l < r) {
        if (h[l] < h[r]) {
            lmax = max(lmax, h[l]);
            water += lmax - h[l];
            l++;
        } else {
            rmax = max(rmax, h[r]);
            water += rmax - h[r];
            r--;
        }
    }
    return water;
}
```
```java
public int trap(int[] h) {
    int l = 0, r = h.length - 1;
    int lmax = 0, rmax = 0, water = 0;
    while (l < r) {
        if (h[l] < h[r]) {
            lmax = Math.max(lmax, h[l]);
            water += lmax - h[l];
            l++;
        } else {
            rmax = Math.max(rmax, h[r]);
            water += rmax - h[r];
            r--;
        }
    }
    return water;
}
```
```python
def trap(h):
    l, r = 0, len(h) - 1
    lmax = rmax = water = 0
    while l < r:
        if h[l] < h[r]:
            lmax = max(lmax, h[l])
            water += lmax - h[l]
            l += 1
        else:
            rmax = max(rmax, h[r])
            water += rmax - h[r]
            r -= 1
    return water
```

### Complexity
- **Time**: O(n). **Space**: O(1).

### Verdict
**The optimal answer.** O(n) time, O(1) space. The cleanest solution — combines the prefix/suffix idea into a single pass without arrays.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Key idea |
|----------|------|-------|----------|
| Brute (per-bar scan) | O(n²) | O(1) | scan left+right per bar |
| Prefix/suffix arrays | O(n) | O(n) | precompute leftMax, rightMax |
| Monotonic stack | O(n) | O(n) | horizontal layer-by-layer |
| Two pointers | **O(n)** | **O(1)** | advance the smaller-max side ⭐ |

---

## 🧪 Edge cases & pitfalls
- **Monotonically increasing/decreasing** → 0 water (no "valley").
- **All same height** → 0 water.
- **Single bar / two bars** → 0 water.
- **Pitfall**: confusing with "Container With Most Water" (that's one container between two lines; this fills ALL gaps).
- **Pitfall (two-pointer)**: the condition is `h[l] < h[r]` (comparing heights), NOT `lmax < rmax` — though both work; the height comparison is simpler.

---

## 🔗 Related problems
- **Container With Most Water** (LC 11) — one container, not all gaps.
- **Largest Rectangle in Histogram** (LC 84) — monotonic stack, related thinking.
- **Trapping Rain Water II** (LC 407) — 2D version (BFS + min-heap).
- **Pour Water** (LC 755) — simulation variant.

---

**→ Done with Two Pointers.** Next topic: Sliding Window (folder `03-Sliding-Window/`). | Prev: [`04-Container-With-Most-Water.md`](./04-Container-With-Most-Water.md) | [Index](./00-Index.md)
