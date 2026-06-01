# 🌐 Cycle Detection

> *"Is there a loop? The answer differs for directed and undirected graphs."*

---

## I. UNDIRECTED GRAPHS

### DFS + parent
A cycle exists if DFS finds an already-visited neighbor that is NOT the parent.
```cpp
bool dfs(int u, int parent, vector<vector<int>>& adj, vector<bool>& vis) {
    vis[u] = true;
    for (int v : adj[u]) {
        if (!vis[v]) { if (dfs(v, u, adj, vis)) return true; }
        else if (v != parent) return true;   // back edge to non-parent ⟹ cycle
    }
    return false;
}
```

### Union-Find
For each edge (u,v): if find(u) == find(v), adding it forms a cycle; else unite. O(E·α). Great for incremental edge addition. (See [`../04-DATA-STRUCTURES-UNIVERSE/32-Disjoint-Set-Union.md`](../04-DATA-STRUCTURES-UNIVERSE/32-Disjoint-Set-Union.md).)

---

## II. DIRECTED GRAPHS

### 3-color DFS ⭐
- WHITE (0) = unvisited, GRAY (1) = in current recursion stack, BLACK (2) = fully done.
- A **back edge** to a GRAY node ⟹ cycle.
```cpp
int color[N]; // 0=white,1=gray,2=black
bool dfs(int u, vector<vector<int>>& adj) {
    color[u] = 1; // gray
    for (int v : adj[u]) {
        if (color[v] == 1) return true;            // back edge ⟹ cycle
        if (color[v] == 0 && dfs(v, adj)) return true;
    }
    color[u] = 2; // black
    return false;
}
```

### Kahn's (in-degree) ⟹ cycle if not all nodes processed
If a topological sort outputs fewer than n nodes, a cycle exists. (See [`03-Topological-Sort.md`](./03-Topological-Sort.md).)

---

## III. FINDING THE CYCLE (not just detecting)
Track the recursion stack / parent pointers; when a back edge is found, walk back to reconstruct the cycle vertices. ([CSES](https://cses.fi/problemset/) "Round Trip", "Round Trip II".)

---

## IV. SPECIAL: FUNCTIONAL GRAPHS (each node out-degree 1)
"a[i] → next[i]" forms a functional graph. Cycle detection via:
- **Floyd's tortoise & hare** (O(1) space) — also for linked-list cycles (LC 141/142).
- Coloring / visited timestamps.
Used in: detecting cycles in "next pointer" arrays, find-the-duplicate (LC 287).

---

## V. NEGATIVE CYCLES (weighted)
Use **Bellman-Ford**: after V−1 relaxations, if any edge still relaxes, a negative cycle is reachable. (See [`06-Shortest-Paths.md`](./06-Shortest-Paths.md).) Application: currency arbitrage.

---

## VI. APPLICATIONS
- Deadlock detection (resource graphs)
- Detecting circular dependencies (builds, imports)
- Validating DAGs before topo sort / DAG DP
- Find duplicate number (LC 287, functional graph)
- Negative cycle / arbitrage detection

---

## VII. COMPLEXITY
- DFS-based: O(V+E)
- Union-Find (undirected): O(E·α)
- Bellman-Ford (negative): O(V·E)

---

## VIII. PROBLEMS
- Course Schedule (207) — directed cycle check
- Detect Cycle in Undirected/Directed Graph (GfG)
- Find the Duplicate Number (287) — Floyd's on functional graph
- Linked List Cycle I/II (141/142)
- Find Eventual Safe States (802)
- CSES "Round Trip", "Round Trip II", "Cycle Finding" (negative)

---

**→ Next:** [`05-Connected-Components.md`](./05-Connected-Components.md)
