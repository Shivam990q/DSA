# 🎯 Branch and Bound

> *"Backtracking with a brain: prune any branch that can't beat the best found so far."*

---

## I. THE IDEA
Branch and bound = systematic search (like backtracking) + **bounding**. At each node of the search tree, compute an optimistic estimate (a **bound**) of the best achievable in that subtree. If the bound can't beat the current best solution, **prune** the entire subtree.

Used for **optimization** problems (find the best), especially NP-hard ones where brute force is too slow but exact answers are needed for moderate sizes.

---

## II. THE COMPONENTS
1. **Branching**: split the problem into subproblems (decisions).
2. **Bounding**: compute an upper bound (for maximization) or lower bound (for minimization) on each subproblem's best possible value.
3. **Pruning**: discard subproblems whose bound is worse than the incumbent (best found so far).
4. **Search order**: DFS (low memory) or best-first (explore the most promising bound first, often with a priority queue).

---

## III. BACKTRACKING vs BRANCH & BOUND ⭐
| | Backtracking | Branch & Bound |
|-|--------------|----------------|
| Goal | find solutions / feasibility | find OPTIMAL solution |
| Prunes by | validity constraints | bounds on the objective |
| Typical use | N-queens, sudoku, permutations | TSP, knapsack, integer programming |

Branch and bound is backtracking enhanced with objective-based pruning.

---

## IV. CLASSIC EXAMPLES

### 0/1 Knapsack (B&B)
At each item, branch take/skip. Bound = current value + fractional-knapsack estimate of the remaining capacity. Prune if bound ≤ best found.

### Traveling Salesman (exact B&B)
Branch over which city to visit next. Bound = current path cost + a lower bound on completing the tour (e.g., sum of minimum outgoing edges, or a 1-tree/MST-based bound). Prune partial tours exceeding the best.

### Integer / Mixed-Integer Programming
The workhorse of solvers (CPLEX, Gurobi): solve LP relaxations for bounds; branch on fractional variables.

### Job Assignment
Branch over assignments; bound via the cheapest remaining completion.

---

## V. THE BOUND QUALITY MATTERS ⭐
A **tighter bound prunes more** → faster. But computing a tighter bound costs more per node. The art is balancing bound quality vs computation cost. Common bounds: LP relaxation, greedy/fractional estimates, MST-based (for TSP).

---

## VI. SEARCH STRATEGY
- **DFS (depth-first B&B)**: low memory, finds a feasible solution fast (good incumbent for pruning).
- **Best-first (least-cost)**: priority queue ordered by bound; explores most promising first; more memory.
- Often: DFS to get a good incumbent quickly, then prune aggressively.

---

## VII. COMPLEXITY
Worst case still exponential (it's solving NP-hard problems exactly), but pruning makes it **practical for moderate sizes** far beyond naive brute force. No polynomial guarantee.

---

## VIII. WHEN TO USE
- Optimization (not just feasibility)
- NP-hard but you need the EXACT optimum
- Moderate input sizes where DP/bitmask is too large but pruned search is feasible
- When a good bounding function exists

For approximate answers on large instances, use approximation algorithms or heuristics instead (see [`COMPENDIUM-Advanced-Algorithms.md`](./COMPENDIUM-Advanced-Algorithms.md) §10).

---

## IX. PROBLEMS / CONTEXTS
- Exact TSP for moderate n
- 0/1 Knapsack when DP table is too big
- Integer programming, constraint optimization
- Puzzle optimization (e.g., optimal solutions to combinatorial puzzles)

---

**→ Next:** [`07-Two-Pointers-And-Sliding-Window.md`](./07-Two-Pointers-And-Sliding-Window.md)
