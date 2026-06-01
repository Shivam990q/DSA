# Permutations

**Platform**: LeetCode 46 · **Difficulty**: Medium · **Topics**: Array, Backtracking · **Pattern**: Order-matters enumeration (used[] / swap)

---

## 📜 Problem Statement

Given an array `nums` of **distinct** integers, return *all the possible permutations*. You can return the answer in **any order**.

### Examples

**Example 1:**
```
Input:  nums = [1, 2, 3]
Output: [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
Explanation: All 3! = 6 orderings.
```

**Example 2:**
```
Input:  nums = [0, 1]
Output: [[0,1], [1,0]]
```

**Example 3:**
```
Input:  nums = [1]
Output: [[1]]
```

### Constraints
```
1 <= nums.length <= 6
-10 <= nums[i] <= 10
All the integers of nums are unique.
```

---

## 🧠 Understanding the problem

A **permutation** is an arrangement where **order matters**: `[1,2,3]` and `[2,1,3]` are different answers. This is the opposite of subsets/combinations. With `n` distinct elements there are `n!` permutations, and each one uses *every* element exactly once.

Because order matters, the "look only forward with a `start` index" trick from combinations is wrong here — that would generate each set in just one order. Instead, at every position we may choose **any element not yet used**. So we need to know *which elements are still available*. Two standard mechanisms:

- a boolean **`used[]`** array (or a hash set) marking elements already placed, or
- **in-place swapping** that partitions `nums` into a "fixed prefix" and an "available suffix."

We record a permutation only at a **leaf** — when the path length equals `n`. With `n <= 6`, `n! <= 720`, so the search is trivially small.

---

## Approach 1 — Backtracking with a `used[]` array ⭐

### Intuition
Build the permutation position by position. At each step scan all elements; skip those already used, otherwise place one, recurse to fill the next position, then unmark on return. The `used[]` array is what replaces the combinations `start` index — it lets every position look at *all* remaining elements, which is exactly what "order matters" requires.

### Algorithm
1. Maintain `cur` (current arrangement) and `used[]` (length `n`, all `false`).
2. `backtrack()`:
   - If `cur.size() == n`: record a copy; return.
   - For `i` from `0` to `n-1`:
     - If `used[i]` → skip.
     - **choose**: `used[i] = true`, append `nums[i]`.
     - **explore**: `backtrack()`.
     - **un-choose**: pop, `used[i] = false`.

### Dry run on `[1, 2, 3]`
```
bt() cur=[]
 i=0 use1 → bt() cur=[1]
   i=1 use2 → bt() cur=[1,2]
     i=2 use3 → bt() cur=[1,2,3] RECORD
   i=2 use3 → bt() cur=[1,3]
     i=1 use2 → cur=[1,3,2] RECORD
 i=1 use2 → cur=[2] → ... → [2,1,3], [2,3,1]
 i=2 use3 → cur=[3] → ... → [3,1,2], [3,2,1]
Result: 6 permutations
```

### Code
```cpp
class Solution {
public:
    void backtrack(vector<int>& nums, vector<int>& cur,
                   vector<bool>& used, vector<vector<int>>& res) {
        if (cur.size() == nums.size()) { res.push_back(cur); return; }
        for (int i = 0; i < (int)nums.size(); i++) {
            if (used[i]) continue;
            used[i] = true; cur.push_back(nums[i]);   // choose
            backtrack(nums, cur, used, res);          // explore
            cur.pop_back(); used[i] = false;          // un-choose
        }
    }
    vector<vector<int>> permute(vector<int>& nums) {
        vector<vector<int>> res;
        vector<int> cur;
        vector<bool> used(nums.size(), false);
        backtrack(nums, cur, used, res);
        return res;
    }
};
```
```java
class Solution {
    public List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> res = new ArrayList<>();
        boolean[] used = new boolean[nums.length];
        backtrack(nums, new ArrayList<>(), used, res);
        return res;
    }
    private void backtrack(int[] nums, List<Integer> cur,
                           boolean[] used, List<List<Integer>> res) {
        if (cur.size() == nums.length) { res.add(new ArrayList<>(cur)); return; }
        for (int i = 0; i < nums.length; i++) {
            if (used[i]) continue;
            used[i] = true; cur.add(nums[i]);          // choose
            backtrack(nums, cur, used, res);           // explore
            cur.remove(cur.size() - 1); used[i] = false; // un-choose
        }
    }
}
```
```python
class Solution:
    def permute(self, nums):
        res = []
        used = [False] * len(nums)
        cur = []
        def backtrack():
            if len(cur) == len(nums):
                res.append(cur[:]); return
            for i in range(len(nums)):
                if used[i]:
                    continue
                used[i] = True; cur.append(nums[i])    # choose
                backtrack()                            # explore
                cur.pop(); used[i] = False             # un-choose
        backtrack()
        return res
```

### Complexity
- **Time**: O(n · n!) — `n!` leaves and O(n) to copy each finished permutation.
- **Space**: O(n) for `used[]`, the `cur` path, and recursion depth (output not counted).

