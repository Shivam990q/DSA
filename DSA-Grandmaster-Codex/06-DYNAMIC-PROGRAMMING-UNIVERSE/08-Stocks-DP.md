# 🧬 Stock DP (State-Machine DP)

> *"Buy, sell, hold, cooldown — a finite state machine that prints money in interviews."*

---

## I. THE STATE-MACHINE VIEW
At each day you're in a state: **holding** a stock or **not holding**. Transitions (buy/sell/rest) move between states. The whole family is one state machine with variations.

---

## II. THE SIX VARIANTS

### I. One transaction (LC 121)
Buy once, sell once. Track min price so far; answer = max(price − minSoFar).

### II. Unlimited transactions (LC 122)
Buy/sell any number of times → greedily sum all positive day-to-day deltas.

### III. At most 2 transactions (LC 123)
4 states: `buy1, sell1, buy2, sell2`.
```cpp
int buy1 = -prices[0], sell1 = 0, buy2 = -prices[0], sell2 = 0;
for (int p : prices) {
    buy1  = max(buy1, -p);
    sell1 = max(sell1, buy1 + p);
    buy2  = max(buy2, sell1 - p);
    sell2 = max(sell2, buy2 + p);
}
return sell2;
```

### IV. At most k transactions (LC 188)
Generalize to 2k states; or `dp[t][i]` with the "max(dp[t-1][j]-prices[j])" optimization → O(nk). If k ≥ n/2, it's effectively unlimited (variant II).

### With Cooldown (LC 309)
3 states: **held**, **sold-today (cooldown)**, **rest (can buy)**. After selling you must rest one day.
```cpp
int held = -prices[0], sold = 0, rest = 0;
for (int i = 1; i < n; i++) {
    int prevSold = sold;
    sold = held + prices[i];
    held = max(held, rest - prices[i]);
    rest = max(rest, prevSold);
}
return max(sold, rest);
```

### With Transaction Fee (LC 714)
Like unlimited, but subtract fee on each sell.

---

## III. THE UNIFIED FRAMEWORK
`dp[i][k][holding]` = max profit on day i, with k transactions left, holding or not.
- `dp[i][k][0] = max(dp[i-1][k][0], dp[i-1][k][1] + prices[i])`   // rest or sell
- `dp[i][k][1] = max(dp[i-1][k][1], dp[i-1][k-1][0] - prices[i])` // rest or buy
All six problems are special cases (k=1, k=∞, k=2, k=k, +cooldown, +fee).

---

## IV. STATE-MACHINE DP IN GENERAL
This pattern—**a small set of states with defined transitions, iterated over a sequence**—appears beyond stocks:
- Paint House (LC 256/265) — state = last color
- House Robber (LC 198/213) — state = robbed/not
- Knight Dialer (LC 935) — state = current digit
- String DP with allowed transitions

Recognize "finite states + per-step transitions" → state-machine DP.

---

## V. COMPLEXITY
- I, II, cooldown, fee: O(n), O(1) space
- III: O(n), O(1)
- IV (k transactions): O(nk), reducible space

---

## VI. PROBLEMS
- Best Time to Buy/Sell Stock I-IV (121, 122, 123, 188)
- With Cooldown (309), With Fee (714)
- Paint House (256/265), Paint Fence (276)
- Knight Dialer (935)
- House Robber (198/213/337)

---

**→ Next:** [`09-Interval-DP.md`](./09-Interval-DP.md)
