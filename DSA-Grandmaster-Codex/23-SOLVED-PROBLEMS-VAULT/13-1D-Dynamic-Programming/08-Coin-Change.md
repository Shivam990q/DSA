# Coin Change

**Platform**: LeetCode 322 · **Difficulty**: Medium · **Topics**: Array, Dynamic Programming, BFS · **Pattern**: Unbounded knapsack (min coins to reach a target)

---

## 📜 Problem Statement

You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.

Return the **fewest number of coins** that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return `-1`.

You may assume that you have an **infinite** number of each kind of coin.

### Examples

**Example 1:**
```
Input:  coins = [1, 2, 5], amount = 11
Output: 3
Explanation: 11 = 5 + 5 + 1.
```

**Example 2:**
```
Input:  coins = [2], amount = 3
Output: -1
Explanation: 3 cannot be formed with only coins of value 2.
```

**Example 3:**
```
Input:  coins = [1], amount = 0
Output: 0
Explanation: Making amount 0 needs no coins.
```

### Constraints
```
1 <= coins.length <= 12
1 <= coins[i] <= 2^31 - 1
0 <= amount <= 10^4
```

---

## 🧠 Understanding the problem

We want the **minimum count** of coins summing to `amount`, with unlimited reuse of each denomination. The crucial observation: to make amount `a`, the *last* coin used is some `c <= a`, leaving the subproblem of making `a - c` optimally. So:

> `minCoins(a) = 1 + min over coins c of minCoins(a - c)`.

This is an **unbounded knapsack** (each coin reusable). Greedy ("always take the largest coin") fails for general denominations — e.g. `coins = [1, 3, 4], amount = 6`: greedy gives `4+1+1 = 3`, but `3+3 = 2` is optimal.

5-step framework:
1. **State**: `dp[a]` = fewest coins to make amount `a`.
2. **Transition**: `dp[a] = min(dp[a - c] + 1)` over all coins `c <= a`.
3. **Base case**: `dp[0] = 0`.
4. **Order**: `a` from `1` to `amount` (so `dp[a-c]` is ready).
5. **Answer**: `dp[amount]`, or `-1` if it's still "infinity".

---

## Approach 1 — Top-down memoization

### Intuition
Recurse on the remaining amount, trying each coin as the last one, and cache the best per amount.

### Algorithm
1. `solve(0) = 0`. `solve(a < 0) = +∞` (impossible).
2. `solve(a) = 1 + min(solve(a - c))` over all coins.
3. Memoize on `a`. Convert `+∞` to `-1` at the top.

### Dry run on `coins = [1,2,5], amount = 11`
```
solve(11) tries 1->solve(10), 2->solve(9), 5->solve(6)
... eventually solve(6)=2 (5+1), solve(9)=3, solve(10)=2 (5+5)
solve(11) = 1 + min(solve(10)=2, solve(9)=3, solve(6)=2) = 3
```

### Code
```cpp
class Solution {
    vector<int> memo;
    int solve(vector<int>& coins, int a) {
        if (a == 0) return 0;
        if (a < 0) return INT_MAX;
        if (memo[a] != -2) return memo[a];
        int best = INT_MAX;
        for (int c : coins) {
            int sub = solve(coins, a - c);
            if (sub != INT_MAX) best = min(best, sub + 1);
        }
        return memo[a] = best;
    }
public:
    int coinChange(vector<int>& coins, int amount) {
        memo.assign(amount + 1, -2);
        int res = solve(coins, amount);
        return res == INT_MAX ? -1 : res;
    }
};
```
```java
class Solution {
    private int[] memo;
    private int solve(int[] coins, int a) {
        if (a == 0) return 0;
        if (a < 0) return Integer.MAX_VALUE;
        if (memo[a] != -2) return memo[a];
        int best = Integer.MAX_VALUE;
        for (int c : coins) {
            int sub = solve(coins, a - c);
            if (sub != Integer.MAX_VALUE) best = Math.min(best, sub + 1);
        }
        return memo[a] = best;
    }
    public int coinChange(int[] coins, int amount) {
        memo = new int[amount + 1];
        java.util.Arrays.fill(memo, -2);
        int res = solve(coins, amount);
        return res == Integer.MAX_VALUE ? -1 : res;
    }
}
```
```python
class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        from functools import lru_cache
        INF = float('inf')

        @lru_cache(maxsize=None)
        def solve(a: int) -> float:
            if a == 0:
                return 0
            if a < 0:
                return INF
            best = INF
            for c in coins:
                best = min(best, solve(a - c) + 1)
            return best

        res = solve(amount)
        return -1 if res == INF else res
```

### Complexity
- **Time**: O(amount × coins).
- **Space**: O(amount) memo + recursion depth.

### Verdict
Direct translation of the recurrence. The bottom-up version is the standard answer.

---

## Approach 2 — Bottom-up tabulation (optimal) ⭐

### Intuition
Fill `dp[0..amount]`. Initialize every entry to a sentinel "infinity" (`amount + 1`, which is unreachable since the smallest coin is ≥ 1). For each amount, try every coin as the last one.

### Algorithm
1. `dp[0] = 0`; `dp[a] = amount + 1` for `a >= 1`.
2. For `a` from 1 to amount, for each coin `c <= a`: `dp[a] = min(dp[a], dp[a - c] + 1)`.
3. Return `dp[amount]` if `<= amount`, else `-1`.

