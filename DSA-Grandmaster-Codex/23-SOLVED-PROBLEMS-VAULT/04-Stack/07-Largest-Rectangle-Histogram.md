# Largest Rectangle in Histogram

**Platform**: LeetCode 84 · **Difficulty**: Hard · **Topics**: Array, Stack, Monotonic Stack · **Pattern**: Monotonic increasing stack with sentinel

---

## 📜 Problem Statement

Given an array of integers `heights` representing the histogram's bar height where the width of each bar is `1`, return the area of the largest rectangle in the histogram.

### Examples

**Example 1:**
```
Input:  heights = [2,1,5,6,2,3]
Output: 10
Explanation: The largest rectangle has area = 5 × 2 = 10 (bars at index 2 and 3 with height 5).
```

**Example 2:**
```
Input:  heights = [2,4]
Output: 4
Explanation: The largest rectangle is the bar at index 1 with height 4, area = 4 × 1 = 4.
```

**Example 3:**
```
Input:  heights = [1]
Output: 1
```

### Constraints
```
1 <= heights.length <= 10^5
0 <= heights[i] <= 10^4
```

---

## 🧠 Understanding the problem

We want the largest rectangular area that fits entirely within the histogram. For any rectangle, its height is limited by the shortest bar it spans. So for each bar `i`, we want to know: how far left and right can we extend while all bars are ≥ `heights[i]`?

If we know the **left boundary** (first bar shorter than `heights[i]` to the left) and **right boundary** (first bar shorter to the right), the width is `right - left - 1`, and area = `heights[i] × width`.

Finding these boundaries for all bars efficiently is the monotonic stack's job.

---

## Approach 1 — Brute force (check every pair of boundaries)

### Intuition
For each bar `i`, expand left and right while bars are ≥ `heights[i]`. Compute the area.

### Algorithm
1. For each `i`:
   - Expand `left` from `i-1` leftward while `heights[left] >= heights[i]`.
   - Expand `right` from `i+1` rightward while `heights[right] >= heights[i]`.
   - Area = `heights[i] × (right - left + 1)`.
   - Track maximum.

### Code
```cpp
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        int n = heights.size();
        int maxArea = 0;
        for (int i = 0; i < n; i++) {
            int left = i, right = i;
            while (left > 0 && heights[left - 1] >= heights[i]) left--;
            while (right < n - 1 && heights[right + 1] >= heights[i]) right++;
            maxArea = max(maxArea, heights[i] * (right - left + 1));
        }
        return maxArea;
    }
};
```
```java
class Solution {
    public int largestRectangleArea(int[] heights) {
        int n = heights.length;
        int maxArea = 0;
        for (int i = 0; i < n; i++) {
            int left = i, right = i;
            while (left > 0 && heights[left - 1] >= heights[i]) left--;
            while (right < n - 1 && heights[right + 1] >= heights[i]) right++;
            maxArea = Math.max(maxArea, heights[i] * (right - left + 1));
        }
        return maxArea;
    }
}
```
```python
class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        n = len(heights)
        max_area = 0
        for i in range(n):
            left = i
            right = i
            while left > 0 and heights[left - 1] >= heights[i]:
                left -= 1
            while right < n - 1 and heights[right + 1] >= heights[i]:
                right += 1
            max_area = max(max_area, heights[i] * (right - left + 1))
        return max_area
```

### Complexity
- **Time**: O(n²) — worst case when all bars are the same height.
- **Space**: O(1).

### Verdict
Correct but TLEs on n = 10^5. Establishes the "expand from each bar" idea that the stack approach optimizes.

---

## Approach 2 — Two-pass with left/right boundary arrays

### Intuition
Precompute for each bar: the index of the nearest shorter bar to the left (`leftSmaller[i]`) and to the right (`rightSmaller[i]`). Then area for bar `i` = `heights[i] × (rightSmaller[i] - leftSmaller[i] - 1)`.

