# Coin Change II

**Platform**: LeetCode 518 · **Difficulty**: Medium · **Topics**: Array, Dynamic Programming · **Pattern**: Unbounded knapsack — counting combinations

---

## 📜 Problem Statement

You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.

Return the **number of combinations** that make up that amount. If that amount of money cannot be made up by any combination of the coins, return `0`.

You may assume that you have an **infinite** number of each kind of coin.

The answer is **guaranteed to fit** into a signed 32-bit integer.

### Examples

**Example 1:**
```
Input:  amount = 5, coins = [1, 2, 5]
Output: 4
Explanation: there are four ways to make up the amount:
5 = 5
5 = 2 + 2 + 1
5 = 2 + 1 + 1 + 1
5 = 1 + 1 + 1 + 1 + 1
```

**Example 2:**
```
Input:  amount = 3, coins = [2]
Output: 0
Explanation: the amount of 3 cannot be made up just with coins of 2.
```

**Example 3:**
```
Input:  amount = 10, coins = [10]
Output: 1
```

### Constraints
```
1 <= coins.length <= 300
1 <= coins[i] <= 5000
All the values of coins are unique.
0 <= amount <= 5000
```

---

## 🧠 Understanding the problem

We count **combinations** (sets of coin counts), not **permutations** (ordered sequences). `2 + 1 + 1` and `1 + 2 + 1` are the **same** combination and must be counted once.

The standard min-coins problem ([Coin Change](../13-1D-Dynamic-Programming/08-Coin-Change.md)) doesn't care about ordering, but here ordering is exactly the trap. The fix is the **loop order**:

> Put the **coins loop on the outside** and the **amount loop on the inside**. This processes coins one at a time, so each combination is counted in a single canonical order (coins introduced in array order) — never as a reordering.

