# 🗂️ 2D Dynamic Programming — Problem Set

> Each problem below is a **complete editorial**: full statement (platform-style) → every approach from brute force / memoization to tabulation to space-optimized → intuition, algorithm, dry run, C++ & Java & Python code, complexity, edge cases, pitfalls, and related problems.

> **How to use**: open a problem, read ONLY the statement, attempt it cold (30–45 min). Then read the approaches in order — feel WHY each one improves on the last. Re-derive the optimal from the key insight after 7 days.

---

## 📋 Problems

| # | Problem | LC # | Difficulty | Core Approaches |
|---|---------|------|------------|-----------------|
| 01 | [Unique Paths](./01-Unique-Paths.md) | 62 | Medium | memo → 2D table → 1D rolling → combinatorics |
| 02 | [Longest Common Subsequence](./02-Longest-Common-Subsequence.md) | 1143 | Medium | memo → 2D table → 1D rolling |
| 03 | [Edit Distance](./03-Edit-Distance.md) | 72 | Medium | memo → 2D table → 1D rolling |
| 04 | [Coin Change II](./04-Coin-Change-II.md) | 518 | Medium | 2D table → 1D rolling (unbounded knapsack) |
| 05 | [Target Sum](./05-Target-Sum.md) | 494 | Medium | memo → subset-sum count → 1D |
| 06 | [Maximal Square](./06-Maximal-Square.md) | 221 | Medium | brute → 2D table → 1D rolling |
| 07 | [Interleaving String](./07-Interleaving-String.md) | 97 | Medium | memo → 2D table → 1D rolling |
| 08 | [Longest Increasing Path in a Matrix](./08-Longest-Increasing-Path-Matrix.md) | 329 | Hard | brute DFS → DFS + memo → topological |
| 09 | [Best Time to Buy & Sell Stock with Cooldown](./09-Best-Time-Buy-Sell-Cooldown.md) | 309 | Medium | memo → state machine table → O(1) |
| 10 | [0/1 Knapsack](./10-Zero-One-Knapsack.md) | classic | Medium | memo → 2D table → 1D rolling |
| 11 | [Distinct Subsequences](./11-Distinct-Subsequences.md) | 115 | Hard | memo → 2D table → 1D rolling |

---

## 🎯 The pattern family

**2D Dynamic Programming** means a subproblem needs **two indices** to describe it. The state `dp[i][j]` ranges over a rectangle, and most transitions look back at a constant number of neighbors — `dp[i-1][j]`, `dp[i][j-1]`, `dp[i-1][j-1]`.

The recurring shapes:

- **Two sequences** (`dp[i][j]` over prefixes of two strings): Longest Common Subsequence, Edit Distance, Interleaving String, Distinct Subsequences. The transition compares `a[i-1]` with `b[j-1]`.
- **Grid walks** (`dp[i][j]` over cells of a matrix): Unique Paths, Maximal Square, Longest Increasing Path. The transition flows from adjacent cells.
- **Item vs capacity** (`dp[i][c]` = items considered vs remaining capacity): 0/1 Knapsack, Coin Change II, Target Sum. The second dimension is a budget.
- **Day vs state** (`dp[day][state]`): Buy/Sell with Cooldown — a small state machine unrolled over time.

### The space-collapse trick

Almost every 2D DP where `dp[i][*]` depends only on `dp[i-1][*]` (the previous row) collapses to **one or two 1D arrays**. The recipe:

1. Confirm row `i` reads only row `i-1` (and maybe row `i` to the left).
2. Replace the 2D grid with `prev[]` and `cur[]`, or a single `dp[]` updated carefully.
3. For knapsack-style budgets, the **sweep direction** of the inner loop decides 0/1 (downward) vs unbounded (upward) — exactly as in the 1D set.

Use the same **5-step DP framework** from the [1D index](../13-1D-Dynamic-Programming/00-Index.md): define the state, write the transition, set base cases, choose iteration order, read off the answer and optimize space. The only change is that "state" and "order" now span two dimensions.

---

**→ Start:** [`01-Unique-Paths.md`](./01-Unique-Paths.md) | Back to [vault index](../00-Index.md)