We can compute these boundary arrays using a monotonic stack in O(n) each.

### Algorithm
1. Compute `leftSmaller[i]`: traverse left to right with a stack. For each `i`, pop while stack top's height ≥ `heights[i]`. The new top (or -1 if empty) is the left boundary.
2. Compute `rightSmaller[i]`: traverse right to left similarly. Boundary is `n` if stack empty.
3. For each `i`: area = `heights[i] × (rightSmaller[i] - leftSmaller[i] - 1)`.
4. Return max area.

### Code
```cpp
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        int n = heights.size();
        vector<int> leftSmaller(n), rightSmaller(n);
        stack<int> st;
        
        // Left boundaries
        for (int i = 0; i < n; i++) {
            while (!st.empty() && heights[st.top()] >= heights[i])
                st.pop();
            leftSmaller[i] = st.empty() ? -1 : st.top();
            st.push(i);
        }
        
        // Clear stack for right pass
        while (!st.empty()) st.pop();
        
        // Right boundaries
        for (int i = n - 1; i >= 0; i--) {
            while (!st.empty() && heights[st.top()] >= heights[i])
                st.pop();
            rightSmaller[i] = st.empty() ? n : st.top();
            st.push(i);
        }
        
        // Compute max area
        int maxArea = 0;
        for (int i = 0; i < n; i++) {
            int width = rightSmaller[i] - leftSmaller[i] - 1;
            maxArea = max(maxArea, heights[i] * width);
        }
        return maxArea;
    }
};
```
```java
class Solution {
    public int largestRectangleArea(int[] heights) {
        int n = heights.length;
        int[] leftSmaller = new int[n], rightSmaller = new int[n];
        Deque<Integer> st = new ArrayDeque<>();

        // Left boundaries
        for (int i = 0; i < n; i++) {
            while (!st.isEmpty() && heights[st.peek()] >= heights[i])
                st.pop();
            leftSmaller[i] = st.isEmpty() ? -1 : st.peek();
            st.push(i);
        }

        // Clear stack for right pass
        st.clear();

        // Right boundaries
        for (int i = n - 1; i >= 0; i--) {
            while (!st.isEmpty() && heights[st.peek()] >= heights[i])
                st.pop();
            rightSmaller[i] = st.isEmpty() ? n : st.peek();
            st.push(i);
        }

        // Compute max area
        int maxArea = 0;
        for (int i = 0; i < n; i++) {
            int width = rightSmaller[i] - leftSmaller[i] - 1;
            maxArea = Math.max(maxArea, heights[i] * width);
        }
        return maxArea;
    }
}
```
```python
class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        n = len(heights)
        left_smaller = [0] * n
        right_smaller = [0] * n
        stack = []
        
        # Left boundaries
        for i in range(n):
            while stack and heights[stack[-1]] >= heights[i]:
                stack.pop()
            left_smaller[i] = stack[-1] if stack else -1
            stack.append(i)
        
        stack.clear()
        
        # Right boundaries
        for i in range(n - 1, -1, -1):
            while stack and heights[stack[-1]] >= heights[i]:
                stack.pop()
            right_smaller[i] = stack[-1] if stack else n
            stack.append(i)
        
        # Compute max area
        max_area = 0
        for i in range(n):
            width = right_smaller[i] - left_smaller[i] - 1
            max_area = max(max_area, heights[i] * width)
        
        return max_area
```

### Complexity
- **Time**: O(n) — two passes, each element pushed/popped once per pass.
- **Space**: O(n) — boundary arrays and stack.

### Verdict
Optimal time. Clear and easy to understand. Two passes make the logic transparent.

---

## Approach 3 — Single-pass monotonic increasing stack with sentinel (optimal) ⭐

### Intuition
Maintain a **monotonically increasing** stack of indices. When we encounter a bar shorter than the stack's top, the top bar's "right boundary" is the current index, and its "left boundary" is the new stack top (after popping). We can compute the area immediately.

