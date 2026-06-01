# 🗂️ Sliding Window — Problem Set

> Each problem is a complete editorial: full statement → every approach from brute to optimal → C++ & Python code, complexity, edge cases.

---

## 📋 Problems

| # | Problem | LC # | Difficulty | Core Approaches |
|---|---------|------|------------|-----------------|
| 01 | [Best Time to Buy and Sell Stock](./01-Best-Time-Buy-Sell-Stock.md) | 121 | Easy | brute → one-pass min-tracking |
| 02 | [Longest Substring Without Repeating](./02-Longest-Substring-Without-Repeating.md) | 3 | Medium | brute → sliding window + hash |
| 03 | [Longest Repeating Character Replacement](./03-Longest-Repeating-Char-Replacement.md) | 424 | Medium | brute → sliding window + max-freq |
| 04 | [Permutation in String](./04-Permutation-In-String.md) | 567 | Medium | sort → fixed window + freq compare |
| 05 | [Minimum Window Substring](./05-Minimum-Window-Substring.md) | 76 | Hard | brute → variable window + formed counter |
| 06 | [Sliding Window Maximum](./06-Sliding-Window-Maximum.md) | 239 | Hard | brute → monotonic deque |

---

## 🎯 The pattern family

**Sliding window** = a contiguous range [l, r] that expands (r++) and shrinks (l++) based on a constraint. The key: the constraint is **monotonic** — once the window is invalid, extending it further (without shrinking) keeps it invalid. This lets `l` only move forward → O(n) total.

**Two sub-types:**
- **Variable-size**: grow until invalid, shrink until valid, record best (longest/shortest).
- **Fixed-size**: window always has size k; slide by adding right, removing left.

---

**→ Start:** [`01-Best-Time-Buy-Sell-Stock.md`](./01-Best-Time-Buy-Sell-Stock.md) | Back to [vault index](../00-Index.md)
