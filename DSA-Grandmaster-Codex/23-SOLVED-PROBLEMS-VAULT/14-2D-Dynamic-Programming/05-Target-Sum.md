# Target Sum

**Platform**: LeetCode 494 · **Difficulty**: Medium · **Topics**: Array, Dynamic Programming, Backtracking · **Pattern**: Subset-sum counting via sign transformation

---

## 📜 Problem Statement

You are given an integer array `nums` and an integer `target`.

You want to build an **expression** out of `nums` by adding one of the symbols `'+'` and `'-'` before each integer in `nums` and then concatenate all the integers.
- For example, if `nums = [2, 1]`, you can add a `'+'` before `2` and a `'-'` before `1` and concatenate them to build the expression `"+2-1"`.

Return the **number of different expressions** that you can build, which evaluates to `target`.

### Examples

**Example 1:**
```
Input:  nums = [1, 1, 1, 1, 1], target = 3
Output: 5
Explanation: There are 5 ways to assign symbols to make the sum of nums be target 3.
-1 + 1 + 1 + 1 + 1 = 3
+1 - 1 + 1 + 1 + 1 = 3
+1 + 1 - 1 + 1 + 1 = 3
+1 + 1 + 1 - 1 + 1 = 3
+1 + 1 + 1 + 1 - 1 = 3
```

**Example 2:**
```
Input:  nums = [1], target = 1
Output: 1
```

**Example 3:**
```
Input:  nums = [1, 0], target = 1
Output: 2
Explanation: +1+0 and +1-0 both evaluate to 1 (the 0 can take either sign).
```

### Constraints
```
1 <= nums.length <= 20
0 <= nums[i] <= 1000
0 <= sum(nums[i]) <= 1000
-1000 <= target <= 1000
```

---

## 🧠 Understanding the problem

Split the numbers into a positive set `P` (assigned `+`) and a negative set `N` (assigned `-`). Then:
```
P - N = target
P + N = sum   (total of all numbers)
```
Adding these: `2P = sum + target`, so `P = (sum + target) / 2`.

So the count of valid sign assignments equals the count of **subsets** summing to `P`. This converts a `±` problem into a clean **subset-sum counting** (0/1 knapsack).

Feasibility guards:
- If `|target| > sum`, no assignment can reach it → 0.
- If `sum + target` is **odd**, `P` isn't an integer → 0.

5-step framework (after the transform):
1. **State**: `dp[v]` = number of subsets summing to `v`.
2. **Transition**: for each number `x`, `dp[v] += dp[v - x]` (sweep `v` downward for 0/1).
3. **Base case**: `dp[0] = 1`.
4. **Order**: numbers outer; `v` from `P` down to `x`.
5. **Answer**: `dp[P]`.

---

## Approach 1 — Top-down memoization (no transform)

### Intuition
Directly try `+nums[i]` and `-nums[i]` at each index, tracking the running sum. Memoize on `(index, runningSum)`.

### Algorithm
1. At index `i` with running sum `s`: if `i == n`, return `s == target ? 1 : 0`.
2. Recurse with `s + nums[i]` and `s - nums[i]`; sum the counts.
3. Memoize on `(i, s)` — offset `s` to a non-negative key.

### Dry run on `nums = [1,1], target = 0`
```
+1: then +1 -> 2 (no), -1 -> 0 (yes)
-1: then +1 -> 0 (yes), -1 -> -2 (no)
count = 2
```

### Code
```cpp
class Solution {
    unordered_map<long long, int> memo;   // key encodes (i, sum)
    vector<int>* nums;
    int target, n;
    int solve(int i, int s) {
        if (i == n) return s == target ? 1 : 0;
        long long key = (long long)i * 100000 + (s + 50000);
        auto it = memo.find(key);
        if (it != memo.end()) return it->second;
        int ways = solve(i + 1, s + (*nums)[i]) + solve(i + 1, s - (*nums)[i]);
        return memo[key] = ways;
    }
public:
    int findTargetSumWays(vector<int>& nums, int target) {
        this->nums = &nums; this->target = target; n = nums.size();
        return solve(0, 0);
    }
};
```
```java
class Solution {
    private java.util.Map<String, Integer> memo = new java.util.HashMap<>();
    private int[] nums;
    private int target, n;
    private int solve(int i, int s) {
        if (i == n) return s == target ? 1 : 0;
        String key = i + "#" + s;
        if (memo.containsKey(key)) return memo.get(key);
        int ways = solve(i + 1, s + nums[i]) + solve(i + 1, s - nums[i]);
        memo.put(key, ways);
        return ways;
    }
    public int findTargetSumWays(int[] nums, int target) {
        this.nums = nums; this.target = target; n = nums.length;
        return solve(0, 0);
    }
}
```
```python
class Solution:
    def findTargetSumWays(self, nums: list[int], target: int) -> int:
        from functools import lru_cache
        n = len(nums)

        @lru_cache(maxsize=None)
        def solve(i: int, s: int) -> int:
            if i == n:
                return 1 if s == target else 0
            return solve(i + 1, s + nums[i]) + solve(i + 1, s - nums[i])

        return solve(0, 0)
```

