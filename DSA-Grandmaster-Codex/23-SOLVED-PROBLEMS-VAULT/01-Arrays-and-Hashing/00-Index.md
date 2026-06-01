# 🗂️ Arrays & Hashing — Problem Set

> Each problem below is a **complete editorial**: full statement (platform-style) → every approach from brute force to optimal → intuition, algorithm, dry run, C++ & Python code, complexity, edge cases, pitfalls, and related problems.

> **How to use**: open a problem, read ONLY the statement, attempt it cold (30–45 min). Then read the approaches in order — feel WHY each one improves on the last. Re-derive the optimal from the key insight after 7 days.

---

## 📋 Problems

| # | Problem | LC # | Difficulty | Core Approaches |
|---|---------|------|------------|-----------------|
| 01 | [Contains Duplicate](./01-Contains-Duplicate.md) | 217 | Easy | brute → sort → hash set |
| 02 | [Valid Anagram](./02-Valid-Anagram.md) | 242 | Easy | sort → count array → hash map |
| 03 | [Two Sum](./03-Two-Sum.md) | 1 | Easy | brute → two-pass hash → one-pass hash |
| 04 | [Group Anagrams](./04-Group-Anagrams.md) | 49 | Medium | sort-key → count-key |
| 05 | [Top K Frequent Elements](./05-Top-K-Frequent-Elements.md) | 347 | Medium | sort → heap → bucket sort |
| 06 | [Product of Array Except Self](./06-Product-of-Array-Except-Self.md) | 238 | Medium | brute → division → prefix/suffix |
| 07 | [Longest Consecutive Sequence](./07-Longest-Consecutive-Sequence.md) | 128 | Medium | brute → sort → hash set |
| 08 | [Valid Sudoku](./08-Valid-Sudoku.md) | 36 | Medium | 3-pass → one-pass sets |

---

## 🎯 The pattern family

**Hashing** is the unifying weapon here. The recurring move: *"I'm doing repeated lookups / counting / membership checks — a hash map or hash set turns each O(n) scan into O(1)."*

- **Seen-before check** → hash **set** (Contains Duplicate, Longest Consecutive)
- **Counting / frequency** → hash **map** or count array (Anagram, Group Anagrams, Top K)
- **Complement lookup** → hash **map** of value→index (Two Sum)
- **Prefix/suffix products or sums** → avoid recomputation (Product Except Self)

---

**→ Start:** [`01-Contains-Duplicate.md`](./01-Contains-Duplicate.md) | Back to [vault index](../00-Index.md)
