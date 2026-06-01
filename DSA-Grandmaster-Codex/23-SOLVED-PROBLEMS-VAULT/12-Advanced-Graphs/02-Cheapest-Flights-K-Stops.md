# Cheapest Flights Within K Stops

**Platform**: LeetCode 787 · **Difficulty**: Medium · **Topics**: Graph, Dynamic Programming, Shortest Path, Bellman-Ford, BFS · **Pattern**: Bounded-edge shortest path

---

## 📜 Problem Statement

There are `n` cities connected by some number of flights. You are given an array `flights` where `flights[i] = [fromi, toi, pricei]` indicates that there is a flight from city `fromi` to city `toi` with cost `pricei`.

You are also given three integers `src`, `dst`, and `k`, return *the **cheapest price** from `src` to `dst` with at most `k` stops.* If there is no such route, return `-1`.

### Examples

**Example 1:**
```
Input: n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]],
       src = 0, dst = 3, k = 1
Output: 700
Explanation: The optimal path with at most 1 stop is 0 -> 1 -> 3, cost 100 + 600 = 700.
Note: 0 -> 1 -> 2 -> 3 is cheaper (500) but uses 2 stops, which exceeds k = 1.
```

**Example 2:**
```
Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 1
Output: 200
Explanation: 0 -> 1 -> 2 costs 200 with 1 stop.
```

**Example 3:**
```
Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 0
Output: 500
Explanation: With 0 stops, the only option is the direct flight 0 -> 2 costing 500.
```

### Constraints
```
1 <= n <= 100
0 <= flights.length <= (n * (n - 1) / 2)
flights[i].length == 3
0 <= fromi, toi < n
fromi != toi
1 <= pricei <= 10^4
There will not be any multiple flights between two cities.
0 <= src, dst, n - 1
src != dst
0 <= k <= n - 1
```

---

## 🧠 Understanding the problem

This is a shortest-path problem with a twist: a hard cap on the number of edges. "At most `k` stops" means the route may use at most **`k + 1` flights** (k intermediate cities ⇒ k+1 edges). Plain Dijkstra fails here because the globally cheapest path might use too many flights; we must respect the edge-count limit.

The clean tool is **Bellman-Ford run for exactly `k + 1` rounds**. The defining property of Bellman-Ford: after `i` relaxation rounds, `dist[v]` holds the cheapest cost to reach `v` using **at most `i` edges**. So running `k + 1` rounds gives us exactly "cheapest using at most `k + 1` flights" = "at most `k` stops."

The critical detail: each round must relax against a **snapshot of the previous round's distances**, not the live array. Relaxing in place would let a single round chain multiple edges (use more than one extra flight), breaking the edge-count guarantee.

---

## Approach 1 — Bellman-Ford limited to k+1 rounds (recommended) ⭐

### Intuition
Each round lets every city be reached using one *more* flight than before. Do exactly `k + 1` rounds and you have all routes using at most `k + 1` flights. The snapshot ensures a city updated this round is not immediately used to relax further within the same round.

### Algorithm
1. `dist` array of size `n`, all `∞`, `dist[src] = 0`.
2. Repeat `k + 1` times:
   - Copy `dist` into `tmp`.
   - For each flight `(u, v, w)`: if `dist[u] + w < tmp[v]`, set `tmp[v] = dist[u] + w`.
   - `dist = tmp`.
3. Return `dist[dst]` or `-1` if still `∞`.

### Dry run on Example 1 (`src=0, dst=3, k=1` → 2 rounds)
```
dist init: [0, ∞, ∞, ∞].
Round 1 (≤1 flight): from 0→1 (100). tmp=[0,100,∞,∞]. dist=[0,100,∞,∞].
Round 2 (≤2 flights): 1→2 (100→200), 1→3 (100+600=700), 2→3 needs dist[2] which is ∞ this round (snapshot).
   tmp=[0,100,200,700]. dist=[0,100,200,700].
dist[3] = 700 → answer 700.  (the 500 route needs 3 flights → excluded)
```

### Code

```cpp
class Solution {
public:
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
        const int INF = 1e9;
        vector<int> dist(n, INF);
        dist[src] = 0;
        for (int i = 0; i <= k; i++) {
            vector<int> tmp = dist;
            for (auto& f : flights) {
                int u = f[0], v = f[1], w = f[2];
                if (dist[u] != INF && dist[u] + w < tmp[v])
                    tmp[v] = dist[u] + w;
            }
            dist = tmp;
        }
        return dist[dst] == INF ? -1 : dist[dst];
    }
};
```
```java
class Solution {
    public int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {
        final int INF = 1_000_000_000;
        int[] dist = new int[n];
        Arrays.fill(dist, INF);
        dist[src] = 0;
        for (int i = 0; i <= k; i++) {
            int[] tmp = dist.clone();
            for (int[] f : flights) {
                int u = f[0], v = f[1], w = f[2];
                if (dist[u] != INF && dist[u] + w < tmp[v])
                    tmp[v] = dist[u] + w;
            }
            dist = tmp;
        }
        return dist[dst] == INF ? -1 : dist[dst];
    }
}
```
```python
class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        INF = float('inf')
        dist = [INF] * n
        dist[src] = 0
        for _ in range(k + 1):
            tmp = dist[:]
            for u, v, w in flights:
                if dist[u] != INF and dist[u] + w < tmp[v]:
                    tmp[v] = dist[u] + w
            dist = tmp
        return -1 if dist[dst] == INF else dist[dst]
```

### Complexity
- **Time**: O(k · E) — `k + 1` rounds, each scanning all edges.
- **Space**: O(n) for the two distance arrays.