### Dry run on `coins = [1,2,5], amount = 11`
```
dp[0]=0
dp[1]=1, dp[2]=1, dp[3]=2, dp[4]=2, dp[5]=1
dp[6]=2(5+1), dp[7]=2(5+2), dp[10]=2(5+5), dp[11]=3(5+5+1)
answer = 3
```

### Code
```cpp
class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        vector<int> dp(amount + 1, amount + 1);
        dp[0] = 0;
        for (int a = 1; a <= amount; a++)
            for (int c : coins)
                if (c <= a) dp[a] = min(dp[a], dp[a - c] + 1);
        return dp[amount] > amount ? -1 : dp[amount];
    }
};
```
```java
class Solution {
    public int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        java.util.Arrays.fill(dp, amount + 1);
        dp[0] = 0;
        for (int a = 1; a <= amount; a++)
            for (int c : coins)
                if (c <= a) dp[a] = Math.min(dp[a], dp[a - c] + 1);
        return dp[amount] > amount ? -1 : dp[amount];
    }
}
```
```python
class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        dp = [amount + 1] * (amount + 1)
        dp[0] = 0
        for a in range(1, amount + 1):
            for c in coins:
                if c <= a:
                    dp[a] = min(dp[a], dp[a - c] + 1)
        return dp[amount] if dp[amount] <= amount else -1
```

### Complexity
- **Time**: O(amount × coins).
- **Space**: O(amount).

### Verdict
**The optimal answer.** Iterative, no recursion, easy to reason about. The `amount + 1` sentinel cleanly encodes "unreachable."

---

## Approach 3 — BFS over amounts (alternative view)

### Intuition
Treat amounts as nodes; an edge `a → a - c` costs one coin. The fewest coins to reach `0` from `amount` is the **shortest path**, which BFS finds level by level. The first time we hit 0, the level number is the answer.

### Algorithm
1. BFS from `amount`. Level `k` = "used `k` coins."
2. From amount `a`, push `a - c` for each coin if non-negative and unvisited.
3. Return the level at which `0` is reached; if the queue empties first, return `-1`.

### Code
```cpp
class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        if (amount == 0) return 0;
        vector<bool> visited(amount + 1, false);
        queue<int> q;
        q.push(amount);
        visited[amount] = true;
        int level = 0;
        while (!q.empty()) {
            level++;
            int sz = q.size();
            while (sz--) {
                int a = q.front(); q.pop();
                for (int c : coins) {
                    int next = a - c;
                    if (next == 0) return level;
                    if (next > 0 && !visited[next]) {
                        visited[next] = true;
                        q.push(next);
                    }
                }
            }
        }
        return -1;
    }
};
```
```java
class Solution {
    public int coinChange(int[] coins, int amount) {
        if (amount == 0) return 0;
        boolean[] visited = new boolean[amount + 1];
        java.util.Queue<Integer> q = new java.util.ArrayDeque<>();
        q.add(amount);
        visited[amount] = true;
        int level = 0;
        while (!q.isEmpty()) {
            level++;
            int sz = q.size();
            while (sz-- > 0) {
                int a = q.poll();
                for (int c : coins) {
                    int next = a - c;
                    if (next == 0) return level;
                    if (next > 0 && !visited[next]) {
                        visited[next] = true;
                        q.add(next);
                    }
                }
            }
        }
        return -1;
    }
}
```
```python
class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        if amount == 0:
            return 0
        from collections import deque
        visited = [False] * (amount + 1)
        q = deque([amount])
        visited[amount] = True
        level = 0
        while q:
            level += 1
            for _ in range(len(q)):
                a = q.popleft()
                for c in coins:
                    nxt = a - c
                    if nxt == 0:
                        return level
                    if 0 < nxt <= amount and not visited[nxt]:
                        visited[nxt] = True
                        q.append(nxt)
        return -1
```

### Complexity
- **Time**: O(amount × coins).
- **Space**: O(amount).

### Verdict
Same complexity, sometimes faster in practice because BFS stops at the first time it reaches 0. A nice way to *see* "min coins = shortest path."

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Memoization | O(amount·coins) | O(amount) | top-down recurrence |
| Tabulation | O(amount·coins) | O(amount) | the standard answer ⭐ |
| BFS | O(amount·coins) | O(amount) | shortest-path view, early exit |

---

## 🧪 Edge cases & pitfalls
- **`amount = 0`** → 0 coins. `dp[0] = 0` handles it.
- **Unreachable** (`coins=[2], amount=3`) → `-1`. The sentinel stays above `amount`.
- **Pitfall — greedy**: taking the largest coin first is wrong for arbitrary denominations (`[1,3,4]`, amount 6). Always DP.
- **Pitfall — overflow in `dp[a-c] + 1`**: using `INT_MAX` as the sentinel and then `+1` overflows. Either use `amount + 1` as the sentinel (as in Approach 2) or guard the addition (as in Approach 1).
- **Pitfall — large coin values**: `coins[i]` can exceed `amount`; the `c <= a` guard skips them.

---

## 🔗 Related problems
- **Coin Change II** (LC 518) — count the number of combinations (not the minimum count).
- **Perfect Squares** (LC 279) — min count of squares summing to n; identical unbounded-knapsack shape.
- **Minimum Cost For Tickets** (LC 983) — DP over days with reuse.
- **Combination Sum IV** (LC 377) — count ordered combinations summing to a target.

---

**→ Next:** [`09-Maximum-Product-Subarray.md`](./09-Maximum-Product-Subarray.md) | **→ Prev:** [`07-Decode-Ways.md`](./07-Decode-Ways.md) | Back to [`00-Index.md`](./00-Index.md)
