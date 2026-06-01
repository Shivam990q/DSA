# 🌐 Shortest Paths

> *"From A to B at minimum cost — the most-asked graph question in the universe."*

---

## I. THE ALGORITHM SELECTOR ⭐
| Situation | Use | Time |
|-----------|-----|------|
| Unweighted | **BFS** | O(V+E) |
| Weights 0 or 1 | **0-1 BFS** (deque) | O(V+E) |
| Non-negative weights, single source | **Dijkstra** | O((V+E) log V) |
| Negative weights / detect neg cycle | **Bellman-Ford** | O(V·E) |
| All pairs, small V | **Floyd-Warshall** | O(V³) |
| DAG | **Topo order + relax** | O(V+E) |
| With heuristic (goal-directed) | **A*** | varies |

---

## II. DIJKSTRA ⭐ (non-negative weights)
Greedy: always finalize the closest unfinalized node. Uses a min-heap.
```cpp
vector<long long> dijkstra(int src, int n, vector<vector<pair<int,int>>>& adj) {
    vector<long long> dist(n, LLONG_MAX);
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    dist[src] = 0; pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;            // stale entry
        for (auto [v, w] : adj[u])
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
    }
    return dist;
}
```
**Why non-negative required**: the greedy "closest is final" breaks if a later negative edge could shorten a path. (Full proof: [`../15-CASE-STUDIES-LEGENDARY/08-The-Story-of-Dijkstra.md`](../15-CASE-STUDIES-LEGENDARY/08-The-Story-of-Dijkstra.md).)

---

## III. BELLMAN-FORD (negative weights)
Relax all edges V−1 times. One more relaxation succeeding ⟹ a negative cycle exists.
```cpp
for (int i = 0; i < n - 1; i++)
    for (auto [u, v, w] : edges)
        if (dist[u] != INF && dist[u] + w < dist[v]) dist[v] = dist[u] + w;
// check: any edge still relaxable ⟹ negative cycle
```
O(V·E). Use for: negative edges, negative-cycle detection (arbitrage!).

---

## IV. FLOYD-WARSHALL (all pairs)
```cpp
for (int k = 0; k < n; k++)
  for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
        if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
```
O(V³). Use for V ≤ ~500. Also computes transitive closure (reachability).

---

## V. 0-1 BFS
Weights only 0 or 1: use a deque; push-front for weight-0 edges, push-back for weight-1. O(V+E).
- Useful: grids where some moves are "free."

---

## VI. DIJKSTRA WITH STATE AUGMENTATION ⭐
The node can carry extra state:
- **Cheapest Flights Within K Stops (LC 787)**: state = (city, stops used).
- **Path with Minimum Effort (LC 1631)**: minimize the MAX edge (modified relaxation).
- **Swim in Rising Water (LC 778)**: minimize max elevation.
- **Path with Maximum Probability (LC 1514)**: maximize product (use −log or max-heap).

---

## VII. A* SEARCH
Dijkstra + a heuristic h(v) estimating distance to the goal. Expands fewer nodes when h is good (and admissible). Used in pathfinding (games, maps). At Level 8, **Contraction Hierarchies** make continent-scale routing instant.

---

## VIII. SHORTEST PATH IN A DAG
Topologically sort, then relax edges in order. Handles negative weights too (no cycles). O(V+E). Also gives LONGEST path (max instead of min) — which is NP-hard on general graphs but easy on DAGs.

---

## IX. COUNTING SHORTEST PATHS
Dijkstra + a count array: when you find an equal-distance path, add counts; when shorter, reset. (LC 1976 Number of Ways to Arrive at Destination.)

---

## X. PROBLEMS
- Network Delay Time (743), Cheapest Flights K Stops (787)
- Path with Minimum Effort (1631), Swim in Rising Water (778)
- Path with Maximum Probability (1514), Min Cost to Reach Destination (1928)
- Number of Ways to Arrive at Destination (1976)
- [CSES](https://cses.fi/problemset/) "Shortest Routes I/II", "Flight Discount", "High Score" (Bellman-Ford), "Cycle Finding"

---

**→ Next:** [`07-MST.md`](./07-MST.md)
