# Best Time to Buy and Sell Stock with Cooldown

**Platform**: LeetCode 309 · **Difficulty**: Medium · **Topics**: Array, Dynamic Programming · **Pattern**: State-machine DP (day × holding state)

---

## 📜 Problem Statement

You are given an array `prices` where `prices[i]` is the price of a given stock on the `i`-th day.

Find the **maximum profit** you can achieve. You may complete as many transactions as you like (i.e., buy one and sell one share of the stock multiple times) with the following restrictions:
- After you sell your stock, you **cannot buy stock on the next day** (i.e., **cooldown one day**).

**Note:** You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).

### Examples

**Example 1:**
```
Input:  prices = [1, 2, 3, 0, 2]
Output: 3
Explanation: transactions = [buy, sell, cooldown, buy, sell]
Profit = (2 - 1) + (2 - 0) = 3.
```

**Example 2:**
```
Input:  prices = [1]
Output: 0
Explanation: Only one day; no transaction possible.
```

**Example 3:**
```
Input:  prices = [2, 1, 4]
Output: 3
Explanation: Buy at 1 (day 1), sell at 4 (day 2). Profit = 3.
```

### Constraints
```
1 <= prices.length <= 5000
0 <= prices[i] <= 1000
```

---

## 🧠 Understanding the problem

Unlimited transactions, but a **one-day cooldown** after every sale. On each day you are in exactly one of three states:

- **hold**: you currently own a share.
- **sold**: you sold *today* (so tomorrow is a forced cooldown — you cannot buy).
- **rest**: you own nothing and are free to buy (either you've been idle or your cooldown has passed).

Track the best achievable cash in each state and transition day by day. This is a tiny **state machine** unrolled over time — a 2D DP where the second dimension is "which of 3 states."

Transitions when moving to a new day with price `p`:
- `hold` = max(stay holding, buy today from a `rest` state) = `max(hold, rest - p)`.
- `sold` = sell today the share we held = `hold + p`.
- `rest` = max(stay resting, come off yesterday's cooldown) = `max(rest, prevSold)`.

5-step framework:
1. **State**: `(day, s)` with `s ∈ {hold, sold, rest}` → best cash.
2. **Transition**: the three rules above.
3. **Base case**: before any day, `hold = -∞` (can't hold for free), `sold = 0`, `rest = 0`.
4. **Order**: iterate days left to right.
5. **Answer**: `max(sold, rest)` after the last day (never end while holding).

---

## Approach 1 — Top-down memoization

### Intuition
`solve(i, holding)` = best profit from day `i` onward given whether we currently hold a share. If holding, choose sell (then skip a day for cooldown) or keep holding. If not holding, choose buy or skip.

### Algorithm
1. If `i >= n`, return 0.
2. If holding: `max(prices[i] + solve(i+2, false)  /* sell + cooldown */, solve(i+1, true) /* keep */)`.
3. If not holding: `max(-prices[i] + solve(i+1, true) /* buy */, solve(i+1, false) /* skip */)`.
4. Memoize on `(i, holding)`.

### Dry run on `prices = [1,2,3,0,2]`
```
buy@1, sell@2 (profit1), cooldown day2(idx2), buy@0, sell@2 (profit2)
total = 3
```

### Code
```cpp
class Solution {
    vector<array<int,2>> memo;
    vector<int>* p;
    int n;
    int solve(int i, int holding) {
        if (i >= n) return 0;
        if (memo[i][holding] != INT_MIN) return memo[i][holding];
        int best;
        if (holding)
            best = max((*p)[i] + solve(i + 2, 0), solve(i + 1, 1));
        else
            best = max(-(*p)[i] + solve(i + 1, 1), solve(i + 1, 0));
        return memo[i][holding] = best;
    }
public:
    int maxProfit(vector<int>& prices) {
        p = &prices; n = prices.size();
        memo.assign(n, {INT_MIN, INT_MIN});
        return solve(0, 0);
    }
};
```
```java
class Solution {
    private int[][] memo;
    private int[] p;
    private int n;
    private int solve(int i, int holding) {
        if (i >= n) return 0;
        if (memo[i][holding] != Integer.MIN_VALUE) return memo[i][holding];
        int best;
        if (holding == 1)
            best = Math.max(p[i] + solve(i + 2, 0), solve(i + 1, 1));
        else
            best = Math.max(-p[i] + solve(i + 1, 1), solve(i + 1, 0));
        return memo[i][holding] = best;
    }
    public int maxProfit(int[] prices) {
        p = prices; n = prices.length;
        memo = new int[n][2];
        for (int[] row : memo) java.util.Arrays.fill(row, Integer.MIN_VALUE);
        return solve(0, 0);
    }
}
```
```python
class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        from functools import lru_cache
        n = len(prices)

        @lru_cache(maxsize=None)
        def solve(i: int, holding: bool) -> int:
            if i >= n:
                return 0
            if holding:
                return max(prices[i] + solve(i + 2, False), solve(i + 1, True))
            return max(-prices[i] + solve(i + 1, True), solve(i + 1, False))

        return solve(0, False)
```

### Complexity
- **Time**: O(n) — 2n states.
- **Space**: O(n) memo + recursion.

### Verdict
The cooldown is encoded by `solve(i+2, ...)` after a sell. Clear, but the rolling state-machine version is the cleanest optimum.

---

## Approach 2 — Tabulated state machine

### Intuition
Carry three arrays (or, as we'll see, three scalars) `hold[i]`, `sold[i]`, `rest[i]` and apply the transitions per day.

### Algorithm
1. `hold[0] = -prices[0]`, `sold[0] = 0`, `rest[0] = 0`.
2. For `i >= 1`:
   - `hold[i] = max(hold[i-1], rest[i-1] - prices[i])`.
   - `sold[i] = hold[i-1] + prices[i]`.
   - `rest[i] = max(rest[i-1], sold[i-1])`.
3. Answer = `max(sold[n-1], rest[n-1])`.

### Dry run on `prices = [1,2,3,0,2]`
```
day0: hold=-1, sold=0, rest=0
day1(2): hold=max(-1,0-2)=-1; sold=-1+2=1; rest=max(0,0)=0
day2(3): hold=max(-1,0-3)=-1; sold=-1+3=2; rest=max(0,1)=1
day3(0): hold=max(-1,1-0)=1;  sold=-1+0=-1; rest=max(1,2)=2
day4(2): hold=max(1,2-2)=1;   sold=1+2=3;   rest=max(2,-1)=2
answer = max(3,2)=3
```

### Code
```cpp
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int n = prices.size();
        if (n <= 1) return 0;
        vector<int> hold(n), sold(n), rest(n);
        hold[0] = -prices[0]; sold[0] = 0; rest[0] = 0;
        for (int i = 1; i < n; i++) {
            hold[i] = max(hold[i - 1], rest[i - 1] - prices[i]);
            sold[i] = hold[i - 1] + prices[i];
            rest[i] = max(rest[i - 1], sold[i - 1]);
        }
        return max(sold[n - 1], rest[n - 1]);
    }
};
```
```java
class Solution {
    public int maxProfit(int[] prices) {
        int n = prices.length;
        if (n <= 1) return 0;
        int[] hold = new int[n], sold = new int[n], rest = new int[n];
        hold[0] = -prices[0];
        for (int i = 1; i < n; i++) {
            hold[i] = Math.max(hold[i - 1], rest[i - 1] - prices[i]);
            sold[i] = hold[i - 1] + prices[i];
            rest[i] = Math.max(rest[i - 1], sold[i - 1]);
        }
        return Math.max(sold[n - 1], rest[n - 1]);
    }
}
```
```python
class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        n = len(prices)
        if n <= 1:
            return 0
        hold = [0] * n
        sold = [0] * n
        rest = [0] * n
        hold[0] = -prices[0]
        for i in range(1, n):
            hold[i] = max(hold[i - 1], rest[i - 1] - prices[i])
            sold[i] = hold[i - 1] + prices[i]
            rest[i] = max(rest[i - 1], sold[i - 1])
        return max(sold[n - 1], rest[n - 1])
```

### Complexity
- **Time**: O(n).
- **Space**: O(n).

### Verdict
Explicit state machine. Each day reads only the previous day → O(1) scalars.

---

## Approach 3 — Space-optimized scalars (optimal) ⭐

### Intuition
Keep `hold`, `sold`, `rest` as scalars and update them per day. The only subtlety: `rest` needs *yesterday's* `sold`, so stash it before overwriting `sold`.

### Algorithm
1. `hold = -∞`, `sold = 0`, `rest = 0`.
2. For each price `p`: `prevSold = sold`; `sold = hold + p`; `hold = max(hold, rest - p)`; `rest = max(rest, prevSold)`.
3. Return `max(sold, rest)`.

### Dry run on `prices = [1,2,3,0,2]`
```
matches the table above -> 3
```

### Code
```cpp
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int hold = INT_MIN, sold = 0, rest = 0;
        for (int p : prices) {
            int prevSold = sold;
            sold = hold + p;
            hold = max(hold, rest - p);
            rest = max(rest, prevSold);
        }
        return max(sold, rest);
    }
};
```
```java
class Solution {
    public int maxProfit(int[] prices) {
        int hold = Integer.MIN_VALUE, sold = 0, rest = 0;
        for (int p : prices) {
            int prevSold = sold;
            sold = hold + p;
            hold = Math.max(hold, rest - p);
            rest = Math.max(rest, prevSold);
        }
        return Math.max(sold, rest);
    }
}
```
```python
class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        hold, sold, rest = float('-inf'), 0, 0
        for p in prices:
            prev_sold = sold
            sold = hold + p
            hold = max(hold, rest - p)
            rest = max(rest, prev_sold)
        return max(sold, rest)
```

### Complexity
- **Time**: O(n).
- **Space**: O(1).

### Verdict
**The optimal answer.** Three scalars carry the whole state machine.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Memoization | O(n) | O(n) | holding flag + cooldown via i+2 |
| Tabulated states | O(n) | O(n) | explicit hold/sold/rest arrays |
| Scalars | **O(n)** | **O(1)** | the answer ⭐ |

---

## 🧪 Edge cases & pitfalls
- **One day** → 0 (no transaction possible). `hold + p` is hugely negative, so `max(sold, rest) = 0`.
- **Monotonic decreasing prices** → 0 (never profitable to buy).
- **Pitfall — using updated `sold` for `rest`**: `rest` must use *yesterday's* `sold` (the cooldown comes from a sale on a previous day). Stash `prevSold` before reassigning.
- **Pitfall — order of updates**: compute `sold` from the *old* `hold` (you sell a share you were holding coming into today). In the scalar version, set `sold = hold + p` before mutating `hold`.
- **Pitfall — `hold` init**: must be `-∞` (or `-prices[0]` on day 0) so that "holding without ever buying" is impossible.

---

## 🔗 Related problems
- **Best Time to Buy and Sell Stock** (LC 121) — single transaction.
- **Best Time to Buy and Sell Stock II** (LC 122) — unlimited, no cooldown.
- **Best Time to Buy and Sell Stock with Transaction Fee** (LC 714) — same state machine, fee instead of cooldown.
- **Best Time to Buy and Sell Stock III / IV** (LC 123 / 188) — at most `k` transactions (2D `day × transactions` DP).

---

**→ Next:** [`10-Zero-One-Knapsack.md`](./10-Zero-One-Knapsack.md) | **→ Prev:** [`08-Longest-Increasing-Path-Matrix.md`](./08-Longest-Increasing-Path-Matrix.md) | Back to [`00-Index.md`](./00-Index.md)
