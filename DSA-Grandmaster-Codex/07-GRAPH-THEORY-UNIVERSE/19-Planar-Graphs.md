# 🌐 Planar Graphs

> *"Graphs you can draw on paper without edge crossings — with surprising special structure."*

---

## I. DEFINITION
A graph is **planar** if it can be drawn in the plane with no edges crossing. Such a drawing divides the plane into **faces** (regions).

---

## II. EULER'S FORMULA ⭐
For a connected planar graph: **V − E + F = 2** (vertices − edges + faces, including the outer face).

Consequences (simple connected planar graph, V ≥ 3):
- **E ≤ 3V − 6** (planar graphs are SPARSE — at most linear edges).
- If triangle-free: E ≤ 2V − 4.
- → Every planar graph has a vertex of degree ≤ 5.

---

## III. KURATOWSKI / WAGNER (characterization)
A graph is planar **iff** it contains no subdivision of **K₅** (complete graph on 5 vertices) or **K₃,₃** (complete bipartite 3×3) — Kuratowski's theorem. Wagner's gives the equivalent minor version.

---

## IV. PLANARITY TESTING
Determine if a graph is planar in **O(V)** (Hopcroft-Tarjan, or the simpler Boyer-Myrvold). These also produce a planar embedding if one exists. (Complex to implement; libraries exist.)

---

## V. WHY PLANARITY MATTERS
- **Sparsity**: E = O(V) → many algorithms run faster on planar graphs.
- **Separator theorem (Lipton-Tarjan)**: a planar graph has a separator of size O(√V) whose removal splits it into balanced parts → divide-and-conquer algorithms, faster shortest paths.
- **Four Color Theorem**: every planar graph is 4-colorable (famous result).
- Faster max-flow, shortest paths, and other problems have specialized planar algorithms.

---

## VI. APPLICATIONS
- **Maps & GIS** (road networks are nearly planar)
- **VLSI / circuit design** (avoiding wire crossings)
- **Graph drawing** (clean layouts)
- Specialized fast algorithms exploiting O(√V) separators

---

## VII. THE FOUR COLOR THEOREM
Every planar graph can be vertex-colored with **4 colors** so no adjacent vertices share a color. Proved in 1976 (Appel-Haken) — the first major theorem proved with computer assistance. (3-coloring planar graphs is NP-complete, interestingly.)

---

## VIII. DUAL GRAPH
The **dual** of a planar graph: one vertex per face; connect faces sharing an edge. Min-cut in the primal ↔ shortest path in the dual (for planar s-t cuts) — a beautiful duality used in planar max-flow.

---

## IX. CP/PRACTICAL NOTE
Planar-specific algorithms are mostly **advanced/research** (Level 8-9). In typical CP, you mainly use:
- The sparsity bound (E ≤ 3V−6) for complexity reasoning.
- Euler's formula for counting faces/regions.
- Occasionally the separator idea.

Full planarity testing/embedding is rarely needed in contests.

---

## X. PROBLEMS / CONCEPTS
- Counting regions formed by lines/segments (Euler's formula)
- Map coloring problems
- Problems where you reason "the graph is planar, so E = O(V)"
- Research: planar shortest paths, planar max-flow

---

**→ Back to:** [`00-Index.md`](./00-Index.md) | All algorithms with code → [`COMPENDIUM-All-Graph-Algorithms.md`](./COMPENDIUM-All-Graph-Algorithms.md)
