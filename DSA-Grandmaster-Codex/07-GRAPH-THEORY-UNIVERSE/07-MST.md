# 🌐 Minimum Spanning Tree (MST)

> *"Connect all nodes at minimum total edge cost. Two greedy algorithms, both provably optimal."*

---

## I. THE PROBLEM
Given a connected weighted undirected graph, find a subset of edges that connects all vertices with **minimum total weight** and no cycles (a tree). It has exactly V−1 edges.

---

## II. KRUSKAL'S ALGORITHM ⭐ (edge-based greedy)
Sort edges by weight; add each edge if it doesn't form a cycle (use DSU).
```cpp
long long kruskal(int n, vector<tuple<int,int,int>>& edges) { // {w, u, v}
    sort(edges.begin(), edges.end());
    DSU dsu(n);
    long long total = 0; int used = 0;
    for (auto [w, u, v] : edges)
        if (dsu.unite(u, v)) { total += w; used++; }
    return used == n - 1 ? total : -1;  // -1 if disconnected
}
```
O(E log E). Needs DSU (see [`../04-DATA-STRUCTURES-UNIVERSE/32-Disjoint-Set-Union.md`](../04-DATA-STRUCTURES-UNIVERSE/32-Disjoint-Set-Union.md)).

---

## III. PRIM'S ALGORITHM (vertex-based greedy)
Grow the tree from a start vertex; repeatedly add the cheapest edge connecting tree to non-tree. Uses a min-heap.
```cpp
long long prim(int n, vector<vector<pair<int,int>>>& adj) {
    vector<bool> in(n, false);
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    pq.push({0, 0});
    long long total = 0; int cnt = 0;
    while (!pq.empty() && cnt < n) {
        auto [w, u] = pq.top(); pq.pop();
        if (in[u]) continue;
        in[u] = true; total += w; cnt++;
        for (auto [v, ww] : adj[u]) if (!in[v]) pq.push({ww, v});
    }
    return cnt == n ? total : -1;
}
```
O((V+E) log V). Better for dense graphs; Kruskal better for sparse / edge-list input.

---

## IV. WHY GREEDY WORKS — THE CUT PROPERTY
**Cut property**: for any partition of vertices into two sets, the minimum-weight edge crossing the cut is in SOME MST. Both Kruskal (safe edge across components) and Prim (cheapest edge leaving the tree) exploit this. (Exchange-argument proof.)

---

## V. BORŮVKA'S ALGORITHM
Each component simultaneously picks its cheapest outgoing edge; merge; repeat. O(E log V). Naturally parallelizable; basis for some advanced/parallel MST algorithms.

---

## VI. VARIANTS & APPLICATIONS
- **Min cost to connect all points (LC 1584)**: complete graph on points; MST. (Use Prim for dense.)
- **Second-best MST**: find MST, then for each non-tree edge consider swapping.
- **Critical & pseudo-critical edges (LC 1489)**: which edges appear in every / some MST.
- **Maximum spanning tree**: negate weights or sort descending.
- **Euclidean MST**: subset of Delaunay edges (see [`../10-GEOMETRY-UNIVERSE/07-Voronoi-Delaunay.md`](../10-GEOMETRY-UNIVERSE/07-Voronoi-Delaunay.md)).
- Clustering (cut the k−1 largest MST edges → k clusters).
- Network design (lay cable/roads at min cost).

---

## VII. KRUSKAL vs PRIM — WHICH?
| | Kruskal | Prim |
|-|---------|------|
| Best for | sparse graphs / edge list | dense graphs / adjacency |
| Needs | DSU + sorted edges | min-heap |
| Time | O(E log E) | O((V+E) log V) |

---

## VIII. COMPLEXITY
Both O(E log V) effectively. MST is always connected-graph; for disconnected input you get a minimum spanning FOREST.

---

## IX. PROBLEMS
- Min Cost to Connect All Points (1584) ⭐
- Connecting Cities With Minimum Cost (1135)
- Optimize Water Distribution (1168) — virtual node trick
- Find Critical and Pseudo-Critical Edges (1489)
- [CSES](https://cses.fi/problemset/) "Road Reparation", "Road Construction" (DSU)

---

**→ Next:** [`08-Bridges-Articulation.md`](./08-Bridges-Articulation.md)
