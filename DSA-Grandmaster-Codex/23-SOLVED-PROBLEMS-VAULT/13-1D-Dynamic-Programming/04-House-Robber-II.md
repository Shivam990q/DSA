# House Robber II

**Platform**: LeetCode 213 · **Difficulty**: Medium · **Topics**: Array, Dynamic Programming · **Pattern**: Circular constraint → split into two linear subproblems

---

## 📜 Problem Statement

You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. All houses at this place are **arranged in a circle**. That means the **first house is the neighbor of the last one**. Meanwhile, adjacent houses have a security system connected, and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array `nums` representing the amount of money of each house, return the **maximum amount of money** you can rob tonight **without alerting the police**.

### Examples

**Example 1:**
```
Input:  nums = [2, 3, 2]
Output: 3
Explanation: You cannot rob house 0 (money = 2) and house 2 (money = 2),
because they are adjacent (circle). The best single choice is house 1 (money = 3).
```

**Example 2:**
```
Input:  nums = [1, 2, 3, 1]
Output: 4
Explanation: Rob house 0 (money = 1) and house 2 (money = 3).
Total = 1 + 3 = 4.
```

**Example 3:**
```
Input:  nums = [1, 2, 3]
Output: 3
Explanation: Houses 0 and 2 are adjacent. Best is to rob house 2 alone (or house 1).
```

### Constraints
```
1 <= nums.length <= 100
0 <= nums[i] <= 1000
```

---

## 🧠 Understanding the problem

This is [House Robber](./03-House-Robber.md) with one twist: house `0` and house `n-1` are now **adjacent**, so they can never both be robbed.

**Key insight**: that single extra constraint splits every valid plan into two mutually exclusive families:
- Plans that **exclude the last house** → rob within range `[0 .. n-2]`.
- Plans that **exclude the first house** → rob within range `[1 .. n-1]`.

Any optimal plan belongs to at least one family (it cannot rob both ends). So run the *linear* House Robber on each range and take the larger result. We safely ignore the "rob neither end" plans because they are subsumed by both ranges.

5-step framework: the inner routine is identical to House Robber (state `dp[i]` = best loot up to house `i` within the chosen range). The outer step is the split.

---

## Approach 1 — Two linear runs (optimal) ⭐

### Intuition
Solve the linear problem twice on the two ranges, then `max` them. The single-house case is special: there's no "circle," so just return that house.

### Algorithm
1. If `n == 1`, return `nums[0]`.
2. Compute `robLinear(0, n-2)` and `robLinear(1, n-1)` using the standard non-adjacent recurrence.
3. Return the max of the two.

Where `robLinear(lo, hi)` runs `cur = max(cur, prev + nums[i])` across `i` from `lo` to `hi`.

### Dry run on `nums = [1, 2, 3, 1]`
```
Range A = [1,2,3] (indices 0..2): best = max picks of {1,2,3 non-adj} = 1+3 = 4
Range B = [2,3,1] (indices 1..3): best = 2+1 = 3  (or 3 alone)
answer = max(4, 3) = 4
```

### Dry run on `nums = [2, 3, 2]`
```
Range A = indices 0..1 -> {2,3} -> max = 3
Range B = indices 1..2 -> {3,2} -> max = 3
answer = 3
```

### Code
```cpp
class Solution {
    int robLinear(vector<int>& nums, int lo, int hi) {
        int prev = 0, cur = 0;
        for (int i = lo; i <= hi; i++) {
            int next = max(cur, prev + nums[i]);
            prev = cur;
            cur = next;
        }
        return cur;
    }
public:
    int rob(vector<int>& nums) {
        int n = nums.size();
        if (n == 1) return nums[0];
        return max(robLinear(nums, 0, n - 2),
                   robLinear(nums, 1, n - 1));
    }
};
```
```java
class Solution {
    private int robLinear(int[] nums, int lo, int hi) {
        int prev = 0, cur = 0;
        for (int i = lo; i <= hi; i++) {
            int next = Math.max(cur, prev + nums[i]);
            prev = cur;
            cur = next;
        }
        return cur;
    }
    public int rob(int[] nums) {
        int n = nums.length;
        if (n == 1) return nums[0];
        return Math.max(robLinear(nums, 0, n - 2),
                        robLinear(nums, 1, n - 1));
    }
}
```
```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        def linear(lo: int, hi: int) -> int:
            prev = cur = 0
            for i in range(lo, hi + 1):
                prev, cur = cur, max(cur, prev + nums[i])
            return cur

        return max(linear(0, len(nums) - 2),
                   linear(1, len(nums) - 1))
```