Adding a sentinel value of `0` at the end forces all remaining bars to be popped and processed.

### Algorithm
1. Append `0` to `heights` (sentinel to flush the stack at the end).
2. Initialize empty stack, `maxArea = 0`.
3. For each index `i`:
   - While stack is non-empty AND `heights[i] < heights[stack.top()]`:
     - Pop `h_idx`. Height = `heights[h_idx]`.
     - Width = `i - stack.top() - 1` (if stack non-empty) or `i` (if stack empty).
     - Update `maxArea`.
   - Push `i`.
4. Return `maxArea`.

### Dry run on `[2, 1, 5, 6, 2, 3]` + sentinel `0`
```
heights = [2, 1, 5, 6, 2, 3, 0]

i=0 (h=2): stack empty → push 0. Stack: [0]
i=1 (h=1): 1 < 2 → pop 0. Height=2, width=1 (stack empty, so width=i=1). Area=2.
            Push 1. Stack: [1]
i=2 (h=5): 5 > 1 → push 2. Stack: [1,2]
i=3 (h=6): 6 > 5 → push 3. Stack: [1,2,3]
i=4 (h=2): 2 < 6 → pop 3. Height=6, width=4-2-1=1. Area=6.
            2 < 5 → pop 2. Height=5, width=4-1-1=2. Area=10. ← MAX
            2 > 1 → push 4. Stack: [1,4]
i=5 (h=3): 3 > 2 → push 5. Stack: [1,4,5]
i=6 (h=0): 0 < 3 → pop 5. Height=3, width=6-4-1=1. Area=3.
            0 < 2 → pop 4. Height=2, width=6-1-1=4. Area=8.
            0 < 1 → pop 1. Height=1, width=6 (stack empty). Area=6.
            Push 6. Stack: [6]

maxArea = 10 ✓
```

### Code
```cpp
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        heights.push_back(0); // sentinel
        int n = heights.size();
        stack<int> st;
        int maxArea = 0;
        
        for (int i = 0; i < n; i++) {
            while (!st.empty() && heights[i] < heights[st.top()]) {
                int h = heights[st.top()]; st.pop();
                int width = st.empty() ? i : i - st.top() - 1;
                maxArea = max(maxArea, h * width);
            }
            st.push(i);
        }
        
        heights.pop_back(); // restore original array
        return maxArea;
    }
};
```
```java
class Solution {
    public int largestRectangleArea(int[] heights) {
        int n = heights.length;
        int[] h = new int[n + 1]; // append sentinel 0
        System.arraycopy(heights, 0, h, 0, n);
        h[n] = 0;
        Deque<Integer> st = new ArrayDeque<>();
        int maxArea = 0;

        for (int i = 0; i <= n; i++) {
            while (!st.isEmpty() && h[i] < h[st.peek()]) {
                int height = h[st.pop()];
                int width = st.isEmpty() ? i : i - st.peek() - 1;
                maxArea = Math.max(maxArea, height * width);
            }
            st.push(i);
        }

        return maxArea;
    }
}
```
```python
class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        heights.append(0)  # sentinel to flush stack
        stack = []
        max_area = 0
        
        for i in range(len(heights)):
            while stack and heights[i] < heights[stack[-1]]:
                h = heights[stack.pop()]
                width = i if not stack else i - stack[-1] - 1
                max_area = max(max_area, h * width)
            stack.append(i)
        
        heights.pop()  # restore original
        return max_area
```

### Complexity
- **Time**: O(n) — each index pushed and popped exactly once.
- **Space**: O(n) — stack size.

### Verdict
**The optimal single-pass answer.** The sentinel trick eliminates the need for a separate cleanup loop. This is the classic interview solution for this problem.

---

## Approach 4 — Divide and conquer

### Intuition
The largest rectangle either:
1. Uses the minimum-height bar (spans the entire range), or
2. Is entirely in the left half, or
3. Is entirely in the right half.

