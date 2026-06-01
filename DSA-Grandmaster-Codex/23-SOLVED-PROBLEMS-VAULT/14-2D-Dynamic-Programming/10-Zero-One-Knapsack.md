# 0/1 Knapsack (Classic)

**Platform**: Classic problem (GfG / CSES / textbook) · **Difficulty**: Medium · **Topics**: Array, Dynamic Programming · **Pattern**: Item × capacity DP (each item used at most once)

---

## 📜 Problem Statement

You are given `n` items. Item `i` has weight `weight[i]` and value `value[i]`. You also have a knapsack that can carry at most `W` total weight.

Select a subset of items so that their total weight does not exceed `W` and their total value is **maximized**. Each item may be taken **at most once** (this is the "0/1" — take it or leave it).

Return the maximum total value achievable.

> This is the canonical foundation behind LeetCode problems like Partition Equal Subset Sum (416), Target Sum (494), Ones and Zeroes (474), and Last Stone Weight II (1049). The signature below mirrors the standard GeeksforGeeks / competitive form.

### Examples

**Example 1:**
```
Input:  W = 4, weight = [1, 3, 4, 5], value = [1, 4, 5, 7]
Output: 5
Explanation: Items {weight 1, value 1} and {weight 3, value 4} together weigh 4 (<= W)
for value 1 + 4 = 5. Item {weight 4, value 5} alone also gives 5. No subset within
capacity 4 beats 5.
```

**Example 2:**
```
Input:  W = 3, weight = [4, 5, 1], value = [1, 2, 3]
Output: 3
Explanation: Only the item of weight 1 fits within capacity 3; its value is 3.
```

**Example 3:**
```
Input:  W = 10, weight = [2, 3, 5, 7], value = [1, 5, 2, 4]
Output: 9
Explanation: Items of weight 3 (value 5) and weight 7 (value 4) weigh 10 (<= W)
for value 5 + 4 = 9, which is the maximum.
```

### Constraints
```
1 <= n <= 1000
1 <= W <= 1000
1 <= weight[i], value[i] <= 1000
```

---

## 🧠 Understanding the problem

For each item there's a binary decision: **include it** or **exclude it**. If we include item `i` (only possible when `weight[i] <= capacity`), we gain `value[i]` and the remaining capacity drops by `weight[i]`. If we exclude it, capacity is unchanged. We want the best over all subsets respecting the capacity.

The two dimensions of the state are **which items we've considered** and **how much capacity remains** — the prototypical 2D "item × capacity" DP.

Greedy by value, by weight, or by value/weight ratio all fail for 0/1 (ratio-greedy is only optimal for the *fractional* knapsack). DP is required.

5-step framework:
1. **State**: `dp[i][c]` = max value using the first `i` items with capacity `c`.
2. **Transition**: `dp[i][c] = max(dp[i-1][c], dp[i-1][c - weight[i-1]] + value[i-1])` (skip vs take).
3. **Base case**: `dp[0][c] = 0` (no items → no value).
4. **Order**: items outer, capacity inner. For the 1D version, sweep capacity **downward**.
5. **Answer**: `dp[n][W]`.

---

## Approach 1 — Top-down memoization

### Intuition
`solve(i, c)` = best value choosing among items `i..n-1` with capacity `c`. Try skipping item `i`, and (if it fits) taking it.

### Algorithm
1. If `i == n` or `c == 0`, return 0.
2. `best = solve(i+1, c)` (skip).
3. If `weight[i] <= c`: `best = max(best, value[i] + solve(i+1, c - weight[i]))`.
4. Memoize on `(i, c)`.

### Dry run on `W=4, weight=[1,3,4,5], value=[1,4,5,7]`
```
solve(0,4): skip->solve(1,4); take item0 -> 1 + solve(1,3)
solve(1,3): take item1(w3) -> 4 + solve(2,0)=4
so take0+take1 = 1+4 = 5 ; item2(w4) alone also 5
answer = 5
```

