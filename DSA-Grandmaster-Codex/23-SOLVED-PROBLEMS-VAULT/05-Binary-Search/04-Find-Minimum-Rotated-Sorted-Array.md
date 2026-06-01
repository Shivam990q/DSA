# Find Minimum in Rotated Sorted Array

**Platform**: LeetCode 153 · **Difficulty**: Medium · **Topics**: Array, Binary Search · **Pattern**: Pivot search on a rotated array

---

## 📜 Problem Statement

Suppose an array of length `n` sorted in ascending order is **rotated** between `1` and `n` times. For example, the array `nums = [0,1,2,4,5,6,7]` might become:

- `[4,5,6,7,0,1,2]` if it was rotated `4` times.
- `[0,1,2,4,5,6,7]` if it was rotated `7` times.

Notice that **rotating** an array `[a[0], a[1], a[2], ..., a[n-1]]` 1 time results in the array `[a[n-1], a[0], a[1], a[2], ..., a[n-2]]`.

Given the sorted rotated array `nums` of **unique** elements, return the **minimum element** of this array.

You must write an algorithm that runs in **O(log n)** time.

### Examples

**Example 1:**
```
Input:  nums = [3,4,5,1,2]
Output: 1
Explanation: The original array was [1,2,3,4,5] rotated 3 times.
```

**Example 2:**
```
Input:  nums = [4,5,6,7,0,1,2]
Output: 0
Explanation: The original array was [0,1,2,4,5,6,7] rotated 4 times.
```

**Example 3:**
```
Input:  nums = [11,13,15,17]
Output: 11
Explanation: The original array was rotated n times, so it looks un-rotated.
```

### Constraints
```
n == nums.length
1 <= n <= 5000
-5000 <= nums[i] <= 5000
All the integers of nums are unique.
nums is sorted and rotated between 1 and n times.
```

---

## 🧠 Understanding the problem

Picture a sorted array bent at one spot. A rotated sorted array always looks like **two ascending runs**, where the second run's values are all smaller than the first run's:

```
[4, 5, 6, 7, 0, 1, 2]
 \_______/  \_______/
  run 1       run 2
 (high vals) (low vals)
```

The **minimum** is the very first element of the second run — the single point where the array "drops". It's also the only place where an element is **smaller than its predecessor** (the pivot). If the array isn't rotated at all (or rotated `n` times so it looks sorted), the minimum is simply `nums[0]`.

The required O(log n) tells us we can't scan; we must binary search. The trick is: we don't have a `target` to compare against. Instead we compare `nums[mid]` to a **boundary element** to decide which half contains the drop.

The cleanest comparison is `nums[mid]` vs `nums[hi]` (the rightmost element of the current window):

- If `nums[mid] > nums[hi]`: `mid` is still in the **high run** (the left run). The drop, and therefore the minimum, must be **to the right** of `mid`. So `lo = mid + 1`.
- If `nums[mid] <= nums[hi]`: `mid` is in the **low run** (or exactly the minimum). The minimum is at `mid` or **to its left**. So `hi = mid`.

Why compare to `nums[hi]` and not `nums[lo]`? Because the right end is always part of the low run (or the whole thing is sorted), making the comparison unambiguous. Comparing to `nums[lo]` needs an extra "is this whole window already sorted?" check.

---

## Approach 1 — Linear scan (baseline)

### Intuition
The minimum is just the smallest element; scan and track it. Or, equivalently, find the one place where `nums[i] < nums[i-1]`.

### Algorithm
1. Track `mn = nums[0]`.
2. For each element, update `mn = min(mn, x)`.
3. Return `mn`.

### Code

```cpp
class Solution {
public:
    int findMin(vector<int>& nums) {
        int mn = nums[0];
        for (int x : nums) mn = min(mn, x);
        return mn;
    }
};
```
```java
class Solution {
    public int findMin(int[] nums) {
        int mn = nums[0];
        for (int x : nums) mn = Math.min(mn, x);
        return mn;
    }
}
```
```python
class Solution:
    def findMin(self, nums: List[int]) -> int:
        mn = nums[0]
        for x in nums:
            mn = min(mn, x)
        return mn
```

### Complexity
- **Time**: O(n) — visits every element.
- **Space**: O(1).

### Verdict
Correct but **violates the required O(log n)** and ignores the rotated-sorted structure entirely. Baseline only.

---

## Approach 2 — Pivot binary search (optimal) ⭐

### Intuition
Maintain a window `[lo, hi]` guaranteed to contain the minimum. Compare `nums[mid]` to `nums[hi]` to decide which half keeps the drop, and shrink toward it. We use the **converging template** `while (lo < hi)` and return `nums[lo]` when the window collapses to a single element — the minimum.

