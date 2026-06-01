# 🎯 Pattern Recognition — Compressed Experience

> *"Pattern recognition is what years of practice compress into instinct."*

---

## I. WHY PATTERN RECOGNITION

A grandmaster sees a 2400 problem and within 30 seconds says: *"This is segment tree with lazy + binary search on value."*

A beginner reads the same problem and says: *"???"*

The difference: **patterns**. The grandmaster has 500+ in their head, indexed by surface features.

---

## II. THE PATTERN HIERARCHY

### Level 1: **Topic patterns** (broad)
- "It's a graph problem."
- "It's DP."
- "It's a tree problem."

### Level 2: **Subtopic patterns**
- "It's BFS on a state graph."
- "It's interval DP."
- "It's tree DP with re-rooting."

### Level 3: **Technique patterns**
- "Bitmask DP with subset enumeration."
- "Two pointers on sorted prefix sums."
- "Monotonic stack for next greater element."

### Level 4: **Trick patterns**
- "The complement is easier — count bad strings, subtract."
- "Square-root decomposition makes this O(√n) per query."
- "Coordinate compression turns 10⁹ into 10⁵."

### Level 5: **Idea patterns**
- "There's always an optimal solution where the first move is X."
- "Inductively, if it works for n, it works for n+1 by adding..."

---

## III. THE TOP 50 PATTERNS (CHEAT-SHEET)

### Array / Sequence
1. **Sliding window** (fixed/variable)
2. **Two pointers** (same/opposite direction)
3. **Prefix sum** (O(1) range sums)
4. **Difference array** (range updates)
5. **Kadane** (max subarray)
6. **Boyer-Moore voting** (majority element)
7. **Cyclic sort** (1..n problems)
8. **Square root decomposition** (block scheme)

### Search / Decision
9. **Binary search** (sorted)
10. **Binary search on answer** (monotonic predicate)
11. **Ternary search** (unimodal real function)
12. **Meet in the middle** (n=40)

### Stacks / Monotonic
13. **Stack for matching** (parens)
14. **Monotonic stack** (next greater/smaller)
15. **Monotonic deque** (sliding window max)

### Graph
16. **BFS** (unweighted shortest path)
17. **DFS** (cycles, components)
18. **0-1 BFS** (weights only 0/1)
19. **Dijkstra** (non-negative weights)
20. **Bellman-Ford** (negative weights, ≤V-1 hops)
21. **Floyd-Warshall** (all-pairs)
22. **Topological sort** (DAG)
23. **Union-Find** (dynamic connectivity)
24. **MST** (Kruskal/Prim)
25. **Bridges/Articulation** (Tarjan)
26. **SCC** (Tarjan/Kosaraju)
27. **Bipartite matching** (Kuhn/Hopcroft-Karp)
28. **Max flow** (Dinic)

### Tree
29. **DFS tree DP**
30. **Re-rooting**
31. **LCA via binary lifting / Euler tour**
32. **HLD**
33. **Centroid decomposition**

### DP
34. **Linear DP** (1D)
35. **Knapsack** (0/1, unbounded)
36. **LIS / LCS / Edit distance** (classic 2D)
37. **Interval DP** (matrix chain, burst balloons)
38. **Bitmask DP** (TSP, subset)
39. **Digit DP** (count in [L,R])
40. **Probability/Expected DP**
41. **DP optimizations** (CHT, Knuth, D&C)

### String
42. **Hashing** (rolling)
43. **KMP / Z-algorithm**
44. **Suffix array / automaton**
45. **Trie**
46. **Manacher** (palindromes)

### Math
47. **Sieve** (primes)
48. **Modular inverse** (Fermat)
49. **Combinatorics** (nCr, Catalan)
50. **FFT/NTT** (polynomial multiplication)

---

## IV. PATTERN MATCHING WORKFLOW

When you read a new problem:

1. **What's the input shape?** (array, tree, graph, string, matrix)
2. **What's the output type?** (count, max/min, exists, list)
3. **What are the constraints?** → algorithm class
4. **What are the keywords?** → specific patterns
5. **Have I seen this exact pattern before?** → use template

If yes to step 5: code in 10 minutes.
If no: derive from first principles.

---

## V. TRAINING PATTERN RECOGNITION

### Method 1: **Topical immersion**
Pick one pattern. Solve 30-50 problems. Pattern is now stage 4.

### Method 2: **Pattern flashcards**
For each pattern, have:
- Trigger keywords
- Template code
- 3 example problems
- 1 sentence summary

Review weekly.

### Method 3: **Editorial reading**
Read 1 editorial per day, even of unsolved problems. Note the pattern. Build the library.

### Method 4: **Tagged problem sprints**
[LeetCode](https://leetcode.com)/CF have tags. Solve 10 problems with tag "monotonic stack" in a day. Pattern locks in.

### Method 5: **Speed drills**
Time yourself on tagged problems. Goal: pattern recognition in <60 seconds.

---

## VI. THE DANGER: OVER-PATTERN-MATCHING

Sometimes a problem **looks like** a known pattern but isn't.

> Example: "Find the longest increasing subsequence" — usually O(n log n) DP.
> But if "elements within distance k", that's NOT the standard LIS — needs different DP.

**Defense**: always verify the pattern fits ALL constraints, not just surface keywords.

---

## VII. PATTERN COMPOSITION

Hard problems = **composition of patterns**.

> Example: "Find min path in grid with at most k obstacle removals."
> Pattern 1: BFS for shortest path.
> Pattern 2: State augmentation (track # obstacles used).
> Combined: BFS on state (x, y, k_used).

> Example: "Sum of subarray minimums."
> Pattern 1: For each element, count subarrays where it's the min.
> Pattern 2: Monotonic stack for "next/prev smaller."
> Combined: NSE/PSE bounds, multiply.

The grandmaster's edge: **fluid composition** of patterns.

---

## VIII. PATTERN VS ALGORITHM

- **Algorithm**: a specific procedure (Dijkstra)
- **Pattern**: a recurring structure across problems (graph + non-negative weights → Dijkstra)

The same algorithm can serve many patterns. The same pattern can use multiple algorithms (e.g., MST: Kruskal or Prim).

---

## IX. EXERCISES

For each, identify the pattern (Level 1, 2, 3 of the hierarchy):

1. "Find pair with sum k in a sorted array." → ?
2. "Find min cost to cover all cells with given rectangles." → ?
3. "Count subarrays whose product < k." → ?
4. "Find longest substring with at most 2 distinct chars." → ?
5. "Topological order of tasks with dependencies." → ?
6. "Find diameter of tree." → ?
7. "Number of distinct paths in DAG from s to t." → ?
8. "Minimum operations to make array non-decreasing." → ?

(Answers: 1) two pointers, 2) interval DP, 3) sliding window, 4) sliding window, 5) topo sort, 6) DFS tree DP, 7) DAG DP, 8) greedy/stack)

---

**→ Next:** [`05-Brute-Force-First.md`](./05-Brute-Force-First.md)
