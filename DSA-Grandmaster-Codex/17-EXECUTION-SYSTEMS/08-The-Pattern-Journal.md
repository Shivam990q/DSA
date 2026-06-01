# 📔 The Pattern Journal — Your Compressed Experience

> *"Pattern recognition is compressed experience. The journal is the compressor."*

---

## I. WHAT IS THE PATTERN JOURNAL?

A living document where you record **every pattern you discover**, indexed for fast recall.

While the **Mistake Log** records what went wrong, the **Pattern Journal** records what you learned to do right.

---

## II. THE PATTERN ENTRY TEMPLATE

```
PATTERN NAME: Sliding Window with Character Constraint

TRIGGER (when to recognize it):
  - "longest/shortest substring with [constraint on characters]"
  - "at most K distinct", "exactly K", "without repeating"

THE IDEA (in one sentence):
  - Maintain a window [l, r]; expand r; shrink l when constraint violated.

TEMPLATE CODE:
  l = 0
  for r in range(n):
      add(a[r])
      while invalid():
          remove(a[l]); l += 1
      answer = max(answer, r - l + 1)

EXAMPLE PROBLEMS:
  - LC 3: Longest substring without repeating
  - LC 76: Minimum window substring
  - LC 340: Longest substring with at most K distinct

KEY INSIGHT:
  - Works when the constraint is monotonic in window size:
    once invalid, stays invalid until we shrink.

GOTCHAS:
  - For "exactly K", compute "at most K" minus "at most K-1".
  - Reset counters between test cases.

DATE LEARNED: 2026-05-29
MASTERY LEVEL: 3/4 (can apply, working toward teaching)
```

---

## III. ORGANIZING THE JOURNAL

### By topic
```
Pattern-Journal/
├── arrays.md
├── strings.md
├── trees.md
├── graphs.md
├── dp.md
├── greedy.md
├── math.md
└── data-structures.md
```

### Or by single searchable file
One big markdown with headers per pattern. Ctrl+F to find.

### Or flashcard app (Anki)
Front: trigger / problem. Back: pattern / approach. Spaced repetition.

---

## IV. THE 50 CORE PATTERNS TO JOURNAL

(Seed your journal with these; expand over time.)

### Array / Sequence (10)
1. Two pointers (opposite ends)
2. Sliding window (fixed)
3. Sliding window (variable + constraint)
4. Prefix sum
5. Difference array
6. Kadane (max subarray)
7. Boyer-Moore voting
8. Cyclic sort (1..n)
9. Dutch national flag
10. Merge intervals

### Search (5)
11. Binary search (sorted)
12. Binary search on answer
13. Ternary search (unimodal)
14. Search in rotated array
15. Meet in the middle

### Stack / Queue (4)
16. Monotonic stack (next greater/smaller)
17. Monotonic deque (sliding max)
18. Stack for matching (parens)
19. Expression evaluation

### Linked List (2)
20. Fast & slow pointers
21. In-place reversal

### Tree (5)
22. DFS traversals (pre/in/post)
23. BFS level order
24. Tree DP (post-order)
25. Re-rooting
26. LCA (binary lifting)

### Graph (8)
27. BFS shortest path
28. DFS components / cycle
29. Topological sort
30. Dijkstra
31. Bellman-Ford
32. Union-Find
33. MST (Kruskal/Prim)
34. 0-1 BFS

### DP (10)
35. 1D linear DP
36. 0/1 knapsack
37. Unbounded knapsack
38. LIS (O(n log n))
39. LCS / edit distance
40. Interval DP
41. Tree DP
42. Bitmask DP
43. Digit DP
44. DP optimization (CHT/Knuth)

### Other (6)
45. Backtracking (subsets / permutations)
46. Heap (top K)
47. Two heaps (median)
48. Trie
49. Coordinate compression
50. Sweep line

---

## V. THE WEEKLY JOURNAL RITUAL

Every Sunday (15 min):
1. Review patterns added this week
2. Bump mastery level (1-4) on patterns you practiced
3. Identify patterns at mastery 1-2 → schedule drills
4. Cross-link related patterns

---

## VI. THE MASTERY SCALE PER PATTERN

| Level | Meaning                                       |
|-------|-----------------------------------------------|
| 1     | I recognize it when told                      |
| 2     | I can apply it with the template open         |
| 3     | I can apply it from memory                    |
| 4     | I can derive & teach it from first principles |

Goal: all 50 core patterns at level 4.

---

## VII. THE PATTERN-RECOGNITION DRILL

Once a week, do a "naming drill":
- Open 10 random problems (don't solve)
- For each, in 60 seconds, name the pattern(s)
- Check against editorial

Track your recognition speed. Goal: <30 seconds per problem at expert level.

---

## VIII. WHY THIS WORKS

The grandmaster's edge isn't IQ — it's **a large, well-indexed pattern library** with **fast recall**.

The journal externalizes the library. Reviewing it internalizes it. Over years, recall becomes instant. That instant recall IS expertise.

---

**→ Next:** [`09-Time-And-Energy-Management.md`](./09-Time-And-Energy-Management.md)
