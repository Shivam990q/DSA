# 🗂️ Intervals — Problem Set

> Each problem below is a **complete editorial**: full statement (platform-style) → every approach from brute force to the optimal sort-and-sweep → intuition, algorithm, dry run, C++ & Java & Python code, complexity, edge cases, pitfalls, and related problems.

> **How to use**: open a problem, read ONLY the statement, attempt it cold (30–45 min). Then read the approaches in order — feel WHY each one improves on the last. The unifying move is almost always **sort first, then make one greedy pass**. Re-derive the optimal from the key insight after 7 days.

---

## 📋 Problems

| # | Problem | LC # | Difficulty | Core Approaches |
|---|---------|------|------------|-----------------|
| 01 | [Insert Interval](./01-Insert-Interval.md) | 57 | Medium | three-phase linear merge → binary search |
| 02 | [Merge Intervals](./02-Merge-Intervals.md) | 56 | Medium | brute → sort by start + sweep |
| 03 | [Non-Overlapping Intervals](./03-Non-Overlapping-Intervals.md) | 435 | Medium | sort by end greedy → sort by start DP |
| 04 | [Meeting Rooms](./04-Meeting-Rooms.md) | 252 | Easy | brute → sort by start + adjacent check |
| 05 | [Meeting Rooms II](./05-Meeting-Rooms-II.md) | 253 | Medium | min-heap of end times → chronological sweep |
| 06 | [Minimum Interval to Include Each Query](./06-Minimum-Interval-To-Include-Query.md) | 1851 | Hard | offline sort + min-heap by size |

---

## 🎯 The pattern family

An **interval** is a pair `[start, end]`. Interval problems test whether you can impose the right *order* on a pile of ranges so that a single linear pass solves everything. The recurring decision is **what to sort by**:

- **Sort by start** when you process intervals left to right and merge/compare with the previous one: Merge Intervals, Meeting Rooms, Insert Interval (the list is already start-sorted), Meeting Rooms II (combined with a heap).
- **Sort by end** when you greedily keep the interval that finishes earliest to leave maximum room for the rest: Non-Overlapping Intervals (activity-selection). Finishing early is the classic exchange-argument greedy.
- **Sort both intervals and queries (offline)** when each query is independent and you want to feed intervals into a structure as a sweep line crosses them: Minimum Interval to Include Each Query.

### The two reflexes

1. **Overlap test**: intervals `[a,b]` and `[c,d]` (with `a <= c` after sorting by start) overlap iff `c <= b`. Whether touching endpoints count as overlap (`<=` vs `<`) depends on the problem — meetings that end exactly when the next begins usually do **not** conflict.

2. **Sweep line / heap**: when you need "how many intervals are active at once" or "the smallest active interval," sort the events and push/pop from a heap. Meeting Rooms II (count concurrent) and Min Interval to Include Query (smallest active) are both sweeps over a priority queue.

Master the "sort, then one pass with a running boundary or a heap" template and the entire family collapses into variations of the same five lines.

---

**→ Start:** [`01-Insert-Interval.md`](./01-Insert-Interval.md) | Back to [vault index](../00-Index.md)
