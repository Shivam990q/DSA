# 🗂️ 1D Dynamic Programming — Problem Set

> Each problem below is a **complete editorial**: full statement (platform-style) → every approach from brute force / memoization to tabulation to space-optimized → intuition, algorithm, dry run, C++ & Java & Python code, complexity, edge cases, pitfalls, and related problems.

> **How to use**: open a problem, read ONLY the statement, attempt it cold (30–45 min). Then read the approaches in order — feel WHY each one improves on the last. Re-derive the optimal from the key insight after 7 days.

---

## 📋 Problems

| # | Problem | LC # | Difficulty | Core Approaches |
|---|---------|------|------------|-----------------|
| 01 | [Climbing Stairs](./01-Climbing-Stairs.md) | 70 | Easy | recursion → memo → tabulation → O(1) rolling |
| 02 | [Min Cost Climbing Stairs](./02-Min-Cost-Climbing-Stairs.md) | 746 | Easy | memo → tabulation → O(1) rolling |
| 03 | [House Robber](./03-House-Robber.md) | 198 | Medium | memo → tabulation → O(1) rolling |
| 04 | [House Robber II](./04-House-Robber-II.md) | 213 | Medium | circular split → two linear runs |
| 05 | [Longest Palindromic Substring](./05-Longest-Palindromic-Substring.md) | 5 | Medium | brute → DP table → expand-around-center |
| 06 | [Palindromic Substrings](./06-Palindromic-Substrings.md) | 647 | Medium | brute → DP table → expand-around-center |
| 07 | [Decode Ways](./07-Decode-Ways.md) | 91 | Medium | recursion → memo → tabulation → O(1) |
| 08 | [Coin Change](./08-Coin-Change.md) | 322 | Medium | memo → tabulation (unbounded knapsack) |
| 09 | [Maximum Product Subarray](./09-Maximum-Product-Subarray.md) | 152 | Medium | brute → track max/min → O(1) |
| 10 | [Word Break](./10-Word-Break.md) | 139 | Medium | memo → tabulation |
| 11 | [Longest Increasing Subsequence](./11-Longest-Increasing-Subsequence.md) | 300 | Medium | O(n²) DP → O(n log n) patience |
| 12 | [Partition Equal Subset Sum](./12-Partition-Equal-Subset-Sum.md) | 416 | Medium | 2D subset-sum → 1D rolling (0/1 knapsack) |

---

## 🎯 The pattern family

**1D Dynamic Programming** means the *state* of a subproblem is captured by a **single index** (or a small constant set of scalars). You define `dp[i]` over one dimension — a position in an array, a stair number, a prefix length, a target amount — and you compute it from a constant number of earlier entries.

The recurring moves:

- **Linear recurrences** (`dp[i]` from `dp[i-1]`, `dp[i-2]`): Climbing Stairs, Min Cost, House Robber, Decode Ways. These collapse to **O(1) space** because each entry depends on a fixed window.
- **Amount / capacity DP** (`dp[a]` over a target value): Coin Change, Partition Equal Subset Sum. The index is "how much is left to make."
- **Prefix DP** (`dp[i]` = answer for the first `i` characters): Word Break, Decode Ways.
- **Subsequence DP** (`dp[i]` = best run ending at `i`): Longest Increasing Subsequence, Maximum Product Subarray.
- **Substring expansion** (centers, not a classic table): Longest Palindromic Substring, Palindromic Substrings.

---

## 🪜 The 5-Step DP Framework

Every DP solution in this set was built with the same five questions. Use them as a checklist when you sit down cold:

1. **Define the state.** What does `dp[i]` *mean* in one sentence? Be ruthless: "ways to reach step i", "min coins to make amount a", "can the first i chars be segmented". If you cannot say it in words, you cannot code it.
2. **Write the transition (recurrence).** How is `dp[i]` built from smaller states? This is the "choice" line — you usually `max`/`min`/`sum` over the options available at step `i`.
3. **Establish the base case(s).** What are the smallest states whose answers are known without recursion? `dp[0]`, `dp[1]`, the empty string, amount 0.
4. **Decide the iteration order.** Tabulation must compute every state *after* the states it depends on. For knapsack-style problems, the sweep direction (forward vs backward) decides 0/1 vs unbounded.
5. **Read off the answer & optimize space.** Which entry is the final answer (`dp[n]`? `max(dp)`?). Then ask: does each entry depend on only the last `k` entries? If so, replace the array with `k` rolling variables for O(1) space.

> Brute-force recursion = steps 1–3 expressed as a function. Memoization = cache that function. Tabulation = fill steps 1–4 bottom-up. Space optimization = step 5. You are always doing the same four transformations.

---

**→ Start:** [`01-Climbing-Stairs.md`](./01-Climbing-Stairs.md) | Back to [vault index](../00-Index.md)