### Algorithm
1. `lo = 0`, `hi = n - 1`.
2. While `lo < hi`:
   - `mid = lo + (hi - lo) / 2`.
   - If `nums[mid] > nums[hi]` → minimum is strictly right → `lo = mid + 1`.
   - Else → minimum is at `mid` or left → `hi = mid`.
3. Return `nums[lo]`.

### Dry run on `nums = [4,5,6,7,0,1,2]`
```
lo=0, hi=6   (nums[hi]=2)
  mid = 0 + (6-0)/2 = 3 → nums[3]=7 > 2 → drop is right → lo=4
lo=4, hi=6   (nums[hi]=2)
  mid = 4 + (6-4)/2 = 5 → nums[5]=1 <= 2 → min at mid or left → hi=5
lo=4, hi=5   (nums[hi]=1)
  mid = 4 + (5-4)/2 = 4 → nums[4]=0 <= 1 → min at mid or left → hi=4
lo=4, hi=4 → loop ends → return nums[4] = 0 ✅
```

Now an already-sorted case `nums = [11,13,15,17]`:
```
lo=0, hi=3   (nums[hi]=17)
  mid=1 → nums[1]=13 <= 17 → hi=1
lo=0, hi=1   (nums[hi]=13)
  mid=0 → nums[0]=11 <= 13 → hi=0
lo=0, hi=0 → return nums[0] = 11 ✅
```

### Code

```cpp
class Solution {
public:
    int findMin(vector<int>& nums) {
        int lo = 0, hi = (int)nums.size() - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] > nums[hi]) lo = mid + 1;   // min is in right half
            else hi = mid;                            // min is at mid or left
        }
        return nums[lo];
    }
};
```
```java
class Solution {
    public int findMin(int[] nums) {
        int lo = 0, hi = nums.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] > nums[hi]) lo = mid + 1;   // min is in right half
            else hi = mid;                            // min is at mid or left
        }
        return nums[lo];
    }
}
```
```python
class Solution:
    def findMin(self, nums: List[int]) -> int:
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] > nums[hi]:
                lo = mid + 1      # min is in right half
            else:
                hi = mid          # min is at mid or left
        return nums[lo]
```

### Complexity
- **Time**: O(log n) — the window halves each iteration.
- **Space**: O(1).

### Verdict
**The optimal answer.** It meets the O(log n) requirement by exploiting the "one sorted drop" structure. The `nums[mid] vs nums[hi]` comparison is the heart of every rotated-array binary search — study it until it's automatic.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Uses rotation structure | When to mention |
|----------|------|-------|-------------------------|-----------------|
| Linear scan | O(n) | O(1) | no | baseline only |
| Pivot binary search | **O(log n)** | O(1) | yes | the required optimal answer ⭐ |

The single idea that unlocks it: *"a rotated sorted array is two ascending runs; compare the midpoint to the right boundary to find which side holds the drop."*

---

## 🧪 Edge cases & pitfalls
- **Not rotated / rotated n times** (`[1,2,3]`, `[11,13,15,17]`) → every `nums[mid] <= nums[hi]`, so `hi` marches left to index 0 → returns `nums[0]`. Handled.
- **Single element** (`n = 1`) → `lo == hi == 0`, loop doesn't run, returns `nums[0]`.
- **Two elements** (`[2,1]` or `[1,2]`) → one iteration resolves correctly.
- **Pitfall — comparing to `nums[lo]`**: tempting but trickier; in a window that is already sorted, `nums[mid] > nums[lo]` would push you right and miss the minimum at `lo`. Comparing to `nums[hi]` is the clean choice.
- **Pitfall — `while (lo <= hi)` here**: this is a *converge-to-boundary* search, so use `while (lo < hi)` with `hi = mid` (not `mid - 1`). Using `<=` with `hi = mid` would loop forever when `lo == hi`.
- **Pitfall — `lo = mid` instead of `mid + 1`**: on the "go right" branch you must use `mid + 1`, since `nums[mid] > nums[hi]` proves `mid` is *not* the minimum.
- **Note on duplicates** — this solution assumes unique values. With duplicates (LC 154), `nums[mid] == nums[hi]` is ambiguous and needs an extra `hi--` step.

---

## 🔗 Related problems
- **Find Minimum in Rotated Sorted Array II** (LC 154) — allows duplicates; handle the `nums[mid] == nums[hi]` tie with `hi--`.
- **Search in Rotated Sorted Array** (LC 33) — the next problem; find a target, often by first finding this pivot.
- **Search in Rotated Sorted Array II** (LC 81) — rotated search with duplicates.
- **Find Peak Element** (LC 162) — binary search guided by a local comparison rather than a target.

---

**→ Next:** [`05-Search-Rotated-Sorted-Array.md`](./05-Search-Rotated-Sorted-Array.md) | **→ Prev:** [`03-Koko-Eating-Bananas.md`](./03-Koko-Eating-Bananas.md) | [Problem set index](./00-Index.md)
