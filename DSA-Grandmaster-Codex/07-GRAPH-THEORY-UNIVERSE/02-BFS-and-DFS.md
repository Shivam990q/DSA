# 🌐 BFS & DFS — The Two Universal Traversals

> *"Every graph algorithm is a variation on two ideas: go wide, or go deep."*

---

## I. BFS (Breadth-First Search)
Explore level by level using a **queue**. First time you reach a node = shortest path (in edges) from the source.
```cpp
vector<int> bfs(int src, int n, vector<vector<int>>& adj) {
    vector<int> dist(n, -1);
    queue<int> q; q.push(src); dist[src] = 0;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u])
            if (dist[v] == -1) { dist[v] = dist[u] + 1; q.push(v); }
    }
    return dist;
}
```
**Key property**: BFS = shortest path in UNWEIGHTED graphs. O(V+E).

---

## II. DFS (Depth-First Search)
Go as deep as possible, then backtrack. Recursion or explicit stack.
```cpp
void dfs(int u, vector<vector<int>>& adj, vector<bool>& vis) {
    vis[u] = true;
    for (int v : adj[u]) if (!vis[v]) dfs(v, adj, vis);
}
```
**Iterative** (avoid stack overflow for large graphs):
```cpp
void dfsIter(int s, vector<vector<int>>& adj, vector<bool>& vis) {
    stack<int> st; st.push(s);
    while (!st.empty()) {
        int u = st.top(); st.pop();
        if (vis[u]) continue;
        vis[u] = true;
        for (int v : adj[u]) if (!vis[v]) st.push(v);
    }
}
```
O(V+E).

---

## III. WHAT EACH UNLOCKS
| BFS | DFS |
|-----|-----|
| Shortest path (unweighted) | Connected components |
| Level-order / layers | Cycle detection |
| Multi-source shortest dist | Topological sort |
| Bipartite check (2-coloring) | Bridges & articulation points |
| Min steps in state graph | Strongly connected components |
| Shortest path in grids | Tree DP / Euler tour |

---

## IV. MULTI-SOURCE BFS ⭐
Start BFS from MANY sources at once (push all into the queue with dist 0). Computes, for every cell, the distance to the NEAREST source.
- **Rotting Oranges (LC 994)**, **01 Matrix (LC 542)**, **Walls and Gates (LC 286)**.

---

## V. BFS/DFS ON GRIDS
Treat each cell as a node, edges to 4 (or 8) neighbors. Use direction arrays:
```cpp
int dx[] = {0,0,1,-1}, dy[] = {1,-1,0,0};
```
- **Number of Islands (LC 200)**, **Flood Fill (LC 733)**, **Surrounded Regions (LC 130)**.

---

## VI. BFS ON IMPLICIT STATE GRAPHS ⭐
The "node" can be an abstract state:
- **Word Ladder (LC 127)**: nodes = words, edges = 1-letter changes.
- **Open the Lock (LC 752)**: nodes = lock states.
- **Sliding Puzzle (LC 773)**: nodes = board configurations.
- **Minimum Knight Moves (LC 1197)**: nodes = chess positions.
- State augmentation: `(cell, obstacles_removed)` for **Shortest Path with Obstacle Elimination (LC 1293)**.

---

## VII. 0-1 BFS (preview)
If edges have weights 0 or 1, replace the queue with a **deque** (push-front for 0, push-back for 1) → shortest path in O(V+E). See [`06-Shortest-Paths.md`](./06-Shortest-Paths.md).

---

## VIII. DFS EDGE CLASSIFICATION (for directed graphs)
- **Tree edge**: to an unvisited node
- **Back edge**: to an ancestor (in stack) → indicates a CYCLE
- **Forward / Cross edge**: other cases
This classification powers cycle detection, bridges, and SCC. See [`04-Cycle-Detection.md`](./04-Cycle-Detection.md), [`09-SCC.md`](./09-SCC.md).

---

## IX. COMPLEXITY
Both O(V + E) time, O(V) space (queue/stack + visited).
⚠️ For V up to 10⁵-10⁶, prefer **iterative DFS** or raise recursion limit.

---

## X. PROBLEMS
- Number of Islands (200), Flood Fill (733), Rotting Oranges (994), 01 Matrix (542)
- Word Ladder (127), Open the Lock (752), Sliding Puzzle (773)
- Clone Graph (133), Pacific Atlantic Water Flow (417)
- Shortest Path in Binary Matrix (1091), Minimum Knight Moves (1197)
- [CSES](https://cses.fi/problemset/) "Counting Rooms", "Labyrinth", "Building Roads"

---

**→ Next:** [`03-Topological-Sort.md`](./03-Topological-Sort.md) | All algorithms → [`COMPENDIUM-All-Graph-Algorithms.md`](./COMPENDIUM-All-Graph-Algorithms.md)
