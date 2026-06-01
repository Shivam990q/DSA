# 🌐 Lowest Common Ancestor (LCA)

> *"For two nodes in a tree, find their deepest common ancestor — in O(log n) per query."*

---

## I. THE PROBLEM
Given a rooted tree, for queries (u, v) find their **lowest common ancestor**: the deepest node that is an ancestor of both. Foundation for tree path queries (distance, path aggregates).

---

## II. BINARY LIFTING ⭐ (most common)
Precompute `up[v][k]` = the 2^k-th ancestor of v.
```cpp
int LOG; vector<vector<int>> up; vector<int> depth;
void dfs(int u, int p, vector<vector<int>>& adj) {
    up[u][0] = p;
    for (int k = 1; k < LOG; k++) up[u][k] = up[u][k-1] == -1 ? -1 : up[up[u][k-1]][k-1];
    for (int v : adj[u]) if (v != p) { depth[v] = depth[u] + 1; dfs(v, u, adj); }
}
int lca(int u, int v) {
    if (depth[u] < depth[v]) swap(u, v);
    int d = depth[u] - depth[v];
    for (int k = 0; k < LOG; k++) if ((d >> k) & 1) u = up[u][k];   // lift u up
    if (u == v) return u;
    for (int k = LOG-1; k >= 0; k--)
        if (up[u][k] != up[v][k]) { u = up[u][k]; v = up[v][k]; }
    return up[u][0];
}
```
Preprocess O(n log n), query O(log n).

---

## III. EULER TOUR + RMQ — O(1) query
Record the Euler tour (node sequence during DFS) and depths; LCA(u,v) = the node with minimum depth between u and v's tour positions → a **Range Minimum Query**. With a sparse table, O(n log n) build, **O(1) per query**.

---

## IV. DISTANCE & PATH QUERIES (the payoff) ⭐
- **Distance**: dist(u,v) = depth[u] + depth[v] − 2·depth[LCA(u,v)].
- **Kth ancestor**: binary lifting directly (jump by bits of k).
- **Path aggregates** (sum/max/min on the u-v path): combine with prefix sums on root-paths, or HLD/Euler-tour techniques.
- **Is u an ancestor of v?**: using tin/tout from DFS.

---

## V. OFFLINE: TARJAN'S LCA
If all queries are known in advance, **Tarjan's offline LCA** (DFS + Union-Find) answers all in near-linear O((n+q)·α). Great when online queries aren't required.

---

## VI. APPLICATIONS
- Tree distance queries
- Path sum/max/min (with prefix sums or HLD)
- Finding meeting points / common ancestors
- Auxiliary trees / virtual trees
- Many tree DP and query problems

---

## VII. COMPLEXITY
| Method | Preprocess | Query |
|--------|-----------|-------|
| Binary lifting | O(n log n) | O(log n) |
| Euler tour + sparse table | O(n log n) | O(1) |
| Tarjan offline | O((n+q)·α) | amortized |

---

## VIII. PROBLEMS
- LCA of Binary Tree (LC 236), of BST (LC 235)
- Kth Ancestor of a Tree Node (LC 1483) — binary lifting ⭐
- Tree distance / path queries
- [CSES](https://cses.fi/problemset/) "Company Queries I/II", "Distance Queries", "Distinct Colors"
- CF problems tagged "trees" + "binary lifting"

---

**→ Next:** [`17-HLD-Centroid.md`](./17-HLD-Centroid.md)
