# 🗂️ Tries — Problem Set

> Each problem below is a **complete editorial**: full statement (platform-style) → every approach from brute force to optimal → intuition, algorithm, dry run, C++ / Java / Python code, complexity, edge cases, pitfalls, and related problems.

> **How to use**: open a problem, read ONLY the statement, attempt it cold (30–45 min). Then read the approaches in order — feel WHY each one improves on the last. Re-derive the optimal from the key insight after 7 days.

---

## 📋 Problems

| # | Problem | LC # | Difficulty | Core Approaches |
|---|---------|------|------------|-----------------|
| 01 | [Implement Trie (Prefix Tree)](./01-Implement-Trie.md) | 208 | Medium | hash-set baseline → array-26 trie → hashmap trie |
| 02 | [Design Add and Search Words](./02-Add-And-Search-Word.md) | 211 | Medium | linear scan → trie + DFS for `.` |
| 03 | [Word Search II](./03-Word-Search-II.md) | 212 | Hard | per-word DFS → trie-driven board DFS |

---

## 🎯 The pattern family

A **trie** (prefix tree) is a tree where every edge is labelled with a character and every root-to-node path spells a prefix. The single unifying idea: *"I'm doing repeated work that all shares a common prefix — store the prefixes once and walk them in O(L)."*

- **Prefix / autocomplete / dictionary lookups** → store words in a trie, every operation is O(L) where L = word length, independent of how many words you stored (Implement Trie).
- **Wildcard matching** (`.` matches any char) → the trie shape is identical, but a `.` forces a DFS branch over all children at that depth (Add and Search Words).
- **Search many words against one structure at once** → build a trie of ALL query words, then traverse the search space (a grid, a string) ONCE while walking the trie in lockstep. Shared prefixes are explored a single time, and dead branches prune instantly (Word Search II).

**The mental model**: each node owns up to 26 children (`a`–`z`) plus a boolean `isEnd` flag (or stores the full word at the terminal node). Insert = walk/create nodes char by char, set `isEnd` at the last. Search = walk char by char; you either fall off the trie (return false) or land on a node and inspect `isEnd`.

**When to reach for a trie vs a hash set**: a hash set answers "is this *exact* word present?" in O(L) too. The trie wins the moment you need **prefix** semantics, **shared-prefix traversal**, or **ordered / wildcard** queries — things a flat hash set cannot do without scanning every key.

---

**→ Start:** [`01-Implement-Trie.md`](./01-Implement-Trie.md) | Back to [vault index](../00-Index.md)
