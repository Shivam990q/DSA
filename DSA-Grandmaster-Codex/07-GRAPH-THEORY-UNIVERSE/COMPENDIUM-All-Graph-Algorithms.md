# 🌐 The Complete Graph Algorithms Compendium

> Every graph algorithm, in one place. Code, complexity, when to use.

---

## 01 — GRAPH FOUNDATIONS

### Representations

```cpp
// Adjacency list (most common)
vector<vector<int>> adj(n);
adj[u].push_back(v); adj[v].push_back(u);  // undirected

// Weighted
vector<vector<pair<int,int>>> adj(n);  // {to, weight}
adj[u].push_back({v, w});

// Adjacency matrix (dense graphs only)
vector<vector<int>> mat(n, vector<int>(n, 0));
mat[u][v] = w;

// Edge list (for Kruskal's)
vector<tuple<int, int, int>> edges;  // {weight, u, v}
```

### Memory
- Adjacency list: O(V + E)
- Adjacency matrix: O(V²)
- Edge list: O(E)

---

## 02 — BFS

```cpp
vector<int> bfs(int src, int n, vector<vector<int>>& adj) {
    vector<int> dist(n, -1);
    queue<int> q;
    dist[src] = 0; q.push(src);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }
    return dist;
}
```

**Use**: shortest path in unweighted graph, level-order, multi-source.

**Complexity**: O(V + E).

---

## 03 — DFS

```cpp
vector<bool> visited;
void dfs(int u, vector<vector<int>>& adj) {
    visited[u] = true;
    for (int v : adj[u]) if (!visited[v]) dfs(v, adj);
}
```

**Iterative DFS** (avoids stack overflow):
```cpp
void dfsIter(int src, vector<vector<int>>& adj) {
    stack<int> stk; stk.push(src);
    while (!stk.empty()) {
        int u = stk.top(); stk.pop();
        if (visited[u]) continue;
        visited[u] = true;
        for (int v : adj[u]) if (!visited[v]) stk.push(v);
    }
}
```

**Uses**: connected components, cycle detection, topological sort, bridges, SCC.

---

## 04 — TOPOLOGICAL SORT

