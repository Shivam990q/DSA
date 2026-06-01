# 🌐 Heavy-Light Decomposition & Centroid Decomposition

> *"Two ways to break a tree into manageable pieces for fast path/subtree queries."*

---

## I. HEAVY-LIGHT DECOMPOSITION (HLD) ⭐
Decompose a tree into vertical **chains** such that any root-to-node path crosses **O(log n) chains**. Lay each chain contiguously in an array, build a **segment tree** over it → path/subtree queries in O(log² n).

### How
- For each node, its **heavy child** = the child with the largest subtree; the edge to it is "heavy." Other edges are "light."
- Following heavy edges forms chains. Any path goes through O(log n) light edges (each light edge at least halves the subtree).

### Operations (O(log² n))
- **Path query/update** (sum/max/min/assign on the path u→v)
- **Subtree query/update** (using the Euler/positional ordering)

Combine with a **Lazy Segment Tree** ([`../19-TEMPLATES-AND-IMPLEMENTATIONS/segment-tree-lazy.cpp`](../19-TEMPLATES-AND-IMPLEMENTATIONS/segment-tree-lazy.cpp)) to support range updates on paths.

---

## II. CENTROID DECOMPOSITION ⭐
The **centroid** of a tree is a node whose removal leaves subtrees each of size ≤ n/2. Recursively decompose: pick the centroid, recurse on each resulting subtree. The recursion has **O(log n) depth**, and each node belongs to O(log n) levels.

### Why it helps
Every path in the tree passes through the centroid of some level. So "count/aggregate paths with property X" can be solved by, at each centroid, considering paths that pass through it (combining contributions from different subtrees).

### Operations
- Count paths with length / weight ≤ k
- "Distance to nearest marked node" with updates
- Path-counting problems on trees

O(n log n) or O(n log² n) typically.

---

## III. HLD vs CENTROID — WHICH?
| Need | Use |
|------|-----|
| Path queries/updates with a segment tree (sum/max on path) | **HLD** |
| Counting/aggregating paths through a node, distance problems | **Centroid Decomposition** |
| Static path queries (no updates) | LCA + prefix sums (simpler) |

---

## IV. EULER TOUR (the simpler cousin)
For **subtree** queries (not path), flatten the tree via an Euler tour so each subtree is a contiguous range → a plain segment tree/BIT handles subtree sum/update in O(log n). Often enough when you only need subtree (not path) operations.

---

## V. COMPLEXITY
| Technique | Build | Query |
|-----------|-------|-------|
| Euler tour + segtree (subtree) | O(n) | O(log n) |
| HLD + segtree (path) | O(n) | O(log² n) |
| Centroid decomposition | O(n log n) | varies |

---

## VI. APPLICATIONS
- Path sum/max/min/assign with updates (HLD)
- Subtree aggregates with updates (Euler tour)
- Distance/path-counting problems (centroid)
- LCA (HLD gives LCA as a byproduct)
- Network/tree query problems in CP

---

## VII. PROBLEMS
- Path queries on trees ([CSES](https://cses.fi/problemset/) "Path Queries", "Subtree Queries")
- CF problems tagged "trees" + "data structures"
- "Count paths with length ≤ k" (centroid)
- Hard tree query problems (ICPC/CF Div 1)

---

## VIII. NOTE
Both are Level 7 (elite CP). Prerequisites: segment trees + LCA. Start with Euler tour (subtree), then HLD (path), then centroid (path counting). Use tested templates; the indexing is error-prone.

---

**→ Next:** [`18-Dynamic-Graphs.md`](./18-Dynamic-Graphs.md)
