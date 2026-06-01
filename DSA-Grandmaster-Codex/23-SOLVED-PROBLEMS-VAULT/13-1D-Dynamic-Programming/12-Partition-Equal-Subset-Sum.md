# Partition Equal Subset Sum

**Platform**: LeetCode 416 · **Difficulty**: Medium · **Topics**: Array, Dynamic Programming · **Pattern**: 0/1 knapsack — subset-sum reachability

---

## 📜 Problem Statement

Given an integer array `nums`, return `true` if you can partition the array into **two subsets** such that the **sum of the elements in both subsets is equal**, or `false` otherwise.

### Examples

**Example 1:**
```
Input:  nums = [1, 5, 11, 5]
Output: true
Explanation: The array can be partitioned as [1, 5, 5] and [11].
```

**Example 2:**
```
Input:  nums = [1, 2, 3, 5]
Output: false
Explanation: The array cannot be partitioned into equal sum subsets.
```

**Example 3:**
```
Input:  nums = [1, 1]
Output: true
Explanation: [1] and [1].
```

### Constraints
```
1 <= nums.length <= 200
1 <= nums[i] <= 100
```

---

## 🧠 Understanding the problem

Two subsets with equal sums means each must equal `total / 2`. So:

- If `total` is **odd**, it's impossible → `false`.
- Otherwise, the question reduces to: **is there a subset summing to exactly `target = total / 2`?** If yes, the rest automatically sums to `target` too.

That's the classic **subset-sum** / 0-1 knapsack decision problem: each number is an item used at most once, and we ask whether a particular capacity is exactly fillable.

5-step framework:
1. **State**: `dp[v]` = is sum `v` reachable using some subset of the numbers seen so far.
2. **Transition**: for a new number `x`, `dp[v] = dp[v] OR dp[v - x]` for `v >= x`.
3. **Base case**: `dp[0] = true` (empty subset sums to 0).
4. **Order**: for each number, sweep `v` **downward** from `target` to `x` (so each number is used at most once).
5. **Answer**: `dp[target]`.

---

## Approach 1 — 2D subset-sum table

### Intuition
`dp[i][v]` = can we reach sum `v` using the first `i` numbers. Each number is either skipped (`dp[i-1][v]`) or taken (`dp[i-1][v - nums[i-1]]`).

### Algorithm
1. If total odd → false. `target = total/2`.
2. `dp[i][0] = true` for all `i`.
3. `dp[i][v] = dp[i-1][v] OR (v >= nums[i-1] AND dp[i-1][v - nums[i-1]])`.
4. Return `dp[n][target]`.

### Dry run on `nums = [1,5,11,5]`, target = 11
```
After 1:        reachable {0,1}
After 1,5:      {0,1,5,6}
After 1,5,11:   {0,1,5,6,11,...} -> 11 reachable -> true
```

### Code
```cpp
class Solution {
public:
    bool canPartition(vector<int>& nums) {
        int total = accumulate(nums.begin(), nums.end(), 0);
        if (total % 2) return false;
        int target = total / 2, n = nums.size();
        vector<vector<bool>> dp(n + 1, vector<bool>(target + 1, false));
        for (int i = 0; i <= n; i++) dp[i][0] = true;
        for (int i = 1; i <= n; i++)
            for (int v = 1; v <= target; v++) {
                dp[i][v] = dp[i - 1][v];
                if (v >= nums[i - 1])
                    dp[i][v] = dp[i][v] || dp[i - 1][v - nums[i - 1]];
            }
        return dp[n][target];
    }
};
```
```java
class Solution {
    public boolean canPartition(int[] nums) {
        int total = 0;
        for (int x : nums) total += x;
        if (total % 2 == 1) return false;
        int target = total / 2, n = nums.length;
        boolean[][] dp = new boolean[n + 1][target + 1];
        for (int i = 0; i <= n; i++) dp[i][0] = true;
        for (int i = 1; i <= n; i++)
            for (int v = 1; v <= target; v++) {
                dp[i][v] = dp[i - 1][v];
                if (v >= nums[i - 1])
                    dp[i][v] = dp[i][v] || dp[i - 1][v - nums[i - 1]];
            }
        return dp[n][target];
    }
}
```
```python
class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        total = sum(nums)
        if total % 2:
            return False
        target, n = total // 2, len(nums)
        dp = [[False] * (target + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            dp[i][0] = True
        for i in range(1, n + 1):
            for v in range(1, target + 1):
                dp[i][v] = dp[i - 1][v]
                if v >= nums[i - 1]:
                    dp[i][v] = dp[i][v] or dp[i - 1][v - nums[i - 1]]
        return dp[n][target]
```

