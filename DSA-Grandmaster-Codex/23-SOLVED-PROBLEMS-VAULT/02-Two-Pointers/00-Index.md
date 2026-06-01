# 🗂️ Two Pointers — Problem Set

> Each problem is a complete editorial: full statement → every approach from brute to optimal → C++ & Python code, complexity, edge cases.

---

## 📋 Problems

| # | Problem | LC # | Difficulty | Core Approaches |
|---|---------|------|------------|-----------------|
| 01 | [Valid Palindrome](./01-Valid-Palindrome.md) | 125 | Easy | two pointers converging |
| 02 | [Two Sum II – Sorted](./02-Two-Sum-II-Sorted.md) | 167 | Medium | two pointers converging |
| 03 | [3Sum](./03-3Sum.md) | 15 | Medium | sort + fix + two pointers |
| 04 | [Container With Most Water](./04-Container-With-Most-Water.md) | 11 | Medium | two pointers + greedy shrink |
| 05 | [Trapping Rain Water](./05-Trapping-Rain-Water.md) | 42 | Hard | brute → prefix/suffix → two pointers |

---

## 🎯 The pattern family

**Two pointers** = two indices moving through a structure (usually an array) in a coordinated way. The key insight: by reasoning about what moving each pointer does to the answer, you eliminate O(n) candidates per step → O(n²) becomes O(n).

**Two sub-patterns:**
- **Converging** (opposite ends): sorted arrays, palindromes, container problems. Move the "worse" pointer inward.
- **Chasing** (same direction): this is sliding window (covered in Topic 03).

---

**→ Start:** [`01-Valid-Palindrome.md`](./01-Valid-Palindrome.md) | Back to [vault index](../00-Index.md)
