# 🌐 Connected Components

> *"How many separate pieces does this graph have? Which nodes belong together?"*

---

## I. UNDIRECTED: CONNECTED COMPONENTS
A connected component is a maximal set of mutually reachable vertices.

### Via DFS/BFS
Run DFS/BFS from each unvisited node; each launch = one component.
```cpp
int components = 0;
for (int i = 0; i < n; i++)
    if (!vis[i]) { dfs(i, adj, vis); components++; }
```
O(V+E).

### Via Union-Find ⭐
Unite every edge's endpoints; number of components = number of distinct roots. Ideal when edges arrive incrementally / online.
```cpp
DSU dsu(n);
for (auto [u, v] : edges) dsu.unite(u, v);
// dsu.components = answer
```

---

## II. DIRECTED: STRONGLY CONNECTED COMPONENTS (SCC)
In directed graphs, "connected" splits into:
- **Strongly connected**: u→v AND v→u paths exist (mutual reachability).
- SCCs are found with **Tarjan's** or **Kosaraju's** in O(V+E). See [`09-SCC.md`](./09-SCC.md).
- **Weakly connected**: connected if you ignore edge directions (use plain DFS/Union-Find on the undirected version).

---

## III. GRID COMPONENTS (very common)
Cells connected to adjacent same-type cells:
- **Number of Islands (LC 200)**, **Max Area of Island (LC 695)**, **Number of Closed Islands (LC 1254)**.
- Flood-fill each unvisited land cell; count launches.

---

## IV. DYNAMIC CONNECTIVITY
- **Incremental (only adding edges)**: Union-Find, O(α) per op.
- **With deletions / fully dynamic**: harder — Link-Cut Trees, Euler Tour Trees, or offline divide-and-conquer on time. See [`18-Dynamic-Graphs.md`](./18-Dynamic-Graphs.md).
- **Offline (queries known in advance)**: "small-to-large" or DSU with rollback on a segment tree of time.

---

## V. RELATED CONCEPTS
- **Bridges & articulation points**: edges/vertices whose removal increases component count. See [`08-Bridges-Articulation.md`](./08-Bridges-Articulation.md).
- **Biconnected components**: maximal subgraphs with no articulation point.
- **2-edge-connected components**: stay connected after removing any single edge.

---

## VI. APPLICATIONS
- Counting clusters / regions
- Network connectivity ("are these computers connected?")
- Image segmentation (grid components)
- Friend circles / social network groups
- Accounts merge (LC 721) — group by shared emails (Union-Find)

---

## VII. COMPLEXITY
- DFS/BFS: O(V+E)
- Union-Find: O(E·α(V)) ≈ O(E)

---

## VIII. PROBLEMS
- Number of Provinces (547), Number of Connected Components (323)
- Number of Islands (200), Max Area of Island (695)
- Accounts Merge (721), Redundant Connection (684)
- Number of Operations to Make Network Connected (1319)
- Graph Valid Tree (261), Satisfiability of Equality Equations (990)
- [CSES](https://cses.fi/problemset/) "Building Roads", "Building Teams" (bipartite components)

---

**→ Next:** [`06-Shortest-Paths.md`](./06-Shortest-Paths.md)