### Complexity
- **Time**: O(n × sum) — distinct `(i, s)` states.
- **Space**: O(n × sum) for the memo.

### Verdict
Intuitive and direct. The transform below makes it a tidy 1D knapsack.

---

## Approach 2 — Subset-sum counting after transform (optimal) ⭐

### Intuition
Reduce to "count subsets summing to `P = (sum + target) / 2`," then run the standard 0/1 subset-sum count with a downward sweep.

### Algorithm
1. Compute `sum`. If `|target| > sum` or `(sum + target)` is odd → return 0.
2. `P = (sum + target) / 2`. `dp[0] = 1`.
3. For each `x`, for `v` from `P` down to `x`: `dp[v] += dp[v - x]`.
4. Return `dp[P]`.

### Dry run on `nums = [1,1,1,1,1], target = 3`
```
sum=5, P=(5+3)/2=4
dp[0]=1
each '1' adds shifted copies; after all five, dp[4] = C(5,4) = 5
answer = 5
```

### Code
```cpp
class Solution {
public:
    int findTargetSumWays(vector<int>& nums, int target) {
        int sum = accumulate(nums.begin(), nums.end(), 0);
        if (abs(target) > sum || (sum + target) % 2) return 0;
        int P = (sum + target) / 2;
        vector<int> dp(P + 1, 0);
        dp[0] = 1;
        for (int x : nums)
            for (int v = P; v >= x; v--)
                dp[v] += dp[v - x];
        return dp[P];
    }
};
```
```java
class Solution {
    public int findTargetSumWays(int[] nums, int target) {
        int sum = 0;
        for (int x : nums) sum += x;
        if (Math.abs(target) > sum || ((sum + target) & 1) == 1) return 0;
        int P = (sum + target) / 2;
        int[] dp = new int[P + 1];
        dp[0] = 1;
        for (int x : nums)
            for (int v = P; v >= x; v--)
                dp[v] += dp[v - x];
        return dp[P];
    }
}
```
```python
class Solution:
    def findTargetSumWays(self, nums: list[int], target: int) -> int:
        total = sum(nums)
        if abs(target) > total or (total + target) % 2:
            return 0
        P = (total + target) // 2
        dp = [0] * (P + 1)
        dp[0] = 1
        for x in nums:
            for v in range(P, x - 1, -1):
                dp[v] += dp[v - x]
        return dp[P]
```

### Complexity
- **Time**: O(n × P) ≤ O(n × sum).
- **Space**: O(sum).

### Verdict
**The optimal answer.** The sign-to-subset transform is the key insight; the rest is a textbook 0/1 knapsack count.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Memoization (direct ±) | O(n·sum) | O(n·sum) | intuitive, no math trick |
| Subset-sum after transform | O(n·sum) | **O(sum)** | the answer ⭐ |

---

## 🧪 Edge cases & pitfalls
- **Zeros in `nums`** (`[1,0]`, target 1) → each `0` can take `+` or `-` freely, doubling counts. The DP handles this naturally: a `0` contributes `dp[v] += dp[v]`, doubling reachable counts. (Don't special-case it away.)
- **`|target| > sum`** → 0 (unreachable).
- **`sum + target` odd** → 0 (`P` non-integer).
- **Pitfall — sweep direction**: `v` must go **downward** (0/1 — each number used once with one sign). Upward would reuse numbers.
- **Pitfall — negative `P`**: the guards ensure `P >= 0`; `target` could be negative but `sum + target >= 0` is checked via `|target| <= sum`.

---

## 🔗 Related problems
- **Partition Equal Subset Sum** (LC 416) — subset-sum decision; the same downward-sweep knapsack.
- **Coin Change II** (LC 518) — counting combinations (unbounded, upward sweep).
- **Last Stone Weight II** (LC 1049) — minimize the difference of two signed groups.
- **Ones and Zeroes** (LC 474) — 2D-capacity 0/1 knapsack.

---

**→ Next:** [`06-Maximal-Square.md`](./06-Maximal-Square.md) | **→ Prev:** [`04-Coin-Change-II.md`](./04-Coin-Change-II.md) | Back to [`00-Index.md`](./00-Index.md)
