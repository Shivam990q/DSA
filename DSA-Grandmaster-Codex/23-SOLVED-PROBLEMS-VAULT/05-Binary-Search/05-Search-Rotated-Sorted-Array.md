# Search in Rotated Sorted Array

**Platform**: LeetCode 33 · **Difficulty**: Medium · **Topics**: Array, Binary Search · **Pattern**: Sorted-half detection in a rotated array

---

## 📜 Problem Statement

There is an integer array `nums` sorted in ascending order (with **distinct** values).

Prior to being passed to your function, `nums` is possibly **rotated** at an unknown pivot index `k` (`1 <= k < nums.length`) such that the resulting array is `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]` (**0-indexed**). For example, `[0,1,2,4,5,6,7]` might be rotated at pivot index `3` and become `[4,5,6,7,0,1,2]`.

Given the array `nums` **after** the possible rotation and an integer `target`, return the **index** of `target` if it is in `nums`, or `-1` if it is not in `nums`.

You must write an algorithm with **O(log n)** runtime complexity.

### Examples

**Example 1:**
```
Input:  nums = [4,5,6,7,0,1,2], target = 0
Output: 4
```

**Example 2:**
```
Input:  nums = [4,5,6,7,0,1,2], target = 3
Output: -1
```

**Example 3:**
```
Input:  nums = [1], target = 0
Output: -1
```

### Constraints
```
1 <= nums.length <= 5000
-10^4 <= nums[i] <= 10^4
All values of nums are unique.
nums is an ascending array that is possibly rotated.
-10^4 <= target <= 10^4
```

---

## 🧠 Understanding the problem

This is the rotated array from LC 153, but now we want the **index of a specific target**, not the minimum. The array is two ascending runs:

```
[4, 5, 6, 7, 0, 1, 2]    target = 0
 \_______/  \_______/
  left run    right run
```

A plain binary search fails because `nums[mid] < target` no longer reliably tells us which half to keep — the rotation breaks the global ordering.

The saving grace: **at any midpoint, at least one of the two halves `[lo..mid]` or `[mid..hi]` is fully sorted** (no drop inside it). If we can tell which half is sorted, we can use ordinary range checks on that sorted half to decide where the target is:

- Detect the sorted half by comparing `nums[lo]` to `nums[mid]`:
  - If `nums[lo] <= nums[mid]` → the **left half is sorted**.
  - Otherwise → the **right half is sorted**.
- Then ask: does `target` fall **within the sorted half's value range**?
  - If yes → search that half.
  - If no → search the other half.

That single-pass logic finds the target (or proves it's absent) in O(log n).

---

## Approach 1 — Linear scan (baseline)

### Intuition
Ignore the structure; scan for the target. Baseline only.

### Algorithm
1. For each index `i`: if `nums[i] == target` → return `i`.
2. Return `-1`.

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
- **Time**: O(n).
- **Space**: O(1).

### Verdict
Correct but **violates the required O(log n)**. Baseline only.

---

## Approach 2 — Find pivot, then binary search (two-pass)

### Intuition
Use the LC 153 technique to find the pivot (index of the minimum). The pivot splits the array into two sorted segments. Decide which segment can contain the target by comparing against the endpoints, then run a standard binary search on that segment.

### Algorithm
1. Binary search the pivot `p` (smallest element's index) as in LC 153.
2. Decide the search range:
   - If `target >= nums[0]` and `target <= nums[n-1]`... (in a rotated array, compare against the run that holds the target). Concretely: if `target >= nums[0]`, search `[0, p-1]` (the left run); else search `[p, n-1]` (the right run). Special-case the un-rotated array (`p == 0`).
3. Standard binary search in the chosen range; return the index or `-1`.

### Code

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int n = nums.size();
        // 1) find pivot = index of minimum
        int lo = 0, hi = n - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] > nums[hi]) lo = mid + 1;
            else hi = mid;
        }
        int pivot = lo;
        // 2) choose the sorted segment that may hold target
        lo = 0; hi = n - 1;
        if (pivot > 0 && target >= nums[0] && target <= nums[pivot - 1]) {
            hi = pivot - 1;                 // search left run
        } else {
            lo = pivot;                     // search right run
        }
        // 3) standard binary search
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
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
        int n = nums.length;
        int lo = 0, hi = n - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] > nums[hi]) lo = mid + 1;
            else hi = mid;
        }
        int pivot = lo;
        lo = 0; hi = n - 1;
        if (pivot > 0 && target >= nums[0] && target <= nums[pivot - 1]) {
            hi = pivot - 1;
        } else {
            lo = pivot;
        }
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
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
        n = len(nums)
        lo, hi = 0, n - 1
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] > nums[hi]:
                lo = mid + 1
            else:
                hi = mid
        pivot = lo
        lo, hi = 0, n - 1
        if pivot > 0 and nums[0] <= target <= nums[pivot - 1]:
            hi = pivot - 1
        else:
            lo = pivot
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1
```

### Complexity
- **Time**: O(log n) — two binary searches, each O(log n).
- **Space**: O(1).

### Verdict
Correct and O(log n), and conceptually clean ("first un-rotate the problem"). But it does two passes and has a fiddly segment-selection step. The one-pass version below is tighter and the preferred interview answer.

---

## Approach 3 — One-pass sorted-half search (optimal) ⭐

### Intuition
Don't find the pivot separately. At each step, detect which half is sorted and immediately decide direction using a range check on that half. One binary search does it all.

### Algorithm
1. `lo = 0`, `hi = n - 1`.
2. While `lo <= hi`:
   - `mid = lo + (hi - lo) / 2`.
   - If `nums[mid] == target` → return `mid`.
   - If `nums[lo] <= nums[mid]` (**left half sorted**):
     - If `nums[lo] <= target < nums[mid]` → target is in the left half → `hi = mid - 1`.
     - Else → `lo = mid + 1`.
   - Else (**right half sorted**):
     - If `nums[mid] < target <= nums[hi]` → target is in the right half → `lo = mid + 1`.
     - Else → `hi = mid - 1`.
3. Return `-1`.

### Dry run on `nums = [4,5,6,7,0,1,2]`, `target = 0`
```
lo=0, hi=6
  mid = 3 → nums[3]=7 ≠ 0
  nums[lo]=4 <= nums[mid]=7 → LEFT half [4..7] sorted
    is 4 <= 0 < 7? no → go right → lo=4
