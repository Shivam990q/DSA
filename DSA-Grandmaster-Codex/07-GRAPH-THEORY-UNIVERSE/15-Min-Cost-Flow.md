# 🌐 Min-Cost Max-Flow (MCMF)

> *"Push the maximum flow — but at the cheapest possible total cost."*

---

## I. THE PROBLEM
A flow network where each edge has both a **capacity** and a **cost per unit flow**. Find the maximum flow from s to t with the **minimum total cost** (cost = Σ flow·cost over edges). Sometimes you want min cost for a SPECIFIC flow value, not necessarily max.

---

## II. THE ALGORITHM ⭐
Repeatedly augment flow along the **shortest (cheapest) path** in the residual graph:
1. Find the minimum-cost s→t path (Bellman-Ford/SPFA, since residual edges have negative costs).
2. Push as much flow as the bottleneck allows along it.
3. Repeat until no augmenting path (max flow) or desired flow reached.

### Johnson's potentials (Dijkstra speedup)
Negative residual costs prevent plain Dijkstra. Use **potentials** (reduced costs) so Dijkstra works after the first Bellman-Ford pass → faster MCMF.

---

## III. COMPLEXITY
Roughly O(flow · (V·E)) with SPFA, or O(flow · E log V) with potentials. Practical for moderate sizes; the flow value bounds iterations.

---

## IV. MODELING WITH MCMF ⭐
Many weighted assignment/transportation problems reduce to MCMF:
- **Assignment problem** (min-cost perfect matching): L→R edges with costs, capacities 1.
- **Transportation**: supplies → demands with per-unit shipping costs.
- **Min-cost to satisfy demands** subject to capacity constraints.
- **Weighted bipartite matching** (alternative to Hungarian).
- **Scheduling with costs**, **k disjoint paths of min total cost**.

The skill (as with max-flow) is the **reduction**: design a network where min-cost max-flow gives the answer.

---

## V. CONVEX COSTS
If an edge's cost is a convex function of flow (increasing marginal cost), split it into multiple parallel edges with increasing per-unit costs — MCMF naturally uses the cheaper ones first.

---

## VI. MCMF VS HUNGARIAN
For the assignment problem specifically:
- **Hungarian algorithm**: O(n³), specialized, often faster for dense complete bipartite.
- **MCMF**: more general (handles capacities, non-complete graphs, supplies/demands).

---

## VII. APPLICATIONS
- Optimal assignment (workers↔tasks with costs)
- Transportation / logistics (min shipping cost)
- Min-cost k-disjoint paths
- Some scheduling and resource-allocation problems
- Image processing (certain energy minimizations)

---

## VIII. COMPLEXITY SUMMARY
- SPFA-based: O(flow · V·E)
- Dijkstra + potentials: O(flow · E log V)

---

## IX. PROBLEMS
- Assignment problem / min-cost matching
- [CSES](https://cses.fi/problemset/) flow problems (advanced)
- CF/ICPC problems tagged "flows" with costs
- Transportation and logistics modeling

---

## X. NOTE
MCMF is Level 7 (elite CP). Build on max-flow ([`14-Network-Flow.md`](./14-Network-Flow.md)) first. Use a tested template; focus your effort on the MODELING (the reduction), which is the hard part.

---

**→ Next:** [`16-LCA.md`](./16-LCA.md)
