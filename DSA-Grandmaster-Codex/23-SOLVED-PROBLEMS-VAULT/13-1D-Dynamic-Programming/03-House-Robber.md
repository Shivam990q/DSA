# House Robber

**Platform**: LeetCode 198 · **Difficulty**: Medium · **Topics**: Array, Dynamic Programming · **Pattern**: Linear recurrence — take/skip (non-adjacent max sum)

---

## 📜 Problem Statement

You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. The only constraint stopping you from robbing each of them is that **adjacent houses have security systems connected**, and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array `nums` representing the amount of money of each house, return the **maximum amount of money** you can rob tonight **without alerting the police**.

### Examples

**Example 1:**
```
Input:  nums = [1, 2, 3, 1]
Output: 4
Explanation: Rob house 0 (money = 1) and house 2 (money = 3).
Total = 1 + 3 = 4.
```

**Example 2:**
```
Input:  nums = [2, 7, 9, 3, 1]
Output: 12
Explanation: Rob house 0 (2), house 2 (9), and house 4 (1).
Total = 2 + 9 + 1 = 12.
```

**Example 3:**
```
Input:  nums = [2, 1, 1, 2]
Output: 4
Explanation: Rob house 0 (2) and house 3 (2). Total = 4.
```

### Constraints
```
1 <= nums.length <= 100
0 <= nums[i] <= 400
```

---

## 🧠 Understanding the problem

At each house you make a binary choice: **rob it** or **skip it**. If you rob house `i`, you cannot have robbed `i-1`, so your best total is `nums[i]` plus the best you could do up to `i-2`. If you skip house `i`, your best total is whatever you had up to `i-1`.

5-step framework:
1. **State**: `dp[i]` = maximum money robbing from houses `0..i`.
2. **Transition**: `dp[i] = max(dp[i-1], dp[i-2] + nums[i])` — skip vs rob.
3. **Base case**: `dp[0] = nums[0]`, `dp[1] = max(nums[0], nums[1])`.
4. **Order**: `i` from `2` to `n-1`.
5. **Answer**: `dp[n-1]`; depends only on the last two entries → O(1) space.

---

## Approach 1 — Top-down memoization

### Intuition
`solve(i)` = best loot considering houses `0..i`. At house `i` choose the better of robbing (`nums[i] + solve(i-2)`) or skipping (`solve(i-1)`).

### Algorithm
1. Base: `solve(i) = 0` for `i < 0`; `solve(0) = nums[0]`.
2. `solve(i) = max(solve(i-1), solve(i-2) + nums[i])`.
3. Memoize on `i`.

### Dry run on `nums = [2, 7, 9, 3, 1]`
```
solve(0)=2
solve(1)=max(2,7)=7
solve(2)=max(7, 2+9)=11
solve(3)=max(11, 7+3)=11
solve(4)=max(11, 11+1)=12
```

### Code
```cpp
class Solution {
    vector<int> memo;
    vector<int>* a;
    int solve(int i) {
        if (i < 0) return 0;
        if (memo[i] != -1) return memo[i];
        return memo[i] = max(solve(i - 1), solve(i - 2) + (*a)[i]);
    }
public:
    int rob(vector<int>& nums) {
        a = &nums;
        memo.assign(nums.size(), -1);
        return solve(nums.size() - 1);
    }
};
```
```java
class Solution {
    private int[] memo;
    private int[] nums;
    private int solve(int i) {
        if (i < 0) return 0;
        if (memo[i] != -1) return memo[i];
        return memo[i] = Math.max(solve(i - 1), solve(i - 2) + nums[i]);
    }
    public int rob(int[] nums) {
        this.nums = nums;
        memo = new int[nums.length];
        java.util.Arrays.fill(memo, -1);
        return solve(nums.length - 1);
    }
}
```
```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def solve(i: int) -> int:
            if i < 0:
                return 0
            return max(solve(i - 1), solve(i - 2) + nums[i])

        return solve(len(nums) - 1)
```

### Complexity
- **Time**: O(n).
- **Space**: O(n) memo + stack.

### Verdict
Clear statement of the take/skip choice. Flip it bottom-up next.

---

## Approach 2 — Bottom-up tabulation

### Intuition
Fill `dp` left to right using the recurrence.

### Algorithm
1. `dp[0] = nums[0]`, `dp[1] = max(nums[0], nums[1])`.
2. For `i` from `2`: `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`.
3. Return `dp[n-1]`.

### Dry run on `nums = [1, 2, 3, 1]`
```
dp[0]=1
dp[1]=max(1,2)=2
dp[2]=max(2, 1+3)=4
dp[3]=max(4, 2+1)=4
return 4
```

