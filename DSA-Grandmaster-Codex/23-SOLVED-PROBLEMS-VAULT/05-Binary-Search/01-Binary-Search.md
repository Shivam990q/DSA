# Binary Search

**Platform**: LeetCode 704 · **Difficulty**: Easy · **Topics**: Array, Binary Search · **Pattern**: Classic two-bound search

---

## 📜 Problem Statement

Given an array of integers `nums` which is sorted in **ascending order**, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its index. Otherwise, return `-1`.

You must write an algorithm with **O(log n)** runtime complexity.

### Examples

**Example 1:**
```
Input:  nums = [-1, 0, 3, 5, 9, 12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4.
```

**Example 2:**
```
Input:  nums = [-1, 0, 3, 5, 9, 12], target = 2
Output: -1
Explanation: 2 does not exist in nums so return -1.
```

**Example 3:**
```
Input:  nums = [5], target = 5
Output: 0
Explanation: Single-element array, target is the only element.
```

### Constraints
```
1 <= nums.length <= 10^4
-10^4 < nums[i], target < 10^4
All the integers in nums are unique.
nums is sorted in ascending order.
```

---

## 🧠 Understanding the problem

This is *the* canonical binary search. Two facts dominate everything:

1. **The array is sorted ascending.** That ordering is the only thing that lets us discard half the array in one comparison. Without sortedness we'd be stuck with a linear scan.
2. **The required complexity is O(log n).** The problem doesn't just want a correct answer — it explicitly forbids the O(n) linear scan. This is a strong hint that binary search is the intended solution.

The core idea: look at the middle element. Because the array is sorted, comparing `nums[mid]` to `target` tells us which side the target *must* be on (if it's present at all), so we throw away the other half. Each step halves the candidates, giving `log₂(n)` steps.

The whole game is keeping a **search window** `[lo, hi]` that always contains the target *if it exists*, and shrinking that window until we either land on the target or the window becomes empty.

---

## Approach 1 — Linear scan (baseline)

### Intuition
Ignore the sortedness and just walk the array. If we see the target, return its index. This is the "prove I understand the problem" baseline — and it shows us exactly what binary search improves on.

### Algorithm
1. For each index `i` from `0` to `n-1`:
   - If `nums[i] == target` → return `i`.
2. If the loop finishes → return `-1`.

### Code

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        for (int i = 0; i < (int)nums.size(); i++)
            if (nums[i] == target) return i;
        return -1;
    }
};
```
```java
class Solution {
    public int search(int[] nums, int target) {
        for (int i = 0; i < nums.length; i++)
            if (nums[i] == target) return i;
        return -1;
    }
}
```
```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        for i, x in enumerate(nums):
            if x == target:
                return i
        return -1
```

### Complexity
- **Time**: O(n) — touches every element in the worst case.
- **Space**: O(1).

### Verdict
Correct, but it **violates the required O(log n)**. It ignores the most valuable property of the input (sortedness). It's only here as the contrast that motivates the real solution.

---

## Approach 2 — Classic binary search (optimal) ⭐

### Intuition
Keep a window `[lo, hi]` that is guaranteed to contain the target if it exists. Look at the middle element `nums[mid]`:

- If `nums[mid] == target` → found it.
- If `nums[mid] < target` → the target (being larger) can only be in the **right half**, so move `lo = mid + 1`.
- If `nums[mid] > target` → the target can only be in the **left half**, so move `hi = mid - 1`.

Each comparison eliminates half the remaining window. When `lo > hi`, the window is empty and the target isn't present.

### Algorithm
1. Set `lo = 0`, `hi = n - 1`.
2. While `lo <= hi`:
   - `mid = lo + (hi - lo) / 2` (this form avoids integer overflow vs `(lo + hi) / 2`).
   - If `nums[mid] == target` → return `mid`.
   - Else if `nums[mid] < target` → `lo = mid + 1`.
   - Else → `hi = mid - 1`.
3. Return `-1`.

### Dry run on `nums = [-1, 0, 3, 5, 9, 12]`, `target = 9`
```
lo=0, hi=5
  mid = 0 + (5-0)/2 = 2 → nums[2]=3 < 9 → search right → lo=3
lo=3, hi=5
  mid = 3 + (5-3)/2 = 4 → nums[4]=9 == 9 → return 4 ✅
```

Now a "not found" trace, `target = 2`:
```
lo=0, hi=5
  mid=2 → nums[2]=3 > 2 → hi=1
lo=0, hi=1
  mid=0 → nums[0]=-1 < 2 → lo=1
lo=1, hi=1
  mid=1 → nums[1]=0 < 2 → lo=2
lo=2, hi=1 → lo > hi → loop ends → return -1 ✅
```

### Code

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int lo = 0, hi = (int)nums.size() - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;     // avoids overflow
            if (nums[mid] == target) return mid;
            else if (nums[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return -1;
    }
};
```
```java
class Solution {
    public int search(int[] nums, int target) {
        int lo = 0, hi = nums.length - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;     // avoids overflow
            if (nums[mid] == target) return mid;
            else if (nums[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return -1;
    }
}
```
```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = lo + (hi - lo) // 2          # avoids overflow in other languages
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1
```

### Complexity
- **Time**: O(log n) — the window halves every iteration.
- **Space**: O(1) — only a few index variables.

### Verdict
**The optimal answer.** Meets the required O(log n), uses O(1) space, and is the foundation every other problem in this set builds on. Memorize this template until it's muscle memory.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Uses sortedness | When to mention |
|----------|------|-------|-----------------|-----------------|
| Linear scan | O(n) | O(1) | no | only as the baseline / when array is unsorted |
| Binary search | **O(log n)** | O(1) | yes | the required, optimal answer ⭐ |

The single sentence that captures the trade-off: *"Sortedness lets a single mid-comparison discard half the array, turning a linear scan into a logarithmic search."*

---

## 🧪 Edge cases & pitfalls
- **Single element** (`n = 1`) → `lo == hi == 0`; one comparison decides it. Handled by `lo <= hi`.
- **Target smaller than all / larger than all** → the window slides fully to one side and collapses; returns `-1`.
- **Overflow pitfall**: in C++ and Java, `(lo + hi) / 2` can overflow `int` when `lo + hi` exceeds `INT_MAX`. Use `lo + (hi - lo) / 2`. (Not an issue in Python, which has arbitrary-precision ints, but use the same form for consistency.)
- **The `<=` vs `<` pitfall**: this template uses `while (lo <= hi)` because we return *immediately on a match* and want to inspect the final single-element window. Using `<` here would skip checking that last element.
- **Off-by-one pitfall**: always move past `mid` (`mid + 1` / `mid - 1`). Setting `lo = mid` or `hi = mid` here can cause an infinite loop because the window may stop shrinking.

---

## 🔗 Related problems
- **Search Insert Position** (LC 35) — return where the target *would* go; the lower-bound variant.
- **First Bad Version** (LC 278) — binary search on a monotonic predicate.
- **Search a 2D Matrix** (LC 74) — flatten a matrix into one sorted array and run this exact search.
- **Binary Search** variants with duplicates → `lower_bound` / `upper_bound` boundary searches.

---

**→ Next:** [`02-Search-2D-Matrix.md`](./02-Search-2D-Matrix.md) | [Problem set index](./00-Index.md)