---

## Approach 2 — BFS by levels (track stops)

### Intuition
Do a level-by-level BFS where each level corresponds to one more flight. Carry `(node, cost)` and stop after `k + 1` levels. Keep a `best[node]` array; only enqueue a state if it improves the best known cost for that node, which prunes the exploration.

### Algorithm
1. Build adjacency list. `best[src] = 0`. Queue starts with `(src, 0)`; `stops = 0`.
2. While queue non-empty and `stops <= k`:
   - Process the whole current level. For each `(u, cost)`, relax each neighbor `(v, w)`: if `cost + w < best[v]`, update and enqueue `(v, cost + w)`.
   - `stops++`.
3. Return `best[dst]` if finite, else `-1`.

### Dry run on Example 2 (`src=0, dst=2, k=1`)
```
best=[0,∞,∞], queue=[(0,0)], stops=0.
Level 0: (0,0) → 1 cost 100 (<∞) enqueue; 2 cost 500 (<∞) enqueue. best=[0,100,500]. stops=1.
Level 1 (stops=1<=k): (1,100) → 2 cost 200 (<500) update enqueue. (2,500) → no outgoing improves.
   best=[0,100,200]. stops=2 > k → stop.
best[2] = 200 → answer 200.
```

### Code

```cpp
class Solution {
public:
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
        vector<vector<pair<int,int>>> adj(n);
        for (auto& f : flights) adj[f[0]].push_back({f[1], f[2]});
        const int INF = 1e9;
        vector<int> best(n, INF);
        best[src] = 0;
        queue<pair<int,int>> q;       // (node, cost)
        q.push({src, 0});
        int stops = 0;
        while (!q.empty() && stops <= k) {
            int sz = q.size();
            for (int i = 0; i < sz; i++) {
                auto [u, cost] = q.front(); q.pop();
                for (auto& [v, w] : adj[u]) {
                    if (cost + w < best[v]) {
                        best[v] = cost + w;
                        q.push({v, best[v]});
                    }
                }
            }
            stops++;
        }
        return best[dst] == INF ? -1 : best[dst];
    }
};
```
```java
class Solution {
    public int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] f : flights) adj.get(f[0]).add(new int[]{f[1], f[2]});
        final int INF = 1_000_000_000;
        int[] best = new int[n];
        Arrays.fill(best, INF);
        best[src] = 0;
        Queue<int[]> q = new LinkedList<>();   // (node, cost)
        q.offer(new int[]{src, 0});
        int stops = 0;
        while (!q.isEmpty() && stops <= k) {
            int sz = q.size();
            for (int i = 0; i < sz; i++) {
                int[] cur = q.poll();
                int u = cur[0], cost = cur[1];
                for (int[] e : adj.get(u)) {
                    int v = e[0], w = e[1];
                    if (cost + w < best[v]) {
                        best[v] = cost + w;
                        q.offer(new int[]{v, best[v]});
                    }
                }
            }
            stops++;
        }
        return best[dst] == INF ? -1 : best[dst];
    }
}
```
```python
from collections import deque

class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        adj = [[] for _ in range(n)]
        for u, v, w in flights:
            adj[u].append((v, w))
        INF = float('inf')
        best = [INF] * n
        best[src] = 0
        q = deque([(src, 0)])      # (node, cost)
        stops = 0
        while q and stops <= k:
            for _ in range(len(q)):
                u, cost = q.popleft()
                for v, w in adj[u]:
                    if cost + w < best[v]:
                        best[v] = cost + w
                        q.append((v, best[v]))
            stops += 1
        return -1 if best[dst] == INF else best[dst]
```

### Complexity
- **Time**: O(k · E) in the worst case — at most `k + 1` levels, each relaxing edges.
- **Space**: O(n + E) for the adjacency list, `best`, and queue.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Bellman-Ford (k+1 rounds) | O(k·E) | O(n) | cleanest; snapshot enforces the edge cap ⭐ |
| BFS by levels | O(k·E) | O(n + E) | intuitive level = stops; needs `best[]` pruning |

Both encode the same idea: limit the number of edges to `k + 1`. Bellman-Ford with the snapshot is the most robust and is the standard interview answer. (Plain Dijkstra without a stops dimension is **wrong** here.)

---

## 🧪 Edge cases & pitfalls
- **The snapshot is essential** in Bellman-Ford — relaxing in place can use more than `k + 1` edges in one round and gives a wrong (too-cheap) answer.
- **Stops vs flights**: `k` stops ⇒ `k + 1` edges ⇒ `k + 1` rounds/levels. Off-by-one here is the most common bug.
- **`k = 0`** → only direct flights count (Example 3).
- **Unreachable within the limit** → `-1`.
- **Don't mark nodes permanently visited** in the BFS version; a node may legitimately be re-reached with a cheaper cost on a different level.

---

## 🔗 Related problems
- **Network Delay Time** (LC 743) — unconstrained shortest path (Dijkstra).
- **Cheapest Flights** is essentially **Bellman-Ford with a round cap** — recognize the pattern in any "at most K edges" problem.
- **Path with Minimum Effort** (LC 1631) — different cost metric, Dijkstra/binary search.
- **Find the City With the Smallest Number of Neighbors at a Threshold Distance** (LC 1334) — all-pairs shortest paths.

---

**→ Next:** [`03-Min-Cost-Connect-Points.md`](./03-Min-Cost-Connect-Points.md) | **← Prev:** [`01-Network-Delay-Time.md`](./01-Network-Delay-Time.md) | [Problem set index](./00-Index.md)
