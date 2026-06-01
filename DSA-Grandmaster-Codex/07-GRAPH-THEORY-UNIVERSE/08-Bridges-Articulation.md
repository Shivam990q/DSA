# 🌐 Bridges & Articulation Points

> *"Which edges/vertices, if removed, break the graph apart? Tarjan's low-link reveals them."*

---

## I. DEFINITIONS
- **Bridge** (cut edge): an edge whose removal increases the number of connected components.
- **Articulation point** (cut vertex): a vertex whose removal increases the number of components.

These identify the "weak points" of a network.

---

## II. THE LOW-LINK IDEA (Tarjan) ⭐
DFS assigns each vertex:
- `tin[u]` = discovery time (when first visited)
- `low[u]` = the lowest `tin` reachable from u's DFS subtree using at most one back edge

```cpp
int timer = 0;
vector<int> tin, low; vector<bool> vis;
```

---

## III. BRIDGES
Edge (u, v) (v a DFS child of u) is a **bridge** iff `low[v] > tin[u]` — v's subtree can't reach u or above without this edge.
```cpp
void dfs(int u, int parent) {
    vis[u] = true; tin[u] = low[u] = timer++;
    for (int v : adj[u]) {
        if (v == parent) continue;
        if (vis[v]) low[u] = min(low[u], tin[v]);     // back edge
        else {
            dfs(v, u);
            low[u] = min(low[u], low[v]);
            if (low[v] > tin[u]) bridges.push_back({u, v});  // BRIDGE
        }
    }
}
```
O(V+E). (Handle multi-edges: distinguish by edge id, not parent vertex.)

---

## IV. ARTICULATION POINTS
Vertex u is an articulation point iff:
- u is the **DFS root** with ≥ 2 children, OR
- u is **non-root** and has a child v with `low[v] >= tin[u]` (v's subtree can't bypass u).

Same DFS, different condition.

---

## V. RELATED STRUCTURES
- **2-edge-connected components**: remove all bridges → the remaining components.
- **Biconnected components (BCC)**: maximal subgraphs with no articulation point; found with a similar DFS using an edge stack.
- **Bridge tree / block-cut tree**: contract 2-edge-connected components → a tree of bridges; powerful for path queries.

---

## VI. APPLICATIONS
- **Network reliability**: single points of failure (a bridge = a critical cable; an articulation point = a critical router).
- **Critical Connections (LC 1192)** — find all bridges.
- Redundancy planning (which links need backups).
- Bridge tree for queries about edge-disjoint paths.

---

## VII. COMPLEXITY
O(V + E), single DFS.

---

## VIII. PROBLEMS
- Critical Connections in a Network (LC 1192) ⭐ — bridges
- Find articulation points (GfG)
- [CSES](https://cses.fi/problemset/) "Necessary Roads" (bridges), "Necessary Cities" (articulation points)
- CF problems tagged "graphs" + "dfs and similar" / "trees"

---

## IX. NOTE
This is the gateway to Tarjan's family. The same low-link technique powers SCC (see [`09-SCC.md`](./09-SCC.md)). Master the low-link concept once; reuse everywhere. (Story: [`../15-CASE-STUDIES-LEGENDARY/09-The-Story-of-Tarjan.md`](../15-CASE-STUDIES-LEGENDARY/09-The-Story-of-Tarjan.md).)

---

**→ Next:** [`09-SCC.md`](./09-SCC.md)
