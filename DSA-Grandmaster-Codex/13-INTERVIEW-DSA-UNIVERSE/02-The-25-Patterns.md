# 🎯 The 25 Interview Patterns — The Complete Bible

> *"90% of FAANG interview problems are one of 25 patterns wearing a costume."*

For each pattern: **trigger → idea → template → 5 problems → gotchas.**

---

## 1. SLIDING WINDOW

**Trigger**: "subarray/substring of size k", "longest/shortest with constraint", "contiguous".

**Idea**: Maintain a window [l, r]. Expand r; shrink l when constraint violated.

**Template**:
```python
l = 0
for r in range(n):
    add(a[r])
    while invalid():
        remove(a[l]); l += 1
    ans = max(ans, r - l + 1)
```

**Problems**: LC 3, 76, 209, 239, 424.
**Gotcha**: for "exactly K", use atMost(K) - atMost(K-1).

---

## 2. TWO POINTERS

**Trigger**: "sorted array", "pair/triplet sum", "palindrome".

**Idea**: Two indices moving toward each other (or same direction).

**Template**:
```python
l, r = 0, n-1
while l < r:
    if condition(a[l], a[r]): record; l += 1; r -= 1
    elif need_larger: l += 1
    else: r -= 1
```

**Problems**: LC 11, 15, 16, 167, 42.
**Gotcha**: skip duplicates for unique triplets.

---

## 3. FAST & SLOW POINTERS

**Trigger**: "cycle", "midpoint", "Kth from end", "find duplicate".

**Idea**: Two pointers at different speeds.

**Problems**: LC 141, 142, 202, 287, 876.
**Gotcha**: cycle start = reset one pointer to head, move both at speed 1.

---

## 4. MERGE INTERVALS

**Trigger**: "intervals", "overlapping", "merge", "meeting rooms".

**Idea**: Sort by start; merge overlapping.

**Template**:
```python
intervals.sort()
result = [intervals[0]]
for cur in intervals[1:]:
    if cur[0] <= result[-1][1]: result[-1][1] = max(result[-1][1], cur[1])
    else: result.append(cur)
```

**Problems**: LC 56, 57, 253, 435, 986.

---

## 5. CYCLIC SORT

**Trigger**: "array of 1 to n", "missing number", "duplicate in range".

**Idea**: Place each number at its correct index (a[i] should be i+1).

**Problems**: LC 41, 268, 287, 442, 448.

---

## 6. IN-PLACE LINKED LIST REVERSAL

**Trigger**: "reverse linked list", "reverse in groups".

**Template**:
```python
prev, cur = None, head
while cur:
    nxt = cur.next
    cur.next = prev
    prev = cur
    cur = nxt
return prev
```

**Problems**: LC 25, 92, 206, 234, 143.

---

## 7. TREE BFS

**Trigger**: "level order", "minimum depth", "right side view", "zigzag".

**Idea**: Queue, process level by level.

**Problems**: LC 102, 103, 107, 111, 199.

---

## 8. TREE DFS

**Trigger**: "path sum", "all paths", "diameter", "ancestor".

**Idea**: Recursion, often with return values bubbling up.

**Problems**: LC 112, 113, 124, 257, 543.

---

## 9. TWO HEAPS

**Trigger**: "median in stream", "schedule", "balance two halves".

**Idea**: Max-heap for lower half, min-heap for upper half.

**Problems**: LC 295, 480, 502, 1825.

---

## 10. SUBSETS / BACKTRACKING

**Trigger**: "all combinations", "all permutations", "all subsets".

**Template**:
```python
def backtrack(start, path):
    result.append(path[:])
    for i in range(start, n):
        path.append(a[i])
        backtrack(i+1, path)
        path.pop()
```

**Problems**: LC 17, 22, 46, 78, 90.

---

## 11. MODIFIED BINARY SEARCH

**Trigger**: "sorted", "rotated", "find min/max such that".

**Problems**: LC 33, 34, 153, 162, 240.

---

## 12. BITWISE XOR

**Trigger**: "single number", "find missing/duplicate", "appears once".

**Idea**: a^a=0, a^0=a.

**Problems**: LC 136, 137, 260, 268, 421.

---

## 13. TOP K ELEMENTS