lo=4, hi=6
  mid = 5 → nums[5]=1 ≠ 0
  nums[lo]=0 <= nums[mid]=1 → LEFT half [0..1] sorted
    is 0 <= 0 < 1? yes → go left → hi=4
lo=4, hi=4
  mid = 4 → nums[4]=0 == 0 → return 4 ✅
```

A "not found" trace, `target = 3`:
```
lo=0, hi=6
  mid=3 → 7≠3; left [4..7] sorted; 4<=3<7? no → lo=4
lo=4, hi=6
  mid=5 → 1≠3; left [0..1] sorted; 0<=3<1? no → lo=6
lo=6, hi=6
  mid=6 → nums[6]=2 ≠ 3; left [2..2] sorted; 2<=3<2? no → lo=7
lo=7 > hi=6 → return -1 ✅
```

### Code

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int lo = 0, hi = (int)nums.size() - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] == target) return mid;
            if (nums[lo] <= nums[mid]) {                 // left half sorted
                if (nums[lo] <= target && target < nums[mid]) hi = mid - 1;
                else lo = mid + 1;
            } else {                                     // right half sorted
                if (nums[mid] < target && target <= nums[hi]) lo = mid + 1;
                else hi = mid - 1;
            }
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
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] == target) return mid;
            if (nums[lo] <= nums[mid]) {                 // left half sorted
                if (nums[lo] <= target && target < nums[mid]) hi = mid - 1;
                else lo = mid + 1;
            } else {                                     // right half sorted
                if (nums[mid] < target && target <= nums[hi]) lo = mid + 1;
                else hi = mid - 1;
            }
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
            mid = lo + (hi - lo) // 2
            if nums[mid] == target:
                return mid
            if nums[lo] <= nums[mid]:                    # left half sorted
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:                                        # right half sorted
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1
                else:
                    hi = mid - 1
        return -1
```

### Complexity
- **Time**: O(log n) — one binary search, constant work per step.
- **Space**: O(1).

### Verdict
**The optimal answer.** One clean pass, no separate pivot hunt. The pattern — *"identify the sorted half, range-check the target against it, recurse into the right side"* — generalizes to many rotated-array problems.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Passes | When to mention |
|----------|------|-------|--------|-----------------|
| Linear scan | O(n) | O(1) | 1 | baseline only |
| Find pivot + search | O(log n) | O(1) | 2 | clear mental model ("un-rotate first") |
| One-pass sorted-half | **O(log n)** | O(1) | 1 | the preferred optimal answer ⭐ |

Both binary approaches are O(log n); the one-pass version is tighter and less error-prone once you trust the sorted-half logic.

---

## 🧪 Edge cases & pitfalls
- **Single element** (`[1]`) → checked directly; returns `0` if it matches, else `-1`.
- **Not rotated** (`[1,2,3,4,5]`) → `nums[lo] <= nums[mid]` always true → degenerates to plain binary search.
- **Target at the pivot / wrap boundary** → the range checks `nums[lo] <= target < nums[mid]` and `nums[mid] < target <= nums[hi]` use the right `<` vs `<=` so boundaries aren't missed.
- **Pitfall — `<=` vs `<` in the range checks**: the sorted-half *includes* its left endpoint (`nums[lo] <= target`) but the comparison against `nums[mid]` is strict (`target < nums[mid]`) because `nums[mid] == target` was already handled. Mixing these up causes infinite loops or wrong answers.
- **Pitfall — using `nums[lo] < nums[mid]` (strict)**: when `lo == mid` (window of size 1 or 2), `nums[lo] == nums[mid]`; you need `<=` so the left half is still treated as sorted.
- **Pitfall — comparing against `nums[hi]` to detect the sorted half**: also works but flips the logic; pick one convention (`nums[lo] <= nums[mid]`) and stick to it.

---

## 🔗 Related problems
- **Find Minimum in Rotated Sorted Array** (LC 153) — the previous problem; the pivot search powers Approach 2 here.
- **Search in Rotated Sorted Array II** (LC 81) — allows duplicates; the `nums[lo] == nums[mid]` ambiguity needs an extra `lo++` step (worst case O(n)).
- **Binary Search** (LC 704) — the un-rotated base case.
- **Find Minimum in Rotated Sorted Array II** (LC 154) — duplicates variant of the pivot search.

---

**→ Next:** [`06-Time-Based-Key-Value-Store.md`](./06-Time-Based-Key-Value-Store.md) | **→ Prev:** [`04-Find-Minimum-Rotated-Sorted-Array.md`](./04-Find-Minimum-Rotated-Sorted-Array.md) | [Problem set index](./00-Index.md)
