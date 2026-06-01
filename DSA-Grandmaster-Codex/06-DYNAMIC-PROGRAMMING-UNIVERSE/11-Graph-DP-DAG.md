# 🧬 DP on Graphs (DAGs)

> *"A DAG has a topological order. A topological order is a DP order."*

---

## I. THE PRINCIPLE
DP requires an acyclic dependency order. A **DAG** (directed acyclic graph) provides exactly that via **topological sort**. Process nodes in topological order; each node's dp depends only on already-processed predecessors.

(If the graph has cycles, plain DP fails — use shortest-path algorithms or SCC condensation first.)

---

## II. LONGEST PATH IN A DAG ⭐
NP-hard in general graphs, but **polynomial in a DAG**:
```cpp
// process in topological order
for (int u : topoOrder)
    for (auto [v, w] : adj[u])
        dp[v] = max(dp[v], dp[u] + w);
```
`dp[v]` = longest path ending at v. O(V + E). (Shortest path in a DAG is the same with min.)

---

## III. COUNTING PATHS IN A DAG
Number of distinct paths from s to t:
```cpp
// process in reverse topological order, or memoized DFS
count[t] = 1;
count[u] = Σ count[v] for each edge u→v;
```
O(V + E).

---

## IV. DP ON IMPLICIT DAGs
Many DPs are secretly DAG DPs:
- **Grid DP** (right/down moves) — the grid is a DAG.
- **Coin change / knapsack** — the state graph is a DAG.
- **LIS** — "i can follow j if a[j] < a[i]" forms a DAG.
- **Longest Increasing Path in a Matrix (LC 329)** — cells form a DAG by increasing value; memoized DFS.

---

## V. DAG DP RECIPES
| Problem type | Approach |
|--------------|----------|
| Longest/shortest path | topo order + relax |
| Count paths | topo order + sum |
| Reachability | DFS/BFS |
| Min/max cost with constraints | topo order + DP with extra state |
| DP with "at most k edges" | layered DP (Bellman-Ford-style) |

---

## VI. CONSTRAINED SHORTEST PATHS (DP flavor)
- **Cheapest Flights Within K Stops (LC 787)**: `dp[k][v]` = min cost to reach v using ≤ k edges (Bellman-Ford-style layered DP). O(k·E).
- **Number of Ways to Arrive at Destination (LC 1976)**: Dijkstra + counting DP for shortest-path counts.

---

## VII. CYCLES? FIRST CONDENSE
If the directed graph has cycles but you need DP:
1. Find SCCs (Tarjan/Kosaraju).
2. Condense each SCC to a single node → the condensation is a DAG.
3. Run DAG DP on the condensation.
(e.g., longest path where you can loop within an SCC freely.)

---

## VIII. COMPLEXITY
- Most DAG DPs: O(V + E).
- Layered (≤ k edges): O(k·E).

---

## IX. PROBLEMS
- Longest Increasing Path in a Matrix (329) ⭐
- Course Schedule II (210) — topo order itself
- Cheapest Flights Within K Stops (787)
- Number of Ways to Arrive at Destination (1976)
- Parallel Courses (1136, 2050) — longest path in DAG
- All Paths From Source to Target (797)
- [CSES](https://cses.fi/problemset/) "Game Routes", "Longest Flight Route", "Investigation"

---

**→ Next:** [`12-Bitmask-DP.md`](./12-Bitmask-DP.md)