### Complexity
- **Time**: O(n) — two linear passes.
- **Space**: O(1).

### Verdict
**The optimal answer.** The whole trick is reducing a circular constraint to two linear problems. Memorize the reduction; the inner loop is just House Robber.

---

## Approach 2 — Same reduction, tabulation inner routine

### Intuition
If you prefer an explicit `dp` array inside, the reduction is identical — only the linear helper changes. Shown for completeness; it costs O(n) extra space for no benefit.

### Algorithm
Same split; the helper builds a `dp` array over the slice `[lo..hi]`.

### Code
```cpp
class Solution {
    int robLinear(vector<int>& nums, int lo, int hi) {
        if (lo > hi) return 0;
        int len = hi - lo + 1;
        vector<int> dp(len + 1, 0);   // dp[k] handles slice prefix of length k
        dp[1] = nums[lo];
        for (int k = 2; k <= len; k++)
            dp[k] = max(dp[k - 1], dp[k - 2] + nums[lo + k - 1]);
        return dp[len];
    }
public:
    int rob(vector<int>& nums) {
        int n = nums.size();
        if (n == 1) return nums[0];
        return max(robLinear(nums, 0, n - 2), robLinear(nums, 1, n - 1));
    }
};
```
```java
class Solution {
    private int robLinear(int[] nums, int lo, int hi) {
        if (lo > hi) return 0;
        int len = hi - lo + 1;
        int[] dp = new int[len + 1];
        dp[1] = nums[lo];
        for (int k = 2; k <= len; k++)
            dp[k] = Math.max(dp[k - 1], dp[k - 2] + nums[lo + k - 1]);
        return dp[len];
    }
    public int rob(int[] nums) {
        int n = nums.length;
        if (n == 1) return nums[0];
        return Math.max(robLinear(nums, 0, n - 2), robLinear(nums, 1, n - 1));
    }
}
```
```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        def linear(lo: int, hi: int) -> int:
            if lo > hi:
                return 0
            length = hi - lo + 1
            dp = [0] * (length + 1)
            dp[1] = nums[lo]
            for k in range(2, length + 1):
                dp[k] = max(dp[k - 1], dp[k - 2] + nums[lo + k - 1])
            return dp[length]

        return max(linear(0, len(nums) - 2), linear(1, len(nums) - 1))
```

### Complexity
- **Time**: O(n).
- **Space**: O(n) for the inner table.

### Verdict
Same idea, more memory. Prefer Approach 1.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Two linear runs (rolling) | **O(n)** | **O(1)** | the answer ⭐ |
| Two linear runs (tabulation) | O(n) | O(n) | explicit table, no upside |

---

## 🧪 Edge cases & pitfalls
- **Single house** → must short-circuit and return `nums[0]`; otherwise the ranges `[0, -1]` and `[1, 0]` are empty/invalid and you'd return 0.
- **Two houses** → ranges become `[0,0]` and `[1,1]`, giving `max(nums[0], nums[1])`. Correct (they're adjacent in the circle).
- **Pitfall — trying both ends and subtracting**: don't try to "rob everything then fix the ends." The clean split into two ranges is provably correct and far simpler.
- **Pitfall — off-by-one on ranges**: it's `[0, n-2]` and `[1, n-1]`, i.e. drop the last house in one and the first house in the other.

---

## 🔗 Related problems
- **House Robber** (LC 198) — the linear base case used twice here.
- **House Robber III** (LC 337) — tree-shaped houses.
- **Maximum Sum Circular Subarray** (LC 918) — another "linear trick applied to a circle" problem (rob-all minus the worst middle).
- **Delete and Earn** (LC 740) — reduces to House Robber.

---

**→ Next:** [`05-Longest-Palindromic-Substring.md`](./05-Longest-Palindromic-Substring.md) | **→ Prev:** [`03-House-Robber.md`](./03-House-Robber.md) | Back to [`00-Index.md`](./00-Index.md)
