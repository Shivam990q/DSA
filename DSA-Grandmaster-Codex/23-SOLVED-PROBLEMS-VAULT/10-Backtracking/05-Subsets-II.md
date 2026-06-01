# Subsets II

**Platform**: LeetCode 90 · **Difficulty**: Medium · **Topics**: Array, Backtracking, Bit Manipulation · **Pattern**: Power set + skip-dup-at-level

---

## 📜 Problem Statement

Given an integer array `nums` that **may contain duplicates**, return *all possible subsets (the power set)*.

The solution set **must not** contain duplicate subsets. Return the solution in **any order**.

### Examples

**Example 1:**
```
Input:  nums = [1, 2, 2]
Output: [[], [1], [1,2], [1,2,2], [2], [2,2]]
Explanation: Although there are two 2's, subsets like [2] and [1,2]
             must appear only once.
```

**Example 2:**
```
Input:  nums = [0]
Output: [[], [0]]
```

**Example 3:**
```
Input:  nums = [4, 4, 4, 1, 4]
Output: [[], [1], [1,4], [1,4,4], [1,4,4,4], [1,4,4,4,4],
         [4], [4,4], [4,4,4], [4,4,4,4]]
```

### Constraints
```
1 <= nums.length <= 10
-10 <= nums[i] <= 10
```

---

## 🧠 Understanding the problem

This is [Subsets](./01-Subsets.md) with one wrinkle: the input may contain **duplicate values**, and the power set must contain each distinct subset **once**. If `nums = [1,2,2]`, the naive `2^n` enumeration would produce `[2]` twice (once for each physical `2`) and `[1,2]` twice — we must collapse those.

The cure is identical to [Combination Sum II](./03-Combination-Sum-II.md): **sort** so equal values are adjacent, then within a recursion level skip a value equal to the one just tried — `if (i > start && nums[i] == nums[i-1]) continue;`. The first occurrence of a value at a level may branch (so deeper levels can still build `[2,2]`), but a duplicate *sibling* branch is pruned (so `[2]` is recorded once). As in plain Subsets, we record at **every node** because every node is a valid subset.

With `n <= 10` the search is tiny; correctness (no duplicates, none missed) is the whole challenge.

---

## Approach 1 — Sort + backtracking + skip-dup-at-level ⭐

### Intuition
Sort to cluster equal values. Walk forward with a `start` index (order doesn't matter — it's subsets). Record the path at every node. The only addition over plain Subsets is the level-dedup guard: skip `nums[i]` when it repeats the previous value *at the same level*, because that sibling branch would regenerate subsets the first branch already produced.

### Algorithm
1. **Sort** `nums`.
2. `backtrack(start)`:
   - Record a copy of `cur` (valid subset).
   - For `i` from `start` to `n-1`:
     - If `i > start && nums[i] == nums[i-1]` → **continue** (skip duplicate at this level).
     - **choose** `nums[i]`.
     - **explore** `backtrack(i + 1)` (forward only).
     - **un-choose** (pop).

### Dry run on `[1, 2, 2]`
```
sort → [1,2,2]
bt(0) cur=[]            RECORD []
 i=0 (1) → bt(1) cur=[1]   RECORD [1]
   i=1 (2) → bt(2) cur=[1,2]   RECORD [1,2]
     i=2 (2) → bt(3) cur=[1,2,2]  RECORD [1,2,2]
   i=2 (2) → SKIP (i>start, nums[2]==nums[1])
 i=1 (2) → bt(2) cur=[2]    RECORD [2]
   i=2 (2) → bt(3) cur=[2,2]   RECORD [2,2]
 i=2 (2) → SKIP (i>start, nums[2]==nums[1])
Result: [], [1], [1,2], [1,2,2], [2], [2,2]
```
The two SKIPs are exactly what prevents the duplicate `[2]` and `[1,2]`.

### Code
```cpp
class Solution {
public:
    void backtrack(int start, vector<int>& nums,
                   vector<int>& cur, vector<vector<int>>& res) {
        res.push_back(cur);                          // every node is a subset
        for (int i = start; i < (int)nums.size(); i++) {
            if (i > start && nums[i] == nums[i-1]) continue; // skip dup at level
            cur.push_back(nums[i]);                  // choose
            backtrack(i + 1, nums, cur, res);        // explore (forward only)
            cur.pop_back();                          // un-choose
        }
    }
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<vector<int>> res;
        vector<int> cur;
        backtrack(0, nums, cur, res);
        return res;
    }
};
```
```java
class Solution {
    public List<List<Integer>> subsetsWithDup(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> res = new ArrayList<>();
        backtrack(0, nums, new ArrayList<>(), res);
        return res;
    }
    private void backtrack(int start, int[] nums, List<Integer> cur,
                           List<List<Integer>> res) {
        res.add(new ArrayList<>(cur));                 // every node is a subset
        for (int i = start; i < nums.length; i++) {
            if (i > start && nums[i] == nums[i-1]) continue; // skip dup at level
            cur.add(nums[i]);                          // choose
            backtrack(i + 1, nums, cur, res);          // explore (forward only)
            cur.remove(cur.size() - 1);                // un-choose
        }
    }
}
```
```python
class Solution:
    def subsetsWithDup(self, nums):
        nums.sort()
        res = []
        def backtrack(start, cur):
            res.append(cur[:])                         # every node is a subset
            for i in range(start, len(nums)):
                if i > start and nums[i] == nums[i-1]:
                    continue                           # skip dup at level
                cur.append(nums[i])                    # choose
                backtrack(i + 1, cur)                  # explore (forward only)
                cur.pop()                              # un-choose
        backtrack(0, [])
        return res
```

