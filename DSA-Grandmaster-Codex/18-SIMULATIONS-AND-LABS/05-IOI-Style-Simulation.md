# 🥇 IOI-Style Simulation

> *"Five hours. Three problems. Subtask scoring. The olympiad gauntlet."*

---

## I. THE FORMAT
- 2 days × 5 hours, 3 problems per day
- Each problem: 100 points
- **Subtask scoring**: partial credit for solving easier constraint versions

---

## II. SIMULATE
- Pick past IOI problems ([oi.uz](https://oi.uz), ioi contest archive)
- 5h timer, 3 problems
- Aim to maximize TOTAL points across all 3

---

## III. THE SUBTASK STRATEGY
This is the IOI-specific skill. Each problem has subtasks:
- Subtask 1: tiny constraints (n ≤ 10) → brute force → easy points
- Subtask 2: small (n ≤ 1000) → O(n²) → more points
- Subtask 3: full (n ≤ 10⁵) → optimal → full points

**Strategy**: grab easy subtask points across ALL THREE problems before attempting any full solution.

```
Min 0-20:   Read all 3; identify subtasks
Min 20-120: Solve easy subtasks of all 3 (secure baseline points)
Min 120-280: Push hardest subtasks of the problems you understand best
Min 280-300: Verify; ensure subtask solutions still pass
```

---

## IV. THE POINT-MAXIMIZATION MINDSET
Unlike ICPC (binary: solve or not), IOI rewards partial progress. A 40-point partial on each of 3 problems (120) beats a single 100-point full solution.

---

## V. POST-SIMULATION
- Which subtasks did I miss that were easy?
- Did I leave points on the table by tunnel-visioning?
- Upsolve full solutions over the next days.

---

## VI. RESOURCES
- **oi.uz** — IOI + national olympiad problems
- **[USACO Guide](https://usaco.guide)** — mirrors IOI training curriculum
- **[USACO](https://www.usaco.org) contests** (free, monthly, subtask-style)
- Past IOI problems with official solutions

---

**→ Next:** [`06-System-Design-Simulation.md`](./06-System-Design-Simulation.md)