### Code
```cpp
class Solution {
    vector<vector<int>> memo;
    vector<int> w, v;
    int n;
    int solve(int i, int c) {
        if (i == n || c == 0) return 0;
        if (memo[i][c] != -1) return memo[i][c];
        int best = solve(i + 1, c);
        if (w[i] <= c) best = max(best, v[i] + solve(i + 1, c - w[i]));
        return memo[i][c] = best;
    }
public:
    int knapsack(int W, vector<int>& weight, vector<int>& value) {
        w = weight; v = value; n = weight.size();
        memo.assign(n, vector<int>(W + 1, -1));
        return solve(0, W);
    }
};
```
```java
class Solution {
    private int[][] memo;
    private int[] w, v;
    private int n;
    private int solve(int i, int c) {
        if (i == n || c == 0) return 0;
        if (memo[i][c] != -1) return memo[i][c];
        int best = solve(i + 1, c);
        if (w[i] <= c) best = Math.max(best, v[i] + solve(i + 1, c - w[i]));
        return memo[i][c] = best;
    }
    public int knapsack(int W, int[] weight, int[] value) {
        w = weight; v = value; n = weight.length;
        memo = new int[n][W + 1];
        for (int[] row : memo) java.util.Arrays.fill(row, -1);
        return solve(0, W);
    }
}
```
```python
class Solution:
    def knapsack(self, W: int, weight: list[int], value: list[int]) -> int:
        from functools import lru_cache
        n = len(weight)

        @lru_cache(maxsize=None)
        def solve(i: int, c: int) -> int:
            if i == n or c == 0:
                return 0
            best = solve(i + 1, c)
            if weight[i] <= c:
                best = max(best, value[i] + solve(i + 1, c - weight[i]))
            return best

        return solve(0, W)
```

### Complexity
- **Time**: O(n × W).
- **Space**: O(n × W) memo + recursion.

### Verdict
The recurrence in its purest form. Bottom-up next.

---

## Approach 2 — Bottom-up 2D table

### Intuition
`dp[i][c]` over items × capacity. Each item either isn't taken (inherit `dp[i-1][c]`) or is taken if it fits (`dp[i-1][c - w] + v`).

### Algorithm
1. `dp[0][*] = 0`.
2. For `i` 1..n, `c` 0..W: `dp[i][c] = dp[i-1][c]`; if `weight[i-1] <= c`, `dp[i][c] = max(dp[i][c], dp[i-1][c - weight[i-1]] + value[i-1])`.
3. Return `dp[n][W]`.

### Dry run (final cell)
```
dp[4][4] = best over taking/skipping all 4 items at capacity 4 = 5
```

### Code
```cpp
class Solution {
public:
    int knapsack(int W, vector<int>& weight, vector<int>& value) {
        int n = weight.size();
        vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));
        for (int i = 1; i <= n; i++)
            for (int c = 0; c <= W; c++) {
                dp[i][c] = dp[i - 1][c];
                if (weight[i - 1] <= c)
                    dp[i][c] = max(dp[i][c], dp[i - 1][c - weight[i - 1]] + value[i - 1]);
            }
        return dp[n][W];
    }
};
```
```java
class Solution {
    public int knapsack(int W, int[] weight, int[] value) {
        int n = weight.length;
        int[][] dp = new int[n + 1][W + 1];
        for (int i = 1; i <= n; i++)
            for (int c = 0; c <= W; c++) {
                dp[i][c] = dp[i - 1][c];
                if (weight[i - 1] <= c)
                    dp[i][c] = Math.max(dp[i][c], dp[i - 1][c - weight[i - 1]] + value[i - 1]);
            }
        return dp[n][W];
    }
}
```
```python
class Solution:
    def knapsack(self, W: int, weight: list[int], value: list[int]) -> int:
        n = len(weight)
        dp = [[0] * (W + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for c in range(W + 1):
                dp[i][c] = dp[i - 1][c]
                if weight[i - 1] <= c:
                    dp[i][c] = max(dp[i][c],
                                   dp[i - 1][c - weight[i - 1]] + value[i - 1])
        return dp[n][W]
```

### Complexity
- **Time**: O(n × W).
- **Space**: O(n × W).

### Verdict
The standard table. Row `i` reads only row `i-1`, so it collapses to 1D.

---

## Approach 3 — 1D rolling array (space optimized) ⭐