If you swapped the loops (amount outside, coins inside), you'd count permutations — that's a different problem ([Combination Sum IV](https://leetcode.com/problems/combination-sum-iv/)).

5-step framework:
1. **State**: `dp[i][a]` = number of combinations making amount `a` using the first `i` coin types.
2. **Transition**: `dp[i][a] = dp[i-1][a]` (don't use coin i) `+ dp[i][a - coin]` (use coin i, still allowed to reuse it).
3. **Base case**: `dp[*][0] = 1` (one way to make 0 — pick nothing).
4. **Order**: coins outer, amount inner ascending.
5. **Answer**: `dp[n][amount]`; collapses to a 1D array.

---

## Approach 1 — 2D table (coins × amount)

### Intuition
`dp[i][a]`: with the first `i` coins, count combinations for amount `a`. Either skip coin `i` entirely, or use at least one copy of it (which keeps it available, hence `dp[i][a-coin]`, same row).

### Algorithm
1. `dp[i][0] = 1` for all `i`.
2. For each coin `i` (1..n), for `a` 0..amount: `dp[i][a] = dp[i-1][a] + (a >= coin ? dp[i][a-coin] : 0)`.
3. Return `dp[n][amount]`.

### Dry run on `coins = [1,2,5], amount = 5`
```
after coin 1: dp[*]=1 for every amount (all ones)
after coin 2: amounts gain 2-combinations -> dp[5]=3
after coin 5: dp[5] += dp[0]=1 -> 4
answer = 4
```

### Code
```cpp
class Solution {
public:
    int change(int amount, vector<int>& coins) {
        int n = coins.size();
        vector<vector<int>> dp(n + 1, vector<int>(amount + 1, 0));
        for (int i = 0; i <= n; i++) dp[i][0] = 1;
        for (int i = 1; i <= n; i++)
            for (int a = 1; a <= amount; a++) {
                dp[i][a] = dp[i - 1][a];
                if (a >= coins[i - 1]) dp[i][a] += dp[i][a - coins[i - 1]];
            }
        return dp[n][amount];
    }
};
```
```java
class Solution {
    public int change(int amount, int[] coins) {
        int n = coins.length;
        int[][] dp = new int[n + 1][amount + 1];
        for (int i = 0; i <= n; i++) dp[i][0] = 1;
        for (int i = 1; i <= n; i++)
            for (int a = 1; a <= amount; a++) {
                dp[i][a] = dp[i - 1][a];
                if (a >= coins[i - 1]) dp[i][a] += dp[i][a - coins[i - 1]];
            }
        return dp[n][amount];
    }
}
```
```python
class Solution:
    def change(self, amount: int, coins: list[int]) -> int:
        n = len(coins)
        dp = [[0] * (amount + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            dp[i][0] = 1
        for i in range(1, n + 1):
            for a in range(1, amount + 1):
                dp[i][a] = dp[i - 1][a]
                if a >= coins[i - 1]:
                    dp[i][a] += dp[i][a - coins[i - 1]]
        return dp[n][amount]
```

### Complexity
- **Time**: O(n × amount).
- **Space**: O(n × amount).

### Verdict
Explicit and makes the "skip vs use" decision visible. Each row reads its own row (left) and the previous row, so it collapses.

---

## Approach 2 — 1D rolling array (optimal) ⭐

### Intuition
Drop the coin index. Process coins one at a time; for each, sweep `a` **upward** so `dp[a - coin]` already includes the current coin (allowing reuse → unbounded). Because coins are handled in a fixed outer order, only combinations are counted.

### Algorithm
1. `dp[0] = 1`.
2. For each coin `c`, for `a` from `c` to amount: `dp[a] += dp[a - c]`.
3. Return `dp[amount]`.

### Dry run on `coins = [1,2,5], amount = 5`
```
dp=[1,0,0,0,0,0]
coin1: dp=[1,1,1,1,1,1]
coin2: dp[2]+=dp[0]=2 ... dp=[1,1,2,2,3,3]
coin5: dp[5]+=dp[0]=4 -> dp[5]=4
answer = 4
```

### Code
```cpp
class Solution {
public:
    int change(int amount, vector<int>& coins) {
        vector<int> dp(amount + 1, 0);
        dp[0] = 1;
        for (int c : coins)
            for (int a = c; a <= amount; a++)
                dp[a] += dp[a - c];
        return dp[amount];
    }
};
```
```java
class Solution {
    public int change(int amount, int[] coins) {
        int[] dp = new int[amount + 1];
        dp[0] = 1;
        for (int c : coins)
            for (int a = c; a <= amount; a++)
                dp[a] += dp[a - c];
        return dp[amount];
    }
}
```
```python
class Solution:
    def change(self, amount: int, coins: list[int]) -> int:
        dp = [0] * (amount + 1)
        dp[0] = 1
        for c in coins:
            for a in range(c, amount + 1):
                dp[a] += dp[a - c]
        return dp[amount]
```

### Complexity
- **Time**: O(n × amount).
- **Space**: O(amount).

### Verdict
**The optimal answer.** Tiny and fast. The loop nesting (coins outer, amount inner, upward) is the entire trick.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| 2D table | O(n·amount) | O(n·amount) | explicit skip/use |
| 1D rolling array | O(n·amount) | **O(amount)** | the answer ⭐ |

> **Contrast with the sweep direction**: here we sweep `a` **upward** (unbounded — a coin can be reused). In [Partition Equal Subset Sum](../13-1D-Dynamic-Programming/12-Partition-Equal-Subset-Sum.md) we sweep **downward** (0/1 — each item once). Same array, opposite direction, different semantics.

---

## 🧪 Edge cases & pitfalls
- **`amount = 0`** → 1 (the empty combination). `dp[0] = 1` encodes it.
- **Unreachable** (`amount = 3, coins = [2]`) → 0.
- **Pitfall — loop order**: amount outer + coins inner counts **permutations**, giving a larger, wrong answer. Coins must be outer here.
- **Pitfall — downward sweep**: sweeping `a` from high to low would forbid reuse, turning this into a 0/1 "each coin once" count — also wrong for this problem.
- **Pitfall — `dp[0]` not set**: forgetting the base case yields all zeros.

---

## 🔗 Related problems
- **Coin Change** (LC 322) — minimize the number of coins (order doesn't matter there either).
- **Combination Sum IV** (LC 377) — count *ordered* sequences (swap the loops).
- **Partition Equal Subset Sum** (LC 416) — 0/1 subset-sum (downward sweep).
- **Target Sum** (LC 494) — subset-sum counting via a sign transformation.

---

**→ Next:** [`05-Target-Sum.md`](./05-Target-Sum.md) | **→ Prev:** [`03-Edit-Distance.md`](./03-Edit-Distance.md) | Back to [`00-Index.md`](./00-Index.md)
