# 📖 IOI Legends: Mecho, Cake, and the Art of Subtasks

> *"IOI problems are sculptures: each subtask reveals more of the form."*

---

## I. "MECHO" (IOI 2007) — Binary Search on Answer + BFS
- **Problem**: A bear must reach home before bees (spreading from hives) reach it. Maximize eating time before fleeing.
- **Key idea**: binary search on "eating time"; for each candidate, BFS to check if the bear can reach home before the bees.
- **Pattern**: binary search on answer + BFS feasibility check.
- **Lesson**: "maximize X such that feasible" → binary search + a checker.

---

## II. "CAKE" / GAME PROBLEMS — Interval & Game DP
- Many IOI problems involve two players taking turns (game theory + DP).
- **Pattern**: minimax DP — `dp[i][j]` = best score difference the current player can achieve on segment [i, j].

---

## III. THE SUBTASK PHILOSOPHY
IOI grades by subtasks. A typical problem:
- Subtask 1 (n ≤ 10): brute force
- Subtask 2 (n ≤ 1000): O(n²)
- Subtask 3 (n ≤ 10⁵): O(n log n) optimal

**Strategy**: solve subtasks incrementally. Partial credit across all problems beats one full solution.

---

## IV. RECURRING IOI TECHNIQUES
1. Binary search on answer
2. DP (interval, tree, game)
3. Greedy with proof
4. Data structures (segment tree, BIT)
5. Graph algorithms
6. Clever observations (the "aha")

---

## V. THE IOI MINDSET
- Read all 3 problems; spot easy subtasks everywhere
- Secure baseline points before going deep
- The hardest subtask often needs ONE more observation than the previous

---

## VI. WHERE TO PRACTICE
- **[oi.uz](https://oi.uz)** — IOI + national olympiad archive
- **[USACO](https://www.usaco.org)** — free, subtask-style, monthly
- **[USACO Guide](https://usaco.guide)** — structured curriculum mirroring IOI

---

**→ Next:** [`04-IOI-Aliens-and-Beyond.md`](./04-IOI-Aliens-and-Beyond.md)
