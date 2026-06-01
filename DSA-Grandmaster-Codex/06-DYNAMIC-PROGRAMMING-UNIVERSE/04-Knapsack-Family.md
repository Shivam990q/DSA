# 🧬 The Knapsack Family

> *"Pick items under a budget. The most versatile DP pattern in existence."*

---

## I. 0/1 KNAPSACK (each item once)
Items with weight w[i], value v[i]; capacity W. Maximize value.
```
dp[i][c] = max(dp[i-1][c],                  // skip item i
               dp[i-1][c-w[i]] + v[i])      // take item i (if w[i] <= c)
```
- Time O(nW), space O(nW) → **1D optimization**: iterate capacity **downward**.
```cpp
vector<long long> dp(W+1, 0);
for (int i = 0; i < n; i++)
    for (int c = W; c >= w[i]; c--)         // DOWNWARD = each item used once
        dp[c] = max(dp[c], dp[c-w[i]] + v[i]);
```

---

## II. UNBOUNDED KNAPSACK (unlimited copies)
Same, but iterate capacity **upward** (so an item can be reused):
```cpp
for (int i = 0; i < n; i++)
    for (int c = w[i]; c <= W; c++)         // UPWARD = reuse allowed
        dp[c] = max(dp[c], dp[c-w[i]] + v[i]);
```
⭐ The loop **direction** is the only difference between 0/1 and unbounded. Memorize this.

---

## III. BOUNDED KNAPSACK (k copies of each)
- Naive: treat as k separate items.
- Better: **binary splitting** (decompose k into powers of 2 → log k items).
- Best: monotonic-deque optimization, O(nW).

---

## IV. SUBSET SUM (boolean knapsack)
"Can we pick a subset summing to T?" → dp[c] = boolean reachability.
```cpp
vector<bool> dp(T+1, false); dp[0] = true;
for (int x : nums)
    for (int c = T; c >= x; c--)
        dp[c] = dp[c] || dp[c-x];
return dp[T];
```

---

## V. THE DERIVED PROBLEMS
- **Partition Equal Subset Sum (LC 416)**: subset sum with T = total/2.
- **Target Sum (LC 494)**: assign +/- to reach target → count subsets with sum = (total+target)/2.
- **Last Stone Weight II (LC 1049)**: minimize |sum1 − sum2| → subset sum closest to total/2.
- **Coin Change (LC 322)**: min coins = unbounded knapsack minimizing count.
- **Coin Change II (LC 518)**: number of ways = unbounded knapsack counting (loop coins OUTER to avoid order duplicates).
- **Ones and Zeroes (LC 474)**: 2D knapsack (two capacities: zeros and ones).
- **Combination Sum IV (LC 377)**: ordered count → loop target OUTER (order matters).

---

## VI. THE ORDER-OF-LOOPS SUBTLETY ⭐
For **counting** problems:
- **Combinations** (order doesn't matter, e.g., Coin Change II): loop items OUTER, capacity INNER.
- **Permutations** (order matters, e.g., Combination Sum IV): loop capacity OUTER, items INNER.

This single distinction trips up most learners. Internalize it.

---

## VII. COUNTING VS OPTIMIZING
- **Optimize** (max/min value): `dp[c] = max/min(...)`
- **Count** (number of ways): `dp[c] += dp[c - x]`
- **Feasibility** (can/can't): `dp[c] = dp[c] || dp[c-x]`

Same skeleton, different combine operation.

---

## VIII. COMPLEXITY
- O(n·W) time, O(W) space (1D). Pseudo-polynomial (depends on W's magnitude).
- If W is huge but values small, swap roles: dp over value, minimize weight.

---

## IX. PROBLEMS
- 0/1 Knapsack (classic / [CSES](https://cses.fi/problemset/) "Book Shop")
- Partition Equal Subset Sum (416), Target Sum (494), Last Stone Weight II (1049)
- Coin Change (322), Coin Change II (518), Combination Sum IV (377)
- Ones and Zeroes (474), Perfect Squares (279)
- CSES: Money Sums, Coin Combinations I/II, Minimizing Coins

---

**→ Next:** [`05-LIS-Family.md`](./05-LIS-Family.md)
