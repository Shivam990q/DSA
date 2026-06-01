# 🌐 Topological Sort

> *"Order tasks so every prerequisite comes before its dependent. Only works on DAGs."*

---

## I. WHAT & WHEN
A **topological order** of a directed acyclic graph (DAG) is a linear ordering of vertices where every edge u→v has u before v.
- Exists **iff** the graph is a DAG (no cycles).
- Used for: scheduling with dependencies, build systems, course prerequisites, DAG DP.

---

## II. KAHN'S ALGORITHM (BFS-based) ⭐
Repeatedly remove nodes with in-degree 0.
```cpp
vector<int> topoSort(int n, vector<vector<int>>& adj) {
    vector<int> indeg(n, 0);
    for (int u = 0; u < n; u++) for (int v : adj[u]) indeg[v]++;
    queue<int> q;
    for (int i = 0; i < n; i++) if (indeg[i] == 0) q.push(i);
    vector<int> order;
    while (!q.empty()) {
        int u = q.front(); q.pop(); order.push_back(u);
        for (int v : adj[u]) if (--indeg[v] == 0) q.push(v);
    }
    return order.size() == (size_t)n ? order : vector<int>{}; // empty ⟹ cycle
}
```
**Bonus**: if `order.size() < n`, the graph has a CYCLE — Kahn's doubles as cycle detection.

---

## III. DFS-BASED TOPOLOGICAL SORT
Post-order DFS; push each node after exploring its descendants; reverse the result.
```cpp
void dfs(int u, vector<vector<int>>& adj, vector<bool>& vis, vector<int>& order) {
    vis[u] = true;
    for (int v : adj[u]) if (!vis[v]) dfs(v, adj, vis, order);
    order.push_back(u);
}
// after all: reverse(order)
```

---

## IV. LEXICOGRAPHICALLY SMALLEST TOPO ORDER
Use Kahn's with a **min-heap** instead of a queue → always pick the smallest available node. (e.g., "smallest valid build order.")

---

## V. TOPO SORT + DP ⭐
Once in topological order, you can DP along the DAG:
- **Longest/shortest path in a DAG**
- **Counting paths**
- **Parallel Courses (LC 1136, 2050)**: minimum semesters = longest chain.

(See [`../06-DYNAMIC-PROGRAMMING-UNIVERSE/11-Graph-DP-DAG.md`](../06-DYNAMIC-PROGRAMMING-UNIVERSE/11-Graph-DP-DAG.md).)

---

## VI. APPLICATIONS
- Course scheduling / prerequisites
- Build systems (make, package managers resolving dependencies)
- Spreadsheet cell recalculation order
- Task scheduling with dependencies
- Compiler instruction scheduling
- Detecting cycles in directed graphs

---

## VII. CYCLE DETECTION CONNECTION
- Kahn's: if fewer than n nodes are output, a cycle exists.
- DFS: a "back edge" (to a node currently in the recursion stack) means a cycle. See [`04-Cycle-Detection.md`](./04-Cycle-Detection.md).

---

## VIII. COMPLEXITY
O(V + E) for both Kahn's and DFS-based.

---

## IX. PROBLEMS
- Course Schedule (207) — can all be finished? (cycle check)
- Course Schedule II (210) — return an order ⭐
- Alien Dictionary (269) — derive letter order, then topo sort ⭐
- Parallel Courses (1136, 2050) — longest chain
- Sequence Reconstruction (444), Sort Items by Groups (1203)
- Find All Possible Recipes (2115)
- [CSES](https://cses.fi/problemset/) "Course Schedule", "Longest Flight Route", "Game Routes"

---

**→ Next:** [`04-Cycle-Detection.md`](./04-Cycle-Detection.md)
