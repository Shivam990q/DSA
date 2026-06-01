# 💎 Greedy Algorithms — When Local is Global

> *"A greedy algorithm makes the locally optimal choice at each step. The miracle: sometimes that's globally optimal."*

---

## I. THE GREEDY PROMISE

Greedy = at each step, pick the choice that looks best **right now**, without backtracking.

**The catch**: greedy doesn't always work.

The art: identifying when greedy works (and proving it).

---

## II. THE TWO REQUIREMENTS

For greedy to work, the problem must have:

### 1. Greedy choice property
A globally optimal solution can be reached by a series of locally optimal choices.

### 2. Optimal substructure
The optimal solution to the problem contains optimal solutions to subproblems.

(Greedy is a special case of DP where the choice is forced, not chosen.)

---

## III. THE PROOF TECHNIQUES

### Exchange argument
Show: if any optimal solution makes a "non-greedy" choice, you can swap it with the greedy choice without making the solution worse.

### Greedy stays ahead
At each step, the greedy's partial solution is at least as good as any other algorithm's.

### Matroid theory
The problem has the structure of a matroid → greedy is optimal (Edmonds-Rado theorem).

---

## IV. CLASSIC GREEDY ALGORITHMS

### 1. Activity Selection
Pick max number of non-overlapping intervals.
**Greedy**: sort by end time. Pick earliest-finishing that doesn't conflict.
**Proof**: exchange argument — if optimal doesn't pick earliest-finishing, swap with first chosen → no decrease.

### 2. Fractional Knapsack
Pack items (fractional allowed) for max value within capacity.
**Greedy**: sort by value/weight ratio; take in order until capacity full.

### 3. Huffman Coding
Build optimal prefix-code tree.
**Greedy**: merge two smallest-frequency nodes; repeat.

### 4. Kruskal's MST
**Greedy**: sort edges by weight; add if doesn't form cycle (DSU).

### 5. Prim's MST
**Greedy**: from any starting vertex, repeatedly add cheapest edge connecting tree to non-tree.

### 6. Dijkstra's Shortest Path (non-negative weights)
**Greedy**: extract closest unfinalized vertex; relax neighbors.

### 7. Job Sequencing with Deadlines
**Greedy**: sort by profit descending; schedule each in latest available slot ≤ deadline.

### 8. Coin Change (canonical systems)
**Greedy**: take largest coin ≤ remaining; repeat.
**Caveat**: only works for canonical systems (USD, INR). For arbitrary, use DP.

---

## V. WHEN GREEDY FAILS

### Counterexample 1: Coin change with [1, 3, 4], target 6
Greedy: 4 + 1 + 1 = 3 coins. Optimal: 3 + 3 = 2 coins.

### Counterexample 2: 0/1 knapsack (greedy by value/weight ratio fails)
Items (weight, value): **A = (10, 60)**, **B = (20, 100)**, **C = (30, 120)**. Capacity **W = 50**.

Value/weight ratios: A = 6.0, B = 5.0, C = 4.0. Greedy takes the highest ratio first:
- Take A (w=10, v=60), then B (w=20, v=100) → used 30, value 160. C doesn't fit in the remaining 20. **Greedy total = 160.**

But the true optimum is **B + C** (w = 50, v = 220). **Greedy = 160 < optimal = 220.**

→ **0/1 knapsack: greedy by ratio fails. Use DP.** (Fractional knapsack, where you can take a *part* of C, IS solvable by this greedy — that's the key difference.)

---

## VI. THE GREEDY PROBLEM CHECKLIST

Before submitting greedy:

1. **State the greedy choice precisely.**
2. **Try counterexamples mentally** (small cases, edge cases).
3. **Prove or sketch why greedy is optimal.**
4. **Test on examples.**
5. **If unsure, write DP as backup.**

---

## VII. GREEDY PROBLEM CATEGORIES

### Interval problems
- Activity selection (LC 435 alike)
- Non-overlapping intervals
- Minimum number of arrows (LC 452)
- Meeting rooms II (LC 253)
- Minimum platforms

### Scheduling
- Job sequencing
- Earliest deadline first
- Smallest remaining time

### Picking
- Gas station (LC 134)
- Jump game I, II (LC 55, 45)
- Minimum number of refueling stops

### Compression / encoding
- Huffman coding
- Run-length encoding (greedy choice trivial)

### Graph
- Kruskal, Prim
- Dijkstra
- Topological sort

### Hard greedy
- Candy distribution (LC 135)
- Reorganize string (LC 767)
- Task scheduler (LC 621)
- IPO (LC 502)

---

## VIII. EXCHANGE ARGUMENT — A WORKED EXAMPLE

**Problem**: Activity selection. Given activities with start/end times, pick max number non-overlapping.

**Greedy**: sort by end time; pick first non-conflicting.

**Proof by exchange**:

Let A = greedy's selection. Let O = optimal selection with max |O|.

If A = O, done. Otherwise:
1. Sort both by start time.
2. Find first index where they differ. Say A picks a; O picks o ≠ a.
3. Greedy picks a = earliest-finishing valid; o is some later-finishing.
4. Replace o with a in O. Resulting O' is still valid (a ends before o, so doesn't conflict with later picks). |O'| = |O|.
5. Repeat for each difference.

End: O is transformed into A with same size. Therefore |A| = |O|. □

---

## IX. PROBLEMS (TOP 25)

1. Activity selection
2. Fractional knapsack
3. Job sequencing
4. Huffman coding
5. Minimum platforms
6. Connect ropes (heap-based greedy)
7. Jump game (greedy reachability)
8. Jump game II (BFS-style greedy)
9. Gas station
10. Candy distribution
11. Reorganize string
12. Task scheduler
13. IPO
14. Minimum number of arrows
15. Non-overlapping intervals
16. Meeting rooms II
17. Largest number (custom sort)
18. Maximum sum after k operations
19. Minimum cost to hire k workers
20. Boats to save people (LC 881)
21. Lemonade change (LC 860)
22. Queue reconstruction by height (LC 406)
23. Two city scheduling (LC 1029)
24. Minimum cost tree from leaf values (LC 1130)
25. Wiggle subsequence

---

## X. THE FINAL TRUTH

> **"Greedy is the simplest paradigm that requires the most rigor.  
>  When wrong, it's silently wrong.  
>  When right, it's beautifully fast.  
>  Always prove."**

---

**→ Next:** [`05-Backtracking.md`](./05-Backtracking.md)