### Kahn's Algorithm (BFS-based)
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
    return order.size() == n ? order : vector<int>{};  // empty if cycle
}
```

### DFS-based (post-order reversed)
```cpp
void topoDFS(int u, vector<vector<int>>& adj, vector<bool>& visited, vector<int>& order) {
    visited[u] = true;
    for (int v : adj[u]) if (!visited[v]) topoDFS(v, adj, visited, order);
    order.push_back(u);
}
// reverse(order)
```

**Use**: course schedule, build order, alien dictionary.

---

## 05 — CYCLE DETECTION

### Undirected (DFS + parent)
```cpp
bool hasCycle(int u, int parent, vector<vector<int>>& adj, vector<bool>& visited) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) {
            if (hasCycle(v, u, adj, visited)) return true;
        } else if (v != parent) return true;
    }
    return false;
}
```

### Directed (3-color DFS)
- White (0): not visited
- Gray (1): in current DFS stack
- Black (2): fully processed

If we encounter a gray vertex → back edge → cycle.

---

## 06 — DIJKSTRA

```cpp
vector<long long> dijkstra(int src, int n, vector<vector<pair<int,int>>>& adj) {
    vector<long long> dist(n, LLONG_MAX);
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    dist[src] = 0;
    pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```

**Complexity**: O((V + E) log V).
**Constraint**: non-negative edge weights.

---

## 07 — BELLMAN-FORD

```cpp
vector<long long> bellmanFord(int src, int n, vector<tuple<int,int,int>>& edges) {
    vector<long long> dist(n, LLONG_MAX);
    dist[src] = 0;
    for (int i = 0; i < n - 1; i++) {
        for (auto [u, v, w] : edges) {
            if (dist[u] != LLONG_MAX && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
            }
        }
    }
    // Detect negative cycle: one more pass
    for (auto [u, v, w] : edges) {
        if (dist[u] != LLONG_MAX && dist[u] + w < dist[v]) {
            // negative cycle exists
        }
    }
    return dist;
}
```

**Complexity**: O(V × E).
**Use**: graphs with negative edges; detect negative cycles.

---

## 08 — FLOYD-WARSHALL

```cpp
vector<vector<long long>> floydWarshall(int n, vector<vector<long long>>& mat) {
    auto d = mat;
    for (int k = 0; k < n; k++)
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (d[i][k] + d[k][j] < d[i][j])
                    d[i][j] = d[i][k] + d[k][j];
    return d;
}
```

**Complexity**: O(V³).
**Use**: all-pairs shortest paths, transitive closure.

---

## 09 — 0-1 BFS

For graphs where edges are 0 or 1.

```cpp
vector<int> zeroOneBFS(int src, int n, vector<vector<pair<int,int>>>& adj) {
    vector<int> dist(n, INT_MAX);
    deque<int> dq;
    dist[src] = 0;
    dq.push_front(src);
    while (!dq.empty()) {
        int u = dq.front(); dq.pop_front();
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                if (w == 0) dq.push_front(v);
                else dq.push_back(v);
            }
        }
    }
    return dist;
}
```

**Complexity**: O(V + E).

---

## 10 — KRUSKAL'S MST

```cpp
long long kruskal(int n, vector<tuple<int,int,int>>& edges) {
    sort(edges.begin(), edges.end());  // by weight
    DSU dsu(n);
    long long total = 0;
    for (auto [w, u, v] : edges) {
        if (dsu.unite(u, v)) total += w;
    }
    return total;
}
```

**Complexity**: O(E log E).

---

## 11 — PRIM'S MST

```cpp
long long prim(int src, int n, vector<vector<pair<int,int>>>& adj) {
    vector<bool> inMST(n, false);
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    pq.push({0, src});
    long long total = 0;
    while (!pq.empty()) {
        auto [w, u] = pq.top(); pq.pop();
        if (inMST[u]) continue;
        inMST[u] = true;
        total += w;
        for (auto [v, ww] : adj[u]) if (!inMST[v]) pq.push({ww, v});
    }
    return total;
}
```

**Complexity**: O((V + E) log V).

---

## 12 — BRIDGES (Tarjan)

```cpp
int timer = 0;
vector<int> tin, low;
vector<bool> visited;
vector<pair<int,int>> bridges;

void dfsBridge(int u, int parent, vector<vector<int>>& adj) {
    visited[u] = true;
    tin[u] = low[u] = timer++;
    for (int v : adj[u]) {
        if (v == parent) continue;
        if (visited[v]) low[u] = min(low[u], tin[v]);
        else {
            dfsBridge(v, u, adj);
            low[u] = min(low[u], low[v]);
            if (low[v] > tin[u]) bridges.push_back({u, v});
        }
    }
}
```

**Complexity**: O(V + E).

---

## 13 — ARTICULATION POINTS

Similar to bridges, but condition: `low[v] >= tin[u]` AND u is not root (or root with > 1 child).

---

## 14 — STRONGLY CONNECTED COMPONENTS

### Tarjan's (single DFS)
Track disc/low; when low[u] == tin[u], pop stack to form SCC.

### Kosaraju's (two DFS)
1. DFS on original graph, push to stack in finish order.
2. Reverse graph.
3. DFS on reversed in stack pop order; each new tree = SCC.

**Complexity**: O(V + E).

---

## 15 — 2-SAT

Reduce to implication graph + SCC.
- For each clause (a ∨ b): add edges ¬a → b and ¬b → a.
- Compute SCCs.
- Satisfiable iff a and ¬a are NOT in the same SCC for any variable.
- Topological order of SCC condensation gives valid assignment.

**Complexity**: O(V + E).

---

## 16 — EULERIAN PATH/CIRCUIT (Hierholzer's)

**Eulerian circuit exists iff**: connected + every vertex has even degree (undirected) / in-deg = out-deg (directed).

**Eulerian path exists iff**: connected + exactly 2 vertices of odd degree (undirected) / one with out-in=1, one with in-out=1 (directed).

### Hierholzer's algorithm
```cpp
void euler(int u, vector<vector<int>>& adj, vector<int>& circuit) {
    while (!adj[u].empty()) {
        int v = adj[u].back(); adj[u].pop_back();
        // remove (u, v) from adj[v] too (undirected)
        euler(v, adj, circuit);
    }
    circuit.push_back(u);
}
// reverse(circuit)
```

**Complexity**: O(V + E).

---

## 17 — BIPARTITE CHECK

```cpp
bool isBipartite(int n, vector<vector<int>>& adj) {
    vector<int> color(n, -1);
    for (int s = 0; s < n; s++) {
        if (color[s] != -1) continue;
        queue<int> q; q.push(s); color[s] = 0;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : adj[u]) {
                if (color[v] == -1) { color[v] = 1 - color[u]; q.push(v); }
                else if (color[v] == color[u]) return false;
            }
        }
    }
    return true;
}
```

---

## 18 — BIPARTITE MATCHING (Kuhn's)

```cpp
vector<int> match;
bool tryKuhn(int u, vector<vector<int>>& adj, vector<bool>& used) {
    for (int v : adj[u]) {
        if (used[v]) continue;
        used[v] = true;
        if (match[v] == -1 || tryKuhn(match[v], adj, used)) {
            match[v] = u; return true;
        }
    }
    return false;
}