---

## Approach 2 — In-place swapping (no extra array)

### Intuition
Treat index `start` as "the next position to fix." Swap each candidate from `start..n-1` into position `start`, recurse on `start + 1`, then swap back. The prefix `[0..start)` is the decided part; the suffix `[start..n)` is whatever's still available. No `used[]` needed — the array itself encodes availability.

### Algorithm
1. `backtrack(start)`:
   - If `start == n`: record a copy of `nums`; return.
   - For `i` from `start` to `n-1`:
     - swap `nums[start]` and `nums[i]` (**choose** position `start`).
     - `backtrack(start + 1)` (**explore**).
     - swap back (**un-choose**).

### Dry run on `[1, 2, 3]`
```
start=0
 swap(0,0)[1,2,3] → start=1
   swap(1,1)[1,2,3] → start=2 → [1,2,3] RECORD
   swap(1,2)[1,3,2] → [1,3,2] RECORD ; swap back
 swap(0,1)[2,1,3] → ... [2,1,3],[2,3,1] ; swap back
 swap(0,2)[3,2,1] → ... [3,2,1],[3,1,2] ; swap back
```

### Code
```cpp
class Solution {
public:
    void backtrack(int start, vector<int>& nums, vector<vector<int>>& res) {
        if (start == (int)nums.size()) { res.push_back(nums); return; }
        for (int i = start; i < (int)nums.size(); i++) {
            swap(nums[start], nums[i]);       // choose
            backtrack(start + 1, nums, res);  // explore
            swap(nums[start], nums[i]);       // un-choose
        }
    }
    vector<vector<int>> permute(vector<int>& nums) {
        vector<vector<int>> res;
        backtrack(0, nums, res);
        return res;
    }
};
```
```java
class Solution {
    public List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> res = new ArrayList<>();
        backtrack(0, nums, res);
        return res;
    }
    private void backtrack(int start, int[] nums, List<List<Integer>> res) {
        if (start == nums.length) {
            List<Integer> perm = new ArrayList<>();
            for (int x : nums) perm.add(x);
            res.add(perm); return;
        }
        for (int i = start; i < nums.length; i++) {
            swap(nums, start, i);            // choose
            backtrack(start + 1, nums, res); // explore
            swap(nums, start, i);            // un-choose
        }
    }
    private void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }
}
```
```python
class Solution:
    def permute(self, nums):
        res = []
        def backtrack(start):
            if start == len(nums):
                res.append(nums[:]); return
            for i in range(start, len(nums)):
                nums[start], nums[i] = nums[i], nums[start]   # choose
                backtrack(start + 1)                          # explore
                nums[start], nums[i] = nums[i], nums[start]   # un-choose
        backtrack(0)
        return res
```

### Complexity
- **Time**: O(n · n!) — same as Approach 1.
- **Space**: O(n) recursion depth only; no `used[]` array (output not counted).

---

## ⚖️ Approach comparison

| Approach | Time | Space | When to mention |
|----------|------|-------|-----------------|
| `used[]` array | O(n·n!) | O(n) | clearest; generalizes to Permutations II dedup ⭐ |
| In-place swap | O(n·n!) | O(n) (stack only) | when asked to avoid extra memory; note swap output order differs |

Both are optimal. Prefer the `used[]` version when you might extend to duplicate handling (Permutations II), because the swap version's dedup is trickier.

---

## 🧪 Edge cases & pitfalls
- **Single element** `[1]` → `[[1]]`. The first call immediately hits the leaf.
- **Two elements** `[0,1]` → `[[0,1],[1,0]]`.
- **Pitfall — using a `start` index loop** (combinations style) here: that produces only `[1,2,3]` and misses every reordering. Permutations need `used[]` or swap, *not* a forward-only `start`.
- **Pitfall — recording by reference**: in the `used[]` version push a copy of `cur`; in the swap version push a copy of `nums` (it keeps mutating).
- **Pitfall — forgetting to unmark / un-swap** on return corrupts sibling branches.
- **Distinct guarantee**: this problem assumes unique values. With duplicates you'd need [Permutations II](https://leetcode.com/problems/permutations-ii/) (sort + `if i>0 && nums[i]==nums[i-1] && !used[i-1] continue`).

---

## 🔗 Related problems
- **Permutations II** (LC 47) — duplicate inputs; sort + skip-dup with `used[]`.
- **Next Permutation** (LC 31) — generate just the next ordering in place.
- **Subsets** (LC 78) — the order-doesn't-matter sibling; uses `start` instead of `used[]`. → [01-Subsets.md](./01-Subsets.md)
- **Letter Combinations of a Phone Number** (LC 17) — positional branching, a permutation-flavored enumeration. → [08-Letter-Combinations-Phone-Number.md](./08-Letter-Combinations-Phone-Number.md)

---

**→ Next:** [`05-Subsets-II.md`](./05-Subsets-II.md) | [Problem set index](./00-Index.md) | **← Prev:** [`03-Combination-Sum-II.md`](./03-Combination-Sum-II.md)
