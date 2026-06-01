# 🧠 The Mental Models Compendium

> *"The grandmaster has 50 mental models. The amateur has 5. The difference is invisible until problems arrive."*

---

## 01 — DIVIDE THINKING

**Worldview**: every complex problem is solvable as the combination of solutions to two (or more) simpler problems.

**Triggers**:
- "Can I split the input in half?"
- "Can I separate cases into independent groups?"
- "Can I solve sub-problem A and sub-problem B separately, then merge?"

**Manifestations**: merge sort, binary search, FFT, Strassen, closest pair, divide-and-conquer DP.

---

## 02 — RECURSIVE THINKING

**Worldview**: a problem's solution often *contains* the solution to a smaller version of itself.

**Triggers**:
- "What if the input were one element smaller?"
- "Trees, lists, and self-similar structures"
- "Backtracking: try, recurse, undo"

**Manifestations**: tree traversal, backtracking, DP, divide-and-conquer.

---

## 03 — GRAPH THINKING

**Worldview**: any problem about discrete objects with relations is a graph problem.

**Triggers**:
- Things connected to other things
- States that can transition to other states
- Dependencies, prerequisites, hierarchies
- Networks, friends, paths, flows

**Manifestations**: BFS, DFS, shortest path, MST, matching, flow.

> Example: "Word Ladder" — words are vertices, edges are 1-letter changes. Shortest path = BFS.
> Example: "Course Schedule" — courses are vertices, prereqs are edges. Topological sort.
> Example: "Sudoku" — assignments are states; transitions are filling cells. Backtracking on state graph.

---

## 04 — DP THINKING

**Worldview**: future decisions depend only on a finite "state" — the rest of history is irrelevant.

**Triggers**:
- "Number of ways to..." (counting)
- "Min/max cost / length / sum..."
- "Longest / shortest..."
- "Match/transform A to B"

**Manifestations**: 1D DP, 2D DP, knapsack, LIS/LCS, edit distance, interval DP, tree DP, bitmask DP.

---

## 05 — GREEDY THINKING

**Worldview**: at each step, the locally best choice extends to the globally best solution (provably).

**Triggers**:
- "Sort by ..."
- "Pick the smallest/largest first"
- "Earliest deadline / shortest job first"

**Manifestations**: activity selection, Huffman, Kruskal, Dijkstra, scheduling.

**Critical**: requires proof. Always.

---

## 06 — MATHEMATICAL THINKING

**Worldview**: many problems have closed-form, formulaic, or structurally elegant solutions.

**Triggers**:
- Number theory: GCD, primes, modular arithmetic
- Combinatorics: count cleverly
- Linear algebra: matrices for linear recurrences
- Probability: expected values, linearity

**Manifestations**: combinatorial counting, modular nCr, matrix exp, FFT, generating functions.

---

## 07 — OPTIMIZATION THINKING

**Worldview**: every brute force has redundancy. Eliminate it. Replace expensive with cheap. Trade memory for time (or vice versa).

**Triggers**:
- "This recomputes the same thing" → memoize
- "This searches linearly" → hash / binary search
- "This re-checks all pairs" → two pointers / monotonic structure

**Manifestations**: every step from O(n³) → O(n²) → O(n log n) → O(n).

---

## 08 — STATE THINKING

**Worldview**: the system at any moment is fully described by its **state**. Find the minimal sufficient state.

**Triggers**:
- "What information determines future decisions?"
- "Is the state Markov?"
- "Can I compress the state?"

**Manifestations**: DP states, BFS on state graph, simulation.

---

## 09 — SYSTEMS THINKING

**Worldview**: the whole emerges from interactions. Optimize the system, not the parts.

**Triggers**:
- "What's the bottleneck?"
- "What latency / throughput?"
- "Where is contention?"

**Manifestations**: production engineering, distributed systems, performance optimization.

---

## 10 — PROBABILISTIC THINKING

**Worldview**: deterministic answers might be hard. Randomness can be a tool.

**Triggers**:
- "Adversarial worst case is rare in practice"
- "Use randomness to break symmetry"
- "Approximate with bounded error"

**Manifestations**: randomized quicksort, Monte Carlo, Las Vegas, probabilistic data structures.

---

## 11 — GEOMETRIC THINKING

**Worldview**: many problems live in space. Coordinates, distances, angles, areas matter.

**Triggers**:
- 2D / 3D coordinates
- Polygons, lines, circles
- Distances, intersections

**Manifestations**: convex hull, sweep line, KD-tree, computational geometry.

---

## 12 — ALGEBRAIC THINKING

**Worldview**: structure imposes constraints. Equations express constraints. Solving = manipulating algebra.

**Triggers**:
- Symmetries
- Invariants
- Group/monoid structure
- Linear systems

**Manifestations**: invariant arguments, group theory in games, linear algebra, polynomial methods.

---

## 13 — THE 30 META-MENTAL MODELS

(Drawn from a synthesis of grandmaster thinking)

1. **Brute force first** — always.
2. **Constraints whisper algorithms** — read them.
3. **Pattern recognition** — compressed experience.
4. **First principles** — derive, never memorize.
5. **The bottleneck dictates optimization**.
6. **Hidden monotonicity → binary search**.
7. **Hidden invariant → proof tool**.
8. **Hidden structure → algorithmic shortcut**.
9. **Symmetries simplify**.
10. **Edge cases are where lazy minds die**.
11. **Stress test before submit**.
12. **Editorial reading is research**.
13. **Upsolving is where learning happens**.
14. **One language deeply > five superficially**.
15. **Templates are tools, not crutches**.
16. **Sleep is preprocessing**.
17. **Compete only with yesterday-you**.
18. **The grandmaster is the beginner who never stopped beginning**.
19. **State your invariant; prove your invariant**.
20. **Practice patterns you avoid**.
21. **Teach to learn**.
22. **Build, don't just consume**.
23. **Show, don't tell — code, don't talk**.
24. **Embrace the suck**.
25. **Detach from outcomes; marry the practice**.
26. **The complement is often easier**.
27. **Sort, and order brings clarity**.
28. **Coordinate compress, and infinity becomes finite**.
29. **Linearity of expectation is magic**.
30. **The algorithm with the fewest moving parts is usually correct**.

---

**→ Next:** [`../17-EXECUTION-SYSTEMS/`](../17-EXECUTION-SYSTEMS/)