int maxMatching(int n, int m, vector<vector<int>>& adj) {
    match.assign(m, -1);
    int total = 0;
    for (int u = 0; u < n; u++) {
        vector<bool> used(m, false);
        if (tryKuhn(u, adj, used)) total++;
    }
    return total;
}
```

**Complexity**: O(V × E).

### Hopcroft-Karp: O(E × √V)
For bipartite matching with V, E up to 10⁵.

---

## 19 — MAX FLOW (Dinic's)

```cpp
struct Edge { int to, rev; long long cap; };
vector<vector<Edge>> graph;
vector<int> level, iter;

void addEdge(int from, int to, long long cap) {
    graph[from].push_back({to, (int)graph[to].size(), cap});
    graph[to].push_back({from, (int)graph[from].size() - 1, 0});
}

bool bfs(int s) {
    level.assign(graph.size(), -1);
    queue<int> q;
    level[s] = 0; q.push(s);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (auto& e : graph[u]) {
            if (e.cap > 0 && level[e.to] < 0) {
                level[e.to] = level[u] + 1;
                q.push(e.to);
            }
        }
    }
    return level.back() >= 0;
}

long long dfs(int u, int t, long long f) {
    if (u == t) return f;
    for (; iter[u] < (int)graph[u].size(); iter[u]++) {
        auto& e = graph[u][iter[u]];
        if (e.cap > 0 && level[u] < level[e.to]) {
            long long d = dfs(e.to, t, min(f, e.cap));
            if (d > 0) {
                e.cap -= d;
                graph[e.to][e.rev].cap += d;
                return d;
            }
        }
    }
    return 0;
}

long long dinic(int s, int t) {
    long long flow = 0;
    while (bfs(s)) {
        iter.assign(graph.size(), 0);
        long long f;
        while ((f = dfs(s, t, LLONG_MAX)) > 0) flow += f;
    }
    return flow;
}
```

**Complexity**: O(V² E). For unit-capacity networks: O(E √V).

### Min-cut = Max-flow theorem
Min s-t cut = max s-t flow.

### Bipartite matching via flow
Source → all left vertices (cap 1), left → right (per edge, cap 1), right → sink (cap 1). Max flow = max matching.

---

## 20 — LCA (Lowest Common Ancestor)

### Binary lifting (O(n log n) preprocess, O(log n) per query)

```cpp
int LOG;
vector<vector<int>> up;
vector<int> depth;

void dfs(int u, int p, vector<vector<int>>& adj) {
    up[u][0] = p;
    for (int k = 1; k < LOG; k++) up[u][k] = up[up[u][k-1]][k-1];
    for (int v : adj[u]) {
        if (v == p) continue;
        depth[v] = depth[u] + 1;
        dfs(v, u, adj);
    }
}