Recursively solve left and right halves.

### Code
```cpp
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        return helper(heights, 0, heights.size() - 1);
    }
    
    int helper(vector<int>& h, int left, int right) {
        if (left > right) return 0;
        if (left == right) return h[left];
        
        int minIdx = left;
        for (int i = left + 1; i <= right; i++)
            if (h[i] < h[minIdx]) minIdx = i;
        
        int throughMin = h[minIdx] * (right - left + 1);
        int leftArea = helper(h, left, minIdx - 1);
        int rightArea = helper(h, minIdx + 1, right);
        
        return max({throughMin, leftArea, rightArea});
    }
};
```
```java
class Solution {
    public int largestRectangleArea(int[] heights) {
        return helper(heights, 0, heights.length - 1);
    }

    private int helper(int[] h, int left, int right) {
        if (left > right) return 0;
        if (left == right) return h[left];

        int minIdx = left;
        for (int i = left + 1; i <= right; i++)
            if (h[i] < h[minIdx]) minIdx = i;

        int throughMin = h[minIdx] * (right - left + 1);
        int leftArea = helper(h, left, minIdx - 1);
        int rightArea = helper(h, minIdx + 1, right);

        return Math.max(throughMin, Math.max(leftArea, rightArea));
    }
}
```
```python
class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        def helper(left, right):
            if left > right:
                return 0
            if left == right:
                return heights[left]
            
            min_idx = left
            for i in range(left + 1, right + 1):
                if heights[i] < heights[min_idx]:
                    min_idx = i
            
            through_min = heights[min_idx] * (right - left + 1)
            left_area = helper(left, min_idx - 1)
            right_area = helper(min_idx + 1, right)
            
            return max(through_min, left_area, right_area)
        
        return helper(0, len(heights) - 1)
```

### Complexity
- **Time**: O(n log n) average, O(n²) worst case (sorted input).
- **Space**: O(n) recursion stack.

### Verdict
Interesting approach but worse than the stack solution. Can be improved to O(n log n) guaranteed with a segment tree for range-minimum queries, but that's overkill here.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute force (expand) | O(n²) | O(1) | TLE |
| Two-pass boundaries | O(n) | O(n) | Clear, two passes |
| Single-pass + sentinel | **O(n)** | O(n) | Cleanest optimal ⭐ |
| Divide and conquer | O(n log n) avg | O(n) | Elegant but slower |

---

## 🧪 Edge cases & pitfalls
- **Single bar** (`[5]`) → area = 5.
- **All same height** (`[3,3,3,3]`) → area = 3 × 4 = 12. The stack pops everything at the sentinel.
- **Strictly increasing** (`[1,2,3,4]`) → all popped at sentinel. Max area = max of each bar × its possible width.
- **Strictly decreasing** (`[4,3,2,1]`) → each bar popped immediately by the next. Max = 4×1 or 3×2 or 2×3 or 1×4 = 6.
- **Contains zeros** (`[0,5,0]`) → zero-height bars act as separators.
- **Pitfall**: forgetting the sentinel → bars remaining on the stack at the end are never processed.
- **Pitfall**: width calculation when stack is empty after popping → width is `i` (extends all the way to the left edge), not `i - (-1) - 1`.
- **Pitfall**: modifying the input array (appending sentinel) — restore it afterward or work on a copy.

---

## 🔗 Related problems
- **Maximal Rectangle** (LC 85) — 2D version: build histogram per row, apply this algorithm.
- **Trapping Rain Water** (LC 42) — related monotonic stack problem.
- **Daily Temperatures** (LC 739) — monotonic decreasing stack.
- **Maximum Width Ramp** (LC 962) — monotonic stack variant.
- **Sum of Subarray Minimums** (LC 907) — uses similar left/right boundary technique.

---

**→ Prev:** [`06-Car-Fleet.md`](./06-Car-Fleet.md) | [Problem set index](./00-Index.md)
