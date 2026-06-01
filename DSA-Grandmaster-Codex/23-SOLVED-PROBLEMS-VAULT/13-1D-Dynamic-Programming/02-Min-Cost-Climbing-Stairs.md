# Min Cost Climbing Stairs

**Platform**: LeetCode 746 · **Difficulty**: Easy · **Topics**: Array, Dynamic Programming · **Pattern**: Linear recurrence with cost minimization

---

## 📜 Problem Statement

You are given an integer array `cost` where `cost[i]` is the cost of `i`-th step on a staircase. Once you pay the cost, you can either climb **one** or **two** steps.

You can either start from the step with index `0`, or the step with index `1`.

Return the **minimum cost** to reach the **top** of the floor (the position just past the last index).

### Examples

**Example 1:**
```
Input:  cost = [10, 15, 20]
Output: 15
Explanation: You will start at index 1.
- Pay 15 and climb two steps to reach the top.
The total cost is 15.
```

**Example 2:**
```
Input:  cost = [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]
Output: 6
Explanation: You will start at index 0.
- Pay 1, climb two steps to reach index 2.
- Pay 1, climb two steps to reach index 4.
- Pay 1, climb two steps to reach index 6.
- Pay 1, climb one step to reach index 7.
- Pay 1, climb two steps to reach index 9.
- Pay 1, climb one step to reach the top.
The total cost is 6.
```

**Example 3:**
```
Input:  cost = [0, 0, 0, 1]
Output: 0
Explanation: Start at index 0, hop 0 -> 2 (free), then 2 -> top (free). Total 0.
```

### Constraints
```
2 <= cost.length <= 1000
0 <= cost[i] <= 999
```

---

## 🧠 Understanding the problem

The "top" is the position **one past the last index** (index `n`). You pay a step's cost only when you *stand on it and launch* from it. So the cost of standing at the top is 0 — you never pay there.

To arrive at position `i`, you must have launched from `i-1` (paying `cost[i-1]`) or from `i-2` (paying `cost[i-2]`). You take the cheaper of those two arrivals.

5-step framework:
1. **State**: `dp[i]` = minimum cost to *reach* position `i`.
2. **Transition**: `dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])`.
3. **Base case**: `dp[0] = dp[1] = 0` (free to start at either index 0 or 1).
4. **Order**: `i` from `2` to `n`.
5. **Answer**: `dp[n]`; depends only on the last two entries → O(1) space.

---

## Approach 1 — Top-down memoization

### Intuition
Define `solve(i)` = min cost to reach position `i`. Recurse on the two predecessors, cache results.

### Algorithm
1. Base: `solve(0) = solve(1) = 0`.
2. `solve(i) = min(solve(i-1) + cost[i-1], solve(i-2) + cost[i-2])`.
3. Memoize on `i`. Answer is `solve(n)`.

### Dry run on `cost = [10, 15, 20]` (n = 3)
```
solve(3) = min(solve(2)+cost[2], solve(1)+cost[1])
solve(2) = min(solve(1)+cost[1], solve(0)+cost[0]) = min(0+15, 0+10) = 10
solve(3) = min(10+20, 0+15) = min(30, 15) = 15
```

### Code
```cpp
class Solution {
    vector<int> memo;
    vector<int>* c;
    int solve(int i) {
        if (i <= 1) return 0;
        if (memo[i] != -1) return memo[i];
        return memo[i] = min(solve(i - 1) + (*c)[i - 1],
                             solve(i - 2) + (*c)[i - 2]);
    }
public:
    int minCostClimbingStairs(vector<int>& cost) {
        int n = cost.size();
        memo.assign(n + 1, -1);
        c = &cost;
        return solve(n);
    }
};
```
```java
class Solution {
    private int[] memo;
    private int[] cost;
    private int solve(int i) {
        if (i <= 1) return 0;
        if (memo[i] != -1) return memo[i];
        return memo[i] = Math.min(solve(i - 1) + cost[i - 1],
                                  solve(i - 2) + cost[i - 2]);
    }
    public int minCostClimbingStairs(int[] cost) {
        this.cost = cost;
        memo = new int[cost.length + 1];
        java.util.Arrays.fill(memo, -1);
        return solve(cost.length);
    }
}
```
```python
class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        from functools import lru_cache
        n = len(cost)

        @lru_cache(maxsize=None)
        def solve(i: int) -> int:
            if i <= 1:
                return 0
            return min(solve(i - 1) + cost[i - 1],
                       solve(i - 2) + cost[i - 2])

        return solve(n)
```

### Complexity
- **Time**: O(n) — each state once.
- **Space**: O(n) memo + recursion stack.

### Verdict
Straightforward top-down. Good for explaining the transition; now flip it bottom-up.

---

## Approach 2 — Bottom-up tabulation

### Intuition
Fill `dp` from the base cases upward. No recursion.

### Algorithm
1. `dp[0] = dp[1] = 0`.
2. For `i` from `2` to `n`: `dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])`.
3. Return `dp[n]`.