### Complexity
- **Time**: O(n × target).
- **Space**: O(n × target).

### Verdict
Correct and explicit. Each row depends only on the previous row, so we can drop to 1D.

---

## Approach 2 — 1D rolling boolean array (optimal) ⭐

### Intuition
Collapse the 2D table to a single boolean array `dp[v]`. To preserve the 0/1 semantics (each number used at most once), sweep `v` **from high to low** so that `dp[v - x]` still refers to the state *before* this number was considered.

### Algorithm
1. If total odd → false. `target = total/2`. `dp[0] = true`.
2. For each `x`, for `v` from `target` down to `x`: `dp[v] = dp[v] OR dp[v - x]`.
3. Optional early exit: if `dp[target]` becomes true, return true.
4. Return `dp[target]`.

### Dry run on `nums = [1,5,11,5]`, target = 11
```
dp[0]=true
x=1:  dp[1]=true
x=5:  dp[6]=dp[1], dp[5]=dp[0] -> {0,1,5,6}
x=11: dp[11]=dp[0] -> true! return true
```

### Code
```cpp
class Solution {
public:
    bool canPartition(vector<int>& nums) {
        int total = accumulate(nums.begin(), nums.end(), 0);
        if (total % 2) return false;
        int target = total / 2;
        vector<bool> dp(target + 1, false);
        dp[0] = true;
        for (int x : nums)
            for (int v = target; v >= x; v--)
                dp[v] = dp[v] || dp[v - x];
        return dp[target];
    }
};
```
```java
class Solution {
    public boolean canPartition(int[] nums) {
        int total = 0;
        for (int x : nums) total += x;
        if (total % 2 == 1) return false;
        int target = total / 2;
        boolean[] dp = new boolean[target + 1];
        dp[0] = true;
        for (int x : nums)
            for (int v = target; v >= x; v--)
                dp[v] = dp[v] || dp[v - x];
        return dp[target];
    }
}
```
```python
class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        total = sum(nums)
        if total % 2:
            return False
        target = total // 2
        dp = [False] * (target + 1)
        dp[0] = True
        for x in nums:
            for v in range(target, x - 1, -1):
                dp[v] = dp[v] or dp[v - x]
        return dp[target]
```

### Complexity
- **Time**: O(n × target).
- **Space**: O(target).

### Verdict
**The optimal answer.** Same time, linear space. The downward sweep is the heart of 0/1 knapsack — memorize it.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| 2D table | O(n·target) | O(n·target) | explicit, easy to follow |
| 1D rolling array | **O(n·target)** | **O(target)** | the answer ⭐ |

A bitset trick (C++ `std::bitset`) can shift the whole reachable set in one operation: `bits |= bits << x`, giving a ~64× constant-factor speedup.

---

## 🧪 Edge cases & pitfalls
- **Odd total** → immediate `false`; the cheapest possible check.
- **Single element** → `false` (can't split one number into two non-empty equal subsets; total is that number, odd unless... even total with one element means the other subset is empty, summing to 0 ≠ target). The parity/`dp[target]` logic returns false correctly.
- **`[1,1]`** → target 1, reachable → true.
- **Pitfall — sweeping `v` upward**: forward iteration would let a single number be reused (turning it into unbounded knapsack), wrongly accepting things like a subset that double-counts one element. Always sweep downward for 0/1.
- **Pitfall — forgetting `dp[0] = true`**: without the empty-subset base case, nothing is reachable.

---

## 🔗 Related problems
- **Target Sum** (LC 494) — assign ± signs; reduces to subset-sum counting.
- **0/1 Knapsack** (classic) — the value-maximizing parent of this decision problem.
- **Partition to K Equal Sum Subsets** (LC 698) — generalize to k subsets (backtracking + DP).
- **Last Stone Weight II** (LC 1049) — minimize the difference of two subset sums (same DP, different read-off).

---

**→ Next:** [`../14-2D-Dynamic-Programming/00-Index.md`](../14-2D-Dynamic-Programming/00-Index.md) | **→ Prev:** [`11-Longest-Increasing-Subsequence.md`](./11-Longest-Increasing-Subsequence.md) | Back to [`00-Index.md`](./00-Index.md)