### Code
```cpp
class Solution {
public:
    int rob(vector<int>& nums) {
        int n = nums.size();
        if (n == 1) return nums[0];
        vector<int> dp(n);
        dp[0] = nums[0];
        dp[1] = max(nums[0], nums[1]);
        for (int i = 2; i < n; i++)
            dp[i] = max(dp[i - 1], dp[i - 2] + nums[i]);
        return dp[n - 1];
    }
};
```
```java
class Solution {
    public int rob(int[] nums) {
        int n = nums.length;
        if (n == 1) return nums[0];
        int[] dp = new int[n];
        dp[0] = nums[0];
        dp[1] = Math.max(nums[0], nums[1]);
        for (int i = 2; i < n; i++)
            dp[i] = Math.max(dp[i - 1], dp[i - 2] + nums[i]);
        return dp[n - 1];
    }
}
```
```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]
        dp = [0] * n
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])
        for i in range(2, n):
            dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
        return dp[n - 1]
```

### Complexity
- **Time**: O(n).
- **Space**: O(n).

### Verdict
Solid; now collapse the array.

---

## Approach 3 — Space-optimized rolling variables (optimal) ⭐

### Intuition
Only the previous two answers matter. Track `prev` (= dp[i-2]) and `cur` (= dp[i-1]).

### Algorithm
1. `prev = 0`, `cur = 0`.
2. For each `x` in `nums`: `next = max(cur, prev + x)`; shift `prev = cur`, `cur = next`.
3. Return `cur`.

### Dry run on `nums = [2, 7, 9, 3, 1]`
```
prev=0, cur=0
x=2: next=max(0,0+2)=2 -> prev=0, cur=2
x=7: next=max(2,0+7)=7 -> prev=2, cur=7
x=9: next=max(7,2+9)=11 -> prev=7, cur=11
x=3: next=max(11,7+3)=11 -> prev=11, cur=11
x=1: next=max(11,11+1)=12 -> cur=12
return 12
```

### Code
```cpp
class Solution {
public:
    int rob(vector<int>& nums) {
        int prev = 0, cur = 0;     // dp[i-2], dp[i-1]
        for (int x : nums) {
            int next = max(cur, prev + x);
            prev = cur;
            cur = next;
        }
        return cur;
    }
};
```
```java
class Solution {
    public int rob(int[] nums) {
        int prev = 0, cur = 0;     // dp[i-2], dp[i-1]
        for (int x : nums) {
            int next = Math.max(cur, prev + x);
            prev = cur;
            cur = next;
        }
        return cur;
    }
}
```
```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        prev = cur = 0             # dp[i-2], dp[i-1]
        for x in nums:
            prev, cur = cur, max(cur, prev + x)
        return cur
```

### Complexity
- **Time**: O(n).
- **Space**: O(1).

### Verdict
**The optimal answer.** Linear time, constant space, and it handles the single-element case naturally (the loop runs once and returns `nums[0]`).

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Memoization | O(n) | O(n) | top-down take/skip |
| Tabulation | O(n) | O(n) | bottom-up array |
| Rolling variables | **O(n)** | **O(1)** | the answer ⭐ |

---

## 🧪 Edge cases & pitfalls
- **Single house** → rob it. The rolling version returns `nums[0]` automatically; the tabulation version needs an explicit `n == 1` guard before touching `dp[1]`.
- **All zeros** → 0.
- **Two houses** → `max(nums[0], nums[1])`.
- **Pitfall — greedy fails**: "always rob the bigger neighbor" or "rob every other house" are both wrong. `[2,1,1,2]` shows you sometimes skip two in a row (rob index 0 and 3). The DP choice is what's correct.
- **Pitfall — initializing `prev/cur` to `nums[0]`**: start both at `0`. Letting the recurrence seed itself avoids special-casing.

---

## 🔗 Related problems
- **House Robber II** (LC 213) — houses in a circle; run this twice.
- **House Robber III** (LC 337) — houses form a binary tree; tree DP.
- **Delete and Earn** (LC 740) — reduces to House Robber after bucketing by value.
- **Maximum Sum of Non-Adjacent Elements** — the generic version of this exact recurrence.

---

**→ Next:** [`04-House-Robber-II.md`](./04-House-Robber-II.md) | **→ Prev:** [`02-Min-Cost-Climbing-Stairs.md`](./02-Min-Cost-Climbing-Stairs.md) | Back to [`00-Index.md`](./00-Index.md)
