# Best Time to Buy and Sell Stock

**Platform**: LeetCode 121 · **Difficulty**: Easy · **Topics**: Array, Dynamic Programming · **Pattern**: One-pass min-tracking (sliding window variant)

---

## 📜 Problem Statement

You are given an array `prices` where `prices[i]` is the price of a given stock on the `i`-th day.

You want to maximize your profit by choosing a **single day** to buy and a **single day** in the future to sell. Return the maximum profit. If no profit is possible, return `0`.

### Examples

**Example 1:**
```
Input:  prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price=1), sell on day 5 (price=6). Profit = 6-1 = 5.
```

**Example 2:**
```
Input:  prices = [7,6,4,3,1]
Output: 0
Explanation: Prices only decrease. No profitable transaction.
```

### Constraints
```
1 <= prices.length <= 10^5
0 <= prices[i] <= 10^4
```

---

## 🧠 Understanding the problem

We need `max(prices[j] - prices[i])` for `j > i`. Equivalently: for each day `j`, the best buy day is the minimum price in `[0, j-1]`. Track that running minimum.

---

## Approach 1 — Brute force (all pairs)

### Code
```cpp
int maxProfit(vector<int>& prices) {
    int n = prices.size(), best = 0;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            best = max(best, prices[j] - prices[i]);
    return best;
}
```
```java
public int maxProfit(int[] prices) {
    int n = prices.length, best = 0;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            best = Math.max(best, prices[j] - prices[i]);
    return best;
}
```
```python
def maxProfit(prices):
    best = 0
    for i in range(len(prices)):
        for j in range(i+1, len(prices)):
            best = max(best, prices[j] - prices[i])
    return best
```

### Complexity
- **Time**: O(n²). **Space**: O(1).

### Verdict
TLE for n=10⁵.

---

## Approach 2 — One-pass min-tracking (optimal) ⭐

### Intuition
As we scan left to right, maintain the **minimum price seen so far**. At each day, the profit if we sold today = `price - minSoFar`. Track the maximum of these.

### Why it works
For any optimal sell day `j`, the best buy day is the global minimum in `[0, j-1]`. By tracking the running min, we compute this for every `j` in O(1).

### Code
```cpp
int maxProfit(vector<int>& prices) {
    int minPrice = INT_MAX, best = 0;
    for (int p : prices) {
        minPrice = min(minPrice, p);
        best = max(best, p - minPrice);
    }
    return best;
}
```
```java
public int maxProfit(int[] prices) {
    int minPrice = Integer.MAX_VALUE, best = 0;
    for (int p : prices) {
        minPrice = Math.min(minPrice, p);
        best = Math.max(best, p - minPrice);
    }
    return best;
}
```
```python
def maxProfit(prices):
    min_price, best = float('inf'), 0
    for p in prices:
        min_price = min(min_price, p)
        best = max(best, p - min_price)
    return best
```

### Complexity
- **Time**: O(n). **Space**: O(1).

### Verdict
**The optimal answer.** Single pass, O(1) space. This is also interpretable as a "sliding window" where the left boundary is the min-price position.

---

## Approach 3 — Kadane's variant (max subarray on deltas)

### Intuition
Define `delta[i] = prices[i] - prices[i-1]`. The max profit = max subarray sum of `delta` (Kadane's). This connects stock problems to Kadane's algorithm.

### Code
```python
def maxProfit(prices):
    best = cur = 0
    for i in range(1, len(prices)):
        cur = max(0, cur + prices[i] - prices[i-1])
        best = max(best, cur)
    return best
```

### Verdict
Same O(n)/O(1). Elegant connection to Kadane's, but the min-tracking approach is more intuitive for this specific problem.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Key idea |
|----------|------|-------|----------|
| Brute force | O(n²) | O(1) | all pairs |
| Min-tracking | **O(n)** | **O(1)** | running min ⭐ |
| Kadane on deltas | O(n) | O(1) | max subarray of price differences |

---

## 🧪 Edge cases & pitfalls
- **Strictly decreasing** → profit = 0 (never buy).
- **Single day** → 0 (can't sell same day).
- **All same price** → 0.
- **Pitfall**: buying AFTER selling (must be `j > i`). The one-pass naturally enforces this.

---

## 🔗 Related problems
- **Best Time II** (LC 122) — unlimited transactions (sum positive deltas).
- **Best Time III** (LC 123) — at most 2 transactions (4-state DP).
- **Best Time IV** (LC 188) — at most k transactions.
- **With Cooldown** (LC 309), **With Fee** (LC 714) — state-machine DP.

---

**→ Next:** [`02-Longest-Substring-Without-Repeating.md`](./02-Longest-Substring-Without-Repeating.md) | [Index](./00-Index.md)
