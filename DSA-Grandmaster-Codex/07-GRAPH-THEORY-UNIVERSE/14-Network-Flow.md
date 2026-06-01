# 🌐 Network Flow (Max Flow / Min Cut)

> *"How much can flow from source to sink? And what's the cheapest cut that stops it?"*

---

## I. THE PROBLEM
A flow network: directed graph with edge **capacities**, a source s and sink t. Find the maximum flow from s to t (respecting capacities and flow conservation at every other node).

---

## II. MAX-FLOW MIN-CUT THEOREM ⭐⭐
**The maximum s-t flow equals the minimum s-t cut** (the minimum total capacity of edges whose removal disconnects s from t). This duality is the heart of flow theory and powers countless reductions.

---

## III. FORD-FULKERSON / EDMONDS-KARP
Repeatedly find an **augmenting path** (s→t with available capacity) in the residual graph, push flow along it, update residuals. Stop when none remains.
- **Edmonds-Karp**: use BFS for shortest augmenting path → O(V·E²).

---

## IV. DINIC'S ALGORITHM ⭐ (the practical choice)
Phases: BFS builds a **level graph**, then DFS finds **blocking flows**. Much faster in practice.
- General: O(V²·E)
- **Unit-capacity networks** (e.g., bipartite matching): O(E·√V)
```cpp
// structure: level[] from BFS, iter[] for current-arc optimization in DFS
// (full template in CP libraries / KACTL)
```
Use Dinic's for almost all flow problems.

---

## V. MODELING WITH FLOW (the real skill) ⭐
Many problems reduce to max-flow / min-cut:
- **Bipartite matching**: s → L (cap 1), L → R (cap 1), R → t (cap 1). Max flow = max matching.
- **Vertex-disjoint paths**: split each vertex into in/out with cap 1.
- **Edge-disjoint paths**: unit capacities; max flow = number of disjoint paths (Menger's theorem).
- **Project selection / max-weight closure**: min-cut formulation.
- **Image segmentation**: min-cut.
- **Assignment with capacities**.

The art: turn the problem into a network where max-flow/min-cut gives the answer.

---

## VI. MIN-COST MAX-FLOW (MCMF)
Each edge also has a cost per unit flow. Find max flow of **minimum total cost**. Algorithm: repeatedly augment along the **shortest (cheapest) path** (Bellman-Ford/SPFA or Dijkstra with potentials). Used for: assignment problem, transportation, weighted matching.

---

## VII. PROJECT SELECTION (classic min-cut)
Choose projects (with profits) and required equipment (with costs) to maximize profit. Model as min-cut: source→projects (profit), equipment→sink (cost), project→equipment (∞). Answer = total profit − min cut.

---

## VIII. COMPLEXITY
| Algorithm | Time |
|-----------|------|
| Edmonds-Karp | O(V·E²) |
| Dinic's | O(V²·E), O(E√V) unit-cap |
| MCMF (SPFA) | O(V·E·flow) roughly |

---

## IX. PROBLEMS
- Maximum bipartite matching (via flow)
- [CSES](https://cses.fi/problemset/) "Download Speed" (max flow), "Police Chase" (min cut), "School Dance" (matching), "Distinct Routes" (edge-disjoint paths)
- Project selection, escape problems, image segmentation
- CF/ICPC problems tagged "flows"

---

## X. NOTE
Network flow is Level 7 (elite CP). The **modeling** (reducing a problem to flow) is harder than the algorithm. Master max-flow min-cut duality and the standard reductions. Use a tested Dinic's template.

---

**→ Next:** [`15-Min-Cost-Flow.md`](./15-Min-Cost-Flow.md)
