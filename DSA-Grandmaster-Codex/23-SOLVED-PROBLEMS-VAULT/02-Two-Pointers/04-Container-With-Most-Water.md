# Container With Most Water

**Platform**: LeetCode 11 · **Difficulty**: Medium · **Topics**: Array, Two Pointers, Greedy · **Pattern**: Converging pointers + greedy shrink

---

## 📜 Problem Statement

You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i`-th line are `(i, 0)` and `(i, height[i])`.

Find two lines that together with the x-axis form a container, such that the container contains the **most water**.

Return the **maximum amount of water** a container can store.

**Note**: You may not slant the container.

### Examples

**Example 1:**
```
Input:  height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: Lines at index 1 (h=8) and index 8 (h=7) form a container of width 7, height min(8,7)=7, area=49.
```

**Example 2:**
```
Input:  height = [1,1]
Output: 1
```

### Constraints
```
n == height.length
2 <= n <= 10^5
0 <= height[i] <= 10^4
```

---

## 🧠 Understanding the problem

Area between lines `i` and `j` = `min(h[i], h[j]) × (j - i)`. We want to maximize this over all pairs. Brute force is O(n²). The key insight: start wide (max width), then the only way to potentially increase area is to increase the height — so move the **shorter** wall inward.

---

## Approach 1 — Brute force (all pairs)

### Code
```cpp
int maxArea(vector<int>& height) {
    int n = height.size(), best = 0;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            best = max(best, min(height[i], height[j]) * (j - i));
    return best;
}
```
```java
public int maxArea(int[] height) {
    int n = height.length, best = 0;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            best = Math.max(best, Math.min(height[i], height[j]) * (j - i));
    return best;
}
```
```python
def maxArea(height):
    n = len(height)
    best = 0
    for i in range(n):
        for j in range(i+1, n):
            best = max(best, min(height[i], height[j]) * (j - i))
    return best
```

### Complexity
- **Time**: O(n²). **Space**: O(1).

### Verdict
Correct but TLE for n=10⁵.

---

## Approach 2 — Two pointers (optimal) ⭐

### Intuition
Start with the widest container (`l=0, r=n-1`). The area is limited by the **shorter** wall. Moving the taller wall inward can only decrease width without guaranteeing a taller min-height. Moving the **shorter** wall inward might find a taller wall → potentially larger area.

### Why it's correct (proof sketch)
When `h[l] < h[r]`, any container using `l` as the left wall has height ≤ `h[l]` and width ≤ `r-l`. So the current `(l, r)` is already the BEST container using `l`. We can safely discard `l` and move inward. (Symmetric for `h[r] < h[l]`.)

### Code
```cpp
int maxArea(vector<int>& height) {
    int l = 0, r = height.size() - 1, best = 0;
    while (l < r) {
        best = max(best, min(height[l], height[r]) * (r - l));
        if (height[l] < height[r]) l++;
        else r--;
    }
    return best;
}
```
```java
public int maxArea(int[] height) {
    int l = 0, r = height.length - 1, best = 0;
    while (l < r) {
        best = Math.max(best, Math.min(height[l], height[r]) * (r - l));
        if (height[l] < height[r]) l++;
        else r--;
    }
    return best;
}
```
```python
def maxArea(height):
    l, r, best = 0, len(height) - 1, 0
    while l < r:
        best = max(best, min(height[l], height[r]) * (r - l))
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return best
```

### Complexity
- **Time**: O(n). **Space**: O(1).

### Verdict
**The optimal answer.** The "move the shorter wall" greedy is provably correct and gives O(n).

---

## ⚖️ Approach comparison

| Approach | Time | Space |
|----------|------|-------|
| Brute force | O(n²) | O(1) |
| Two pointers | **O(n)** | **O(1)** ⭐ |

---

## 🧪 Edge cases & pitfalls
- **Equal heights** (`h[l] == h[r]`): move either (both are safe — the current container is the best using both these walls together).
- **All same height** → first pair (widest) is the answer.
- **Decreasing/increasing** → two pointers still works.
- **Pitfall**: confusing this with Trapping Rain Water (different problem — that one fills ALL gaps, not just one container).

---

## 🔗 Related problems
- **Trapping Rain Water** (LC 42) — fill all gaps between walls (harder, next problem).
- **Largest Rectangle in Histogram** (LC 84) — monotonic stack.

---

**→ Next:** [`05-Trapping-Rain-Water.md`](./05-Trapping-Rain-Water.md) | Prev: [`03-3Sum.md`](./03-3Sum.md) | [Index](./00-Index.md)