int lca(int u, int v) {
    if (depth[u] < depth[v]) swap(u, v);
    int diff = depth[u] - depth[v];
    for (int k = 0; k < LOG; k++) if ((diff >> k) & 1) u = up[u][k];
    if (u == v) return u;
    for (int k = LOG - 1; k >= 0; k--) {
        if (up[u][k] != up[v][k]) {
            u = up[u][k]; v = up[v][k];
        }
    }
    return up[u][0];
}
```

### Euler tour + RMQ (O(n log n) preprocess, O(1) per query — sparse table)

---

## 21 — HLD (Heavy-Light Decomposition)

Decompose tree into heavy chains. Path query in O(log² n) (or O(log n) with carefully crafted segtree).

(Implementation in `19-TEMPLATES-AND-IMPLEMENTATIONS/`)

---

## 22 — CENTROID DECOMPOSITION

Recursively pick centroid, recurse on subtrees. O(n log n) levels deep.

---

## 23 — DYNAMIC GRAPHS

For online edge insertions/deletions:
- Link-Cut Tree (Sleator-Tarjan) for trees
- HDT (Holm-Lichtenberg-Thorup) for general graphs: O(log² n) amortized

---

## 24 — PROBLEM CATALOG (TOP 50)

### BFS/DFS
1. Number of Islands (LC 200)
2. Surrounded Regions (LC 130)
3. Pacific Atlantic (LC 417)
4. Walls and Gates (LC 286)
5. Rotting Oranges (LC 994)
6. Word Ladder (LC 127)
7. Word Ladder II (LC 126)

### Topological
8. Course Schedule I, II (LC 207, 210)
9. Alien Dictionary (LC 269)
10. Find All Possible Recipes (LC 2115)
11. Sequence Reconstruction

### Shortest Path
12. Network Delay Time (LC 743) — Dijkstra
13. Cheapest Flights with K Stops (LC 787) — Bellman-Ford-like
14. Path with Minimum Effort (LC 1631) — Dijkstra
15. Swim in Rising Water (LC 778) — BS or Dijkstra
16. Min Cost to Reach Destination (LC 1928)

### Connected Components / DSU
17. Number of Provinces (LC 547)
18. Redundant Connection (LC 684)
19. Accounts Merge (LC 721)
20. Most Stones Removed (LC 947)
21. Number of Operations to Make Network Connected (LC 1319)
22. Smallest String With Swaps (LC 1202)

### MST
23. Min Cost to Connect All Points (LC 1584)
24. Critical and Pseudo-Critical Edges (LC 1489)
25. Optimize Water Distribution (LC 1168)

### Bridges/Articulation
26. Critical Connections (LC 1192)

### Bipartite
27. Possible Bipartition (LC 886)
28. Is Graph Bipartite (LC 785)

### Matching/Flow
29. Maximum Bipartite Matching
30. Project Selection
31. Minimum Vertex Cover

### Tree
32. Diameter of Tree
33. Sum of Distances in Tree (LC 834)
34. Tree Coloring
35. LCA queries

### Eulerian
36. Reconstruct Itinerary (LC 332)
37. Cracking the Safe (LC 753)

### Hard
38. Sliding Puzzle (LC 773) — BFS on states
39. Shortest Path Visiting All Nodes (LC 847) — BFS + bitmask
40. Maximum Number of Achievable Transfer Requests (LC 1601)
41. Race Car (LC 818)
42. Bus Routes (LC 815)

### CF / Competitive
43. [CSES](https://cses.fi/problemset/) Graph Problems (all)
44. CF "graphs" tag, 1500-2200

### Advanced
45. Maximum flow problems (CSES)
46. Min-cost flow
47. 2-SAT
48. SCC counting
49. Tarjan's bridges with queries
50. HLD path query problems

---

**→ Next universe:** [`../08-STRING-UNIVERSE/00-Index.md`](../08-STRING-UNIVERSE/00-Index.md)