**Trigger**: "top/least K frequent/largest/closest".

**Idea**: Heap of size K, or quickselect.

**Problems**: LC 215, 347, 451, 692, 973.

---

## 14. K-WAY MERGE

**Trigger**: "merge K sorted", "smallest range across lists".

**Idea**: Min-heap of K head elements.

**Problems**: LC 23, 373, 378, 632, 1086.

---

## 15. 0/1 KNAPSACK DP

**Trigger**: "subset with sum", "partition", "can we select to reach target".

**Problems**: LC 416, 474, 494, 698, 1049.

---

## 16. UNBOUNDED KNAPSACK DP

**Trigger**: "coin change", "unlimited use", "rod cutting".

**Problems**: LC 322, 377, 518, 983, 1449.

---

## 17. FIBONACCI DP

**Trigger**: "climb stairs", "ways to reach", "house robber".

**Problems**: LC 70, 91, 198, 213, 746.

---

## 18. PALINDROMIC SUBSEQUENCE DP

**Trigger**: "longest palindrome subseq", "min insertions/cuts".

**Problems**: LC 5, 131, 132, 516, 647.

---

## 19. LONGEST COMMON SUBSTRING/SUBSEQUENCE DP

**Trigger**: "two strings", "common", "edit distance".

**Problems**: LC 72, 583, 1143, 1035, 1092.

---

## 20. TOPOLOGICAL SORT

**Trigger**: "dependencies", "order of tasks", "prerequisites".

**Problems**: LC 207, 210, 269, 310, 444.

---

## 21. DIJKSTRA / BELLMAN-FORD

**Trigger**: "shortest path", "weighted graph", "cheapest".

**Problems**: LC 743, 787, 1334, 1514, 1631.

---

## 22. UNION-FIND

**Trigger**: "connected components", "redundant edge", "merge groups".

**Problems**: LC 547, 684, 721, 947, 1319.

---

## 23. MINIMUM SPANNING TREE

**Trigger**: "minimum cost to connect all".

**Problems**: LC 1135, 1168, 1489, 1584.

---

## 24. TRIE

**Trigger**: "prefix", "autocomplete", "word dictionary", "XOR maximize".

**Problems**: LC 208, 211, 212, 421, 648.

---

## 25. MONOTONIC STACK/QUEUE

**Trigger**: "next greater/smaller", "max in window", "histogram".

**Problems**: LC 84, 85, 239, 496, 739.

---

## 🎯 THE PATTERN RECOGNITION FLOWCHART

```
Is it about a sorted array / monotonic predicate? → Binary Search / Two Pointers
Is it a contiguous subarray/substring with constraint? → Sliding Window
Is it about cycles / midpoint in linked list? → Fast & Slow Pointers
Is it intervals? → Merge Intervals / Sweep Line
Is it "all combinations/permutations/subsets"? → Backtracking
Is it "number of ways" / "min/max cost"? → DP
Is it a graph (connectivity)? → BFS/DFS/Union-Find
Is it a graph (shortest path)? → BFS/Dijkstra/Bellman-Ford
Is it a graph (ordering/dependencies)? → Topological Sort
Is it "top/least K"? → Heap
Is it "next greater/smaller" or "histogram"? → Monotonic Stack
Is it prefix/string-dictionary? → Trie
Is it "single/missing/duplicate number"? → XOR / Cyclic Sort
```

---

## 🏆 THE 30-DAY PATTERN MASTERY PLAN

- Days 1-5: Patterns 1-5 (sliding window, two pointers, fast/slow, intervals, cyclic sort)
- Days 6-10: Patterns 6-10 (LL reversal, tree BFS/DFS, two heaps, backtracking)
- Days 11-15: Patterns 11-15 (binary search, XOR, top K, K-way merge, knapsack)
- Days 16-20: Patterns 16-20 (unbounded knapsack, fibonacci, palindrome, LCS, topo)
- Days 21-25: Patterns 21-25 (Dijkstra, union-find, MST, trie, monotonic stack)
- Days 26-30: Mixed practice (random problems, identify pattern in <60 sec)

5-10 problems per pattern. By day 30, all 25 patterns are second nature.

---

**→ Next:** [`03-LeetCode-Strategy.md`](./03-LeetCode-Strategy.md)