### Dry run on `cost = [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]`
```
dp[0]=0, dp[1]=0
dp[2]=min(0+100, 0+1)=1
dp[3]=min(1+1, 0+100)=2
dp[4]=min(2+1, 1+1)=2
dp[5]=min(2+1, 2+1)=3
dp[6]=min(3+100,2+1)=3
... dp[10]=6
```

### Code
```cpp
class Solution {
public:
    int minCostClimbingStairs(vector<int>& cost) {
        int n = cost.size();
        vector<int> dp(n + 1, 0);
        for (int i = 2; i <= n; i++)
            dp[i] = min(dp[i - 1] + cost[i - 1],
                        dp[i - 2] + cost[i - 2]);
        return dp[n];
    }
};
```
```java
class Solution {
    public int minCostClimbingStairs(int[] cost) {
        int n = cost.length;
        int[] dp = new int[n + 1];
        for (int i = 2; i <= n; i++)
            dp[i] = Math.min(dp[i - 1] + cost[i - 1],
                             dp[i - 2] + cost[i - 2]);
        return dp[n];
    }
}
```
```python
class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        n = len(cost)
        dp = [0] * (n + 1)
        for i in range(2, n + 1):
            dp[i] = min(dp[i - 1] + cost[i - 1],
                        dp[i - 2] + cost[i - 2])
        return dp[n]
```

### Complexity
- **Time**: O(n).
- **Space**: O(n).

### Verdict
Clean and stack-free. Still keeps a full array we don't need.

---

## Approach 3 — Space-optimized rolling variables (optimal) ⭐

### Intuition
`dp[i]` needs only `dp[i-1]` and `dp[i-2]`. Track those two scalars.

### Algorithm
1. `a = 0` (= dp[i-2]), `b = 0` (= dp[i-1]).
2. For `i` from `2` to `n`: `cur = min(b + cost[i-1], a + cost[i-2])`; shift `a = b`, `b = cur`.
3. Return `b`.

### Dry run on `cost = [10, 15, 20]`
```
a=0, b=0
i=2: cur=min(0+15, 0+10)=10 -> a=0, b=10
i=3: cur=min(10+20, 0+15)=15 -> a=10, b=15
return 15
```

### Code
```cpp
class Solution {
public:
    int minCostClimbingStairs(vector<int>& cost) {
        int n = cost.size();
        int a = 0, b = 0;          // dp[i-2], dp[i-1]
        for (int i = 2; i <= n; i++) {
            int cur = min(b + cost[i - 1], a + cost[i - 2]);
            a = b;
            b = cur;
        }
        return b;
    }
};
```
```java
class Solution {
    public int minCostClimbingStairs(int[] cost) {
        int n = cost.length;
        int a = 0, b = 0;          // dp[i-2], dp[i-1]
        for (int i = 2; i <= n; i++) {
            int cur = Math.min(b + cost[i - 1], a + cost[i - 2]);
            a = b;
            b = cur;
        }
        return b;
    }
}
```
```python
class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        a = b = 0                  # dp[i-2], dp[i-1]
        for i in range(2, len(cost) + 1):
            a, b = b, min(b + cost[i - 1], a + cost[i - 2])
        return b
```

### Complexity
- **Time**: O(n).
- **Space**: O(1).

### Verdict
**The optimal answer.** Linear time, constant space.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Memoization | O(n) | O(n) | top-down, easy to reason about |
| Tabulation | O(n) | O(n) | bottom-up, no recursion |
| Rolling variables | **O(n)** | **O(1)** | the answer ⭐ |

---

## 🧪 Edge cases & pitfalls
- **Pitfall — what is "the top"?** It's index `n`, *not* `n-1`. The most common mistake is returning `min(dp[n-1], dp[n-2])` style logic that stops at the last step. Treat `n` as a real (free) destination.
- **Pitfall — paying for the top**: you never pay `cost` at the top, only at the steps you launch from. The base cases `dp[0]=dp[1]=0` encode "starting is free."
- **All zeros** (`[0,0,0]`) → 0.
- **Two elements** (`cost = [a, b]`) → 0, because you can start at index 1 and step directly to the top, or start at index 0 and double-step over. Either way the loop yields `min(b, a)`... wait — actually for `n=2`, `dp[2]=min(dp[1]+cost[1], dp[0]+cost[0]) = min(cost[1], cost[0])`. The minimum of the two costs.

---

## 🔗 Related problems
- **Climbing Stairs** (LC 70) — the same step structure, counting instead of minimizing.
- **House Robber** (LC 198) — `dp[i-1]` vs `dp[i-2]` shape, maximizing non-adjacent picks.
- **Minimum Path Sum** (LC 64) — 2D cost-minimization grid version.
- **Jump Game II** (LC 45) — reach the end with minimum jumps (greedy/BFS flavor).

---

**→ Next:** [`03-House-Robber.md`](./03-House-Robber.md) | **→ Prev:** [`01-Climbing-Stairs.md`](./01-Climbing-Stairs.md) | Back to [`00-Index.md`](./00-Index.md)
