# 📐 Geometry Universe

> *"Geometry is mathematics walking in space."*

---

## 📚 Contents (all deep individual files + compendium)

1. [`01-Computational-Geometry-Foundations.md`](./01-Computational-Geometry-Foundations.md) — Points, vectors, cross/dot products, precision ⭐
2. [`02-Convex-Hull.md`](./02-Convex-Hull.md) — Andrew monotone chain, Graham scan, Jarvis
3. [`03-Line-Sweep.md`](./03-Line-Sweep.md) — Bentley-Ottmann, skyline, rectangle union, interval sweeps
4. [`04-Closest-Pair.md`](./04-Closest-Pair.md) — Divide & conquer, sweep line, grid bucketing
5. [`05-Polygon-Operations.md`](./05-Polygon-Operations.md) — Shoelace area, point-in-polygon, Pick's theorem
6. [`06-KD-Tree.md`](./06-KD-Tree.md) — Spatial nearest-neighbor & range queries
7. [`07-Voronoi-Delaunay.md`](./07-Voronoi-Delaunay.md) — Voronoi diagrams, Delaunay, EMST
8. [`08-COMPENDIUM-Geometry.md`](./08-COMPENDIUM-Geometry.md) ⭐ — all algorithms with code

### Mental Model
- [`../16-MENTAL-MODELS-AND-FRAMEWORKS/11-Geometric-Thinking.md`](../16-MENTAL-MODELS-AND-FRAMEWORKS/11-Geometric-Thinking.md)

---

## 🧭 LEARNING ORDER
Foundations (01) → Convex Hull (02) → Polygon Operations (05) → Line Sweep (03) → Closest Pair (04) → KD-Tree (06) → Voronoi/Delaunay (07, advanced)

---

## ⚠️ PRECISION FIRST
Geometry's #1 difficulty is floating-point error. Prefer integer arithmetic (cross products) when coordinates are integers; use EPS for floats. See Foundations §V.

---

## 📌 DEEP REFERENCE
- **de Berg et al.**, *Computational Geometry: Algorithms and Applications* ⭐
- **[CP-Algorithms.com](https://cp-algorithms.com)** — https://cp-algorithms.com/geometry/