### Intuition
Keep one array `dp[c]`. For each item, sweep capacity from `W` **down to** `weight[i]`. The downward sweep guarantees `dp[c - weight]` still reflects the state *without* this item — enforcing "use each item at most once" (0/1). Sweeping upward would allow reuse (that's the *unbounded* knapsack).

### Algorithm
1. `dp[0..W] = 0`.
2. For each item `i`, for `c` from `W` down to `weight[i]`: `dp[c] = max(dp[c], dp[c - weight[i]] + value[i])`.
3. Return `dp[W]`.

### Dry run on `W=4, weight=[1,3,4,5], value=[1,4,5,7]`
```
item(1,1): dp[1..4] -> [0,1,1,1,1]
item(3,4): c=4 dp[4]=max(1,dp[1]+4=5)=5; c=3 dp[3]=max(1,dp[0]+4=4)=4
           dp=[0,1,1,4,5]
item(4,5): c=4 dp[4]=max(5,dp[0]+5=5)=5
item(5,7): w>W, skip
answer dp[4]=5
```

### Code
```cpp
class Solution {
public:
    int knapsack(int W, vector<int>& weight, vector<int>& value) {
        int n = weight.size();
        vector<int> dp(W + 1, 0);
        for (int i = 0; i < n; i++)
            for (int c = W; c >= weight[i]; c--)
                dp[c] = max(dp[c], dp[c - weight[i]] + value[i]);
        return dp[W];
    }
};
```
```java
class Solution {
    public int knapsack(int W, int[] weight, int[] value) {
        int n = weight.length;
        int[] dp = new int[W + 1];
        for (int i = 0; i < n; i++)
            for (int c = W; c >= weight[i]; c--)
                dp[c] = Math.max(dp[c], dp[c - weight[i]] + value[i]);
        return dp[W];
    }
}
```
```python
class Solution:
    def knapsack(self, W: int, weight: list[int], value: list[int]) -> int:
        n = len(weight)
        dp = [0] * (W + 1)
        for i in range(n):
            for c in range(W, weight[i] - 1, -1):
                dp[c] = max(dp[c], dp[c - weight[i]] + value[i])
        return dp[W]
```

### Complexity
- **Time**: O(n × W).
- **Space**: O(W).

### Verdict
**The optimal answer.** The downward sweep is the single most important detail in all of knapsack DP — it is exactly what distinguishes 0/1 (each item once) from unbounded (reuse allowed).

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Memoization | O(nW) | O(nW) | top-down take/skip |
| 2D table | O(nW) | O(nW) | canonical, supports item reconstruction |
| 1D rolling array | O(nW) | **O(W)** | the answer ⭐ |

### 0/1 vs Unbounded — the sweep direction

| Variant | Inner loop | Meaning |
|---------|-----------|---------|
| 0/1 knapsack | `c` from `W` down to `weight[i]` | each item at most once |
| Unbounded knapsack | `c` from `weight[i]` up to `W` | each item reusable |

This is the same distinction as [Partition Equal Subset Sum](../13-1D-Dynamic-Programming/12-Partition-Equal-Subset-Sum.md) (downward) vs [Coin Change II](./04-Coin-Change-II.md) (upward).

---

## 🧪 Edge cases & pitfalls
- **No item fits** (all weights > W) → 0.
- **Capacity 0** → 0.
- **Pitfall — upward sweep in 1D**: iterating `c` ascending lets one item be picked multiple times, silently solving the wrong (unbounded) problem.
- **Pitfall — greedy by ratio**: optimal only for *fractional* knapsack, not 0/1. Always DP here.
- **Pitfall — huge W**: this DP is *pseudo-polynomial* (O(nW)). If `W` were up to 10⁹ with small `n`, you'd switch to a meet-in-the-middle or value-indexed DP instead.

---

## 🔗 Related problems
- **Partition Equal Subset Sum** (LC 416) — 0/1 subset-sum decision (downward sweep).
- **Target Sum** (LC 494) — subset-sum counting via sign transform.
- **Ones and Zeroes** (LC 474) — 0/1 knapsack with *two* capacity dimensions.
- **Coin Change II** (LC 518) — unbounded knapsack counting (upward sweep).
- **Last Stone Weight II** (LC 1049) — minimize difference of two subset sums.

---

**→ Next:** [`11-Distinct-Subsequences.md`](./11-Distinct-Subsequences.md) | **→ Prev:** [`09-Best-Time-Buy-Sell-Cooldown.md`](./09-Best-Time-Buy-Sell-Cooldown.md) | Back to [`00-Index.md`](./00-Index.md)