### Complexity
- **Time**: O(n · 2^n) worst case (all distinct); fewer when duplicates collapse branches.
- **Space**: O(n) recursion depth + path; plus the sort.

---

## Approach 2 — Count distinct values, take 0..count of each

### Intuition
Group equal values. A subset is fully described by *how many copies* of each distinct value it takes — from `0` up to that value's frequency. Looping over those counts produces each distinct subset exactly once, no `i > start` guard needed.

### Algorithm
1. Sort (or build a frequency map of `(value, count)` pairs).
2. `backtrack(idx)` over the distinct values:
   - If `idx == #distinct`: record `cur`; return.
   - For `k` from `0` to `count[idx]`:
     - append `k` copies of `value[idx]` to `cur`, recurse `backtrack(idx + 1)`, then remove those `k` copies.

### Dry run on `[1, 2, 2]`
```
distinct = [(1,1), (2,2)]
idx=0 take 0 of '1' → idx=1
        take 0 of '2' → RECORD []
        take 1 of '2' → RECORD [2]
        take 2 of '2' → RECORD [2,2]
idx=0 take 1 of '1' → cur=[1] → idx=1
        take 0 → RECORD [1]
        take 1 → RECORD [1,2]
        take 2 → RECORD [1,2,2]
Result: [], [2], [2,2], [1], [1,2], [1,2,2]
```

### Code
```cpp
class Solution {
public:
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<pair<int,int>> vc;                 // (value, count)
        for (int x : nums) {
            if (!vc.empty() && vc.back().first == x) vc.back().second++;
            else vc.push_back({x, 1});
        }
        vector<vector<int>> res;
        vector<int> cur;
        function<void(int)> bt = [&](int idx) {
            if (idx == (int)vc.size()) { res.push_back(cur); return; }
            for (int k = 0; k <= vc[idx].second; k++) {
                for (int t = 0; t < k; t++) cur.push_back(vc[idx].first);
                bt(idx + 1);
                for (int t = 0; t < k; t++) cur.pop_back();
            }
        };
        bt(0);
        return res;
    }
};
```
```java
class Solution {
    public List<List<Integer>> subsetsWithDup(int[] nums) {
        Arrays.sort(nums);
        List<int[]> vc = new ArrayList<>();        // (value, count)
        for (int x : nums) {
            if (!vc.isEmpty() && vc.get(vc.size()-1)[0] == x) vc.get(vc.size()-1)[1]++;
            else vc.add(new int[]{x, 1});
        }
        List<List<Integer>> res = new ArrayList<>();
        bt(0, vc, new ArrayList<>(), res);
        return res;
    }
    private void bt(int idx, List<int[]> vc, List<Integer> cur,
                    List<List<Integer>> res) {
        if (idx == vc.size()) { res.add(new ArrayList<>(cur)); return; }
        int val = vc.get(idx)[0], cnt = vc.get(idx)[1];
        for (int k = 0; k <= cnt; k++) {
            for (int t = 0; t < k; t++) cur.add(val);
            bt(idx + 1, vc, cur, res);
            for (int t = 0; t < k; t++) cur.remove(cur.size() - 1);
        }
    }
}
```
```python
class Solution:
    def subsetsWithDup(self, nums):
        nums.sort()
        vc = []                                    # (value, count)
        for x in nums:
            if vc and vc[-1][0] == x:
                vc[-1][1] += 1
            else:
                vc.append([x, 1])
        res = []
        cur = []
        def bt(idx):
            if idx == len(vc):
                res.append(cur[:]); return
            val, cnt = vc[idx]
            for k in range(cnt + 1):
                cur.extend([val] * k)
                bt(idx + 1)
                if k:
                    del cur[-k:]
        bt(0)
        return res
```

### Complexity
- **Time**: O(n · 2^n) worst case (all distinct ⇒ each count is 0 or 1).
- **Space**: O(n) for the path, distinct-value list, and recursion.

---

## ⚖️ Approach comparison

| Approach | Time | Space | When to mention |
|----------|------|-------|-----------------|
| Sort + skip-dup-at-level | O(n·2^n) | O(n) | the standard answer; same trick as Combination Sum II ⭐ |
| Count distinct, take 0..k | O(n·2^n) | O(n) | avoids the `i>start` guard; cleaner reasoning about "how many copies" |

---

## 🧪 Edge cases & pitfalls
- **All identical** (`[2,2,2]`) → `[[], [2], [2,2], [2,2,2]]` — `n+1` subsets, not `2^n`.
- **No duplicates** → behaves exactly like plain Subsets (`2^n` outputs); the guard never fires.
- **Pitfall — `i > 0` instead of `i > start`**: would wrongly block building `[2,2]` (the second `2` chosen at a deeper level is legitimate). Use `i > start`.
- **Pitfall — forgetting to sort**: equal values won't be adjacent, so the dedup guard misses them and duplicates leak into the result.
- **Pitfall — recording by reference** instead of a copy → stored subsets mutate on backtrack.

---

## 🔗 Related problems
- **Subsets** (LC 78) — the distinct-element base case. → [01-Subsets.md](./01-Subsets.md)
- **Combination Sum II** (LC 40) — identical dedup trick, plus a target sum. → [03-Combination-Sum-II.md](./03-Combination-Sum-II.md)
- **Permutations II** (LC 47) — dedup for order-matters enumeration.

---

**→ Next:** [`06-Word-Search.md`](./06-Word-Search.md) | [Problem set index](./00-Index.md) | **← Prev:** [`04-Permutations.md`](./04-Permutations.md)
