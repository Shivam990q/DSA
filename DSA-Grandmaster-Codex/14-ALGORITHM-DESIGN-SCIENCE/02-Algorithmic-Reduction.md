# 🔄 Algorithmic Reduction — The Art of Conversion

> *"Don't solve the problem. Convert it to a problem you've already solved."*

---

## I. WHAT IS A REDUCTION?

A **reduction** transforms problem A into problem B such that:
- If you can solve B, you can solve A
- The transformation is efficient (usually polynomial)

Reductions are how we:
- Solve new problems via old solutions
- Prove problems are hard (NP-completeness)
- Establish equivalences

---

## II. THE TWO DIRECTIONS

### "A reduces to B" (A ≤ B)
If B is easy, A is easy. (Use B's solver to solve A.)

### Used for:
- **Solving**: reduce your problem to a known-solvable one
- **Hardness**: reduce a known-hard problem to yours → yours is hard too

---

## III. REDUCTIONS FOR SOLVING (the practical use)

### Example 1: Maximum bipartite matching → Max flow
- Add source S connected to all left vertices (capacity 1)
- Add sink T connected from all right vertices (capacity 1)
- Original edges have capacity 1
- Max flow = max matching

### Example 2: Longest path in DAG → Shortest path
- Negate all edge weights
- Find shortest path
- Negate the answer

### Example 3: "K-th largest" → Quickselect / Heap
- Reframe "K-th largest" as a selection problem
- Use quickselect (O(n) avg) or min-heap of size K

### Example 4: "Minimum spanning tree with one fixed edge"
- Force the edge in; run MST on the rest
- Reduction to standard MST

### Example 5: Interval scheduling → Sort + greedy
- Sort by end time
- Greedily select non-overlapping

### Example 6: "Assign tasks to minimize max load" → Binary search + feasibility
- Binary search the answer (max load L)
- Feasibility: can we assign with each ≤ L? (greedy check)

---

## IV. CLASSIC REDUCTION CHAINS

### SAT → 3-SAT → many NP-complete problems
- SAT (general boolean satisfiability) reduces to 3-SAT
- 3-SAT reduces to: vertex cover, clique, independent set, graph coloring, Hamiltonian cycle, subset sum, ...

### These reductions prove NP-completeness
> If a polynomial algorithm existed for any NP-complete problem, all NP problems would be polynomial (P = NP).

---

## V. REDUCTION AS A PROBLEM-SOLVING TOOL

When stuck on a problem, ask:

1. **"What known problem does this resemble?"**
2. **"Can I transform my input into that problem's input?"**
3. **"Can I transform that problem's output into my output?"**

> Example: "Find if you can partition array into two equal-sum subsets" → reduce to "subset sum with target = total/2" → solve with DP.

> Example: "Find min number of platforms for trains" → reduce to "max overlapping intervals" → sweep line.

---

## VI. THE REDUCTION TOOLKIT

| Your problem looks like...           | Reduce to...                         |
|--------------------------------------|--------------------------------------|
| Assignment / matching                | Bipartite matching / flow            |
| "Min max" or "max min"               | Binary search + feasibility          |
| Partition into equal sums            | Subset sum DP                        |
| Scheduling with deadlines            | Greedy / interval scheduling         |
| Pairing with constraints             | Matching / flow                      |
| Selection with budget                | Knapsack DP                          |
| Connectivity over time               | Union-Find / offline                 |
| Path optimization                    | Shortest path (Dijkstra/BF)          |
| Counting configurations              | DP / combinatorics                   |
| "Is X reachable?"                    | BFS/DFS on state graph               |

---

## VII. EXAMPLE WORKED REDUCTION

**Problem**: "You have n jobs, each takes time t[i]. You have 2 machines. Minimize the time when both machines finish (makespan)."

**Recognize**: This is "partition into two subsets with minimum difference in sums."

**Reduce**: 
- Total sum = S
- Find subset with sum closest to S/2 (subset sum DP)
- Makespan = max(subset_sum, S − subset_sum)

**Solve**: 
- DP: `dp[s]` = can we achieve sum s?
- Find largest s ≤ S/2 with `dp[s]` true
- Answer = S − s

We solved a "machine scheduling" problem by reducing to "subset sum."

---

## VIII. THE DANGER OF REDUCTIONS

1. **Overhead**: the reduction itself may be expensive
2. **Loss of structure**: a specialized problem may have a faster direct solution than the general one you reduce to
3. **Incorrect reductions**: must verify the transformation preserves the answer

Always check: does my reduction correctly map inputs AND outputs?

---

## IX. EXERCISES

For each, find the reduction:

1. "Schedule meetings in minimum rooms" → ?
2. "Find if a string can be segmented into dictionary words" → ?
3. "Assign workers to tasks to minimize total cost" → ?
4. "Find longest path in a tree" → ?
5. "Determine if array can be split into K equal-sum parts" → ?
6. "Maximize people you can invite given conflict pairs" → ?

(Sample answers: 1) max overlapping intervals / sweep, 2) DP / BFS on positions, 3) assignment problem / min-cost matching, 4) two BFS/DFS (tree diameter), 5) bitmask DP / backtracking, 6) maximum independent set — NP-hard in general!)

---

## X. RECOMMENDED READING

- **CLRS Chapter 34** — NP-completeness & reductions
- **Garey & Johnson**, *Computers and Intractability* — the NP-completeness bible
- **Kleinberg & Tardos Chapter 8** — NP and reductions

---

**→ Next:** [`03-Lower-Bound-Reasoning.md`](./03-Lower-Bound-Reasoning.md)
