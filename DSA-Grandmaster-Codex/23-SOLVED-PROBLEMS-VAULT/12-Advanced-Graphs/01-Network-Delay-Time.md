# Network Delay Time

**Platform**: LeetCode 743 · **Difficulty**: Medium · **Topics**: Graph, Heap (Priority Queue), Shortest Path, Dijkstra, Bellman-Ford · **Pattern**: Single-source shortest path

---

## 📜 Problem Statement

You are given a network of `n` nodes, labeled from `1` to `n`. You are also given `times`, a list of travel times as directed edges `times[i] = (ui, vi, wi)`, where `ui` is the source node, `vi` is the target node, and `wi` is the time it takes for a signal to travel from source to target.

We will send a signal from a given node `k`. Return *the **minimum** time it takes for all the `n` nodes to receive the signal*. If it is impossible for all the `n` nodes to receive the signal, return `-1`.

### Examples

**Example 1:**
```
Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
Output: 2
Explanation: Signal from node 2 reaches node 1 in 1, node 3 in 1,
node 4 in 2 (via 3). The last node receives it at time 2.
```

**Example 2:**
```
Input: times = [[1,2,1]], n = 2, k = 1
Output: 1
```

**Example 3:**
```
Input: times = [[1,2,1]], n = 2, k = 2
Output: -1
Explanation: Starting at node 2, node 1 can never be reached.
```

### Constraints
```
1 <= k <= n <= 100
1 <= times.length <= 6000
times[i].length == 3
1 <= ui, vi <= n
ui != vi
0 <= wi <= 100
All the pairs (ui, vi) are unique. (i.e., no multiple edges.)
```

---

## 🧠 Understanding the problem

The signal starts at `k` and propagates along directed edges, each taking `wi` time. A node "receives" the signal at the earliest time any path from `k` reaches it — that is its **shortest-path distance** from `k`. For *all* nodes to have received the signal, we wait until the **slowest** of those earliest times, i.e. the **maximum shortest-path distance** over all nodes.

So:
- Compute the shortest distance from `k` to every node.
- If any node is unreachable → return `-1`.
- Otherwise the answer is the maximum of those distances.

Weights are non-negative (`0 <= wi <= 100`), which is exactly the setting for **Dijkstra**. Bellman-Ford also works (and would handle negative weights, which we don't have here) but is slower.

---

## Approach 1 — Dijkstra with a min-heap (recommended) ⭐

### Intuition
Dijkstra always finalizes the closest not-yet-settled node. Using a min-heap keyed by tentative distance, we pop the node with the smallest distance, lock it in, and relax its outgoing edges. Because weights are non-negative, the first time a node is popped its distance is final.

### Algorithm
1. Build an adjacency list `adj[u] = [(v, w), ...]`.
2. `dist[k] = 0`; push `(0, k)` into a min-heap.
3. While the heap is non-empty: pop `(d, u)`. If `d` is stale (`> dist[u]`), skip. For each edge `(v, w)`: if `d + w < dist[v]`, update and push.
4. If every node has a finite distance, return the max; else `-1`.

### Dry run on Example 1 (`k=2`)
```
adj: 2→1(1), 2→3(1), 3→4(1).
dist[2]=0, heap=[(0,2)].
Pop (0,2): relax 1→dist1=1 push; 3→dist3=1 push.
Pop (1,1): no outgoing edges.
Pop (1,3): relax 4→dist4=2 push.
Pop (2,4): no outgoing.
dist = {1:1, 2:0, 3:1, 4:2}. max = 2 → answer 2.
```

### Code

```cpp
class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        vector<vector<pair<int,int>>> adj(n + 1);
        for (auto& t : times) adj[t[0]].push_back({t[1], t[2]});
        vector<int> dist(n + 1, INT_MAX);
        dist[k] = 0;
        priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
        pq.push({0, k});
        while (!pq.empty()) {
            auto [d, u] = pq.top(); pq.pop();
            if (d > dist[u]) continue;
            for (auto& [v, w] : adj[u])
                if (d + w < dist[v]) {
                    dist[v] = d + w;
                    pq.push({dist[v], v});
                }
        }
        int ans = 0;
        for (int i = 1; i <= n; i++) {
            if (dist[i] == INT_MAX) return -1;
            ans = max(ans, dist[i]);
        }
        return ans;
    }
};
```
```java
class Solution {
    public int networkDelayTime(int[][] times, int n, int k) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int i = 0; i <= n; i++) adj.add(new ArrayList<>());
        for (int[] t : times) adj.get(t[0]).add(new int[]{t[1], t[2]});
        int[] dist = new int[n + 1];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[k] = 0;
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
        pq.offer(new int[]{0, k});
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            int d = cur[0], u = cur[1];
            if (d > dist[u]) continue;
            for (int[] e : adj.get(u)) {
                int v = e[0], w = e[1];
                if (d + w < dist[v]) {
                    dist[v] = d + w;
                    pq.offer(new int[]{dist[v], v});
                }
            }
        }
        int ans = 0;
        for (int i = 1; i <= n; i++) {
            if (dist[i] == Integer.MAX_VALUE) return -1;
            ans = Math.max(ans, dist[i]);
        }
        return ans;
    }
}
```
```python
import heapq

class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        adj = [[] for _ in range(n + 1)]
        for u, v, w in times:
            adj[u].append((v, w))
        dist = [float('inf')] * (n + 1)
        dist[k] = 0
        pq = [(0, k)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in adj[u]:
                if d + w < dist[v]:
                    dist[v] = d + w
                    heapq.heappush(pq, (dist[v], v))
        ans = 0
        for i in range(1, n + 1):
            if dist[i] == float('inf'):
                return -1
            ans = max(ans, dist[i])
        return ans
```

### Complexity
- **Time**: O(E log V) — each edge can push to the heap; heap ops are log V.
- **Space**: O(V + E) for the adjacency list, distance array, and heap.

---

## Approach 2 — Bellman-Ford

### Intuition
Relax every edge `V − 1` times. After round `i`, all shortest paths using at most `i` edges are correct; since any shortest path uses at most `V − 1` edges, `V − 1` rounds suffice. Simpler to code (no heap) and tolerates negative weights — though here we have none.

### Algorithm
1. `dist[k] = 0`, all others `∞`.
2. Repeat `n − 1` times: for each edge `(u, v, w)`, if `dist[u] + w < dist[v]`, update `dist[v]`.
3. If any node is still `∞` → `-1`; else return the max distance.

### Dry run on Example 1 (`k=2`)
```
Init dist[2]=0.
Round 1: edge 2→1 sets dist1=1; 2→3 sets dist3=1; 3→4 sets dist4=2.
Round 2,3: no further improvement.
max(dist[1..4]) = 2 → answer 2.
```

### Code

```cpp
class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        const int INF = 1e9;
        vector<int> dist(n + 1, INF);
        dist[k] = 0;
        for (int i = 0; i < n - 1; i++)
            for (auto& t : times) {
                int u = t[0], v = t[1], w = t[2];
                if (dist[u] != INF && dist[u] + w < dist[v])
                    dist[v] = dist[u] + w;
            }
        int ans = 0;
        for (int i = 1; i <= n; i++) {
            if (dist[i] == INF) return -1;
            ans = max(ans, dist[i]);
        }
        return ans;
    }
};
```
```java
class Solution {
    public int networkDelayTime(int[][] times, int n, int k) {
        final int INF = 1_000_000_000;
        int[] dist = new int[n + 1];
        Arrays.fill(dist, INF);
        dist[k] = 0;
        for (int i = 0; i < n - 1; i++)
            for (int[] t : times) {
                int u = t[0], v = t[1], w = t[2];
                if (dist[u] != INF && dist[u] + w < dist[v])
                    dist[v] = dist[u] + w;
            }
        int ans = 0;
        for (int i = 1; i <= n; i++) {
            if (dist[i] == INF) return -1;
            ans = Math.max(ans, dist[i]);
        }
        return ans;
    }
}
```
```python
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        INF = float('inf')
        dist = [INF] * (n + 1)
        dist[k] = 0
        for _ in range(n - 1):
            for u, v, w in times:
                if dist[u] != INF and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
        ans = 0
        for i in range(1, n + 1):
            if dist[i] == INF:
                return -1
            ans = max(ans, dist[i])
        return ans
```

### Complexity
- **Time**: O(V·E) — `V − 1` rounds over all edges.
- **Space**: O(V) for the distance array.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Dijkstra (min-heap) | O(E log V) | O(V + E) | optimal for non-negative weights ⭐ |
| Bellman-Ford | O(V·E) | O(V) | simpler, handles negatives, slower |

Given non-negative weights, Dijkstra is the go-to. Bellman-Ford is the answer if the problem ever introduces negative edges or you want the simplest possible code at small scale.

---

## 🧪 Edge cases & pitfalls
- **Unreachable node** → return `-1` (some `dist` stays infinite). Easy to forget when you only track the max.
- **1-indexed nodes** — size arrays as `n + 1` and ignore index 0.
- **Stale heap entries** in Dijkstra — skip a popped `(d, u)` when `d > dist[u]`, otherwise you reprocess outdated distances (still correct but wasteful; with a `visited` set it is also fine).
- **Zero-weight edges** are allowed (`wi` can be 0) — Dijkstra handles them fine.
- **The answer is the MAX of distances**, not the sum — a common misread.

---

## 🔗 Related problems
- **Cheapest Flights Within K Stops** (LC 787) — shortest path with an edge-count cap.
- **Path with Maximum Probability** (LC 1514) — Dijkstra maximizing a product.
- **Swim in Rising Water** (LC 778) — Dijkstra where path cost is the max edge.
- **Find the City With the Smallest Number of Neighbors** (LC 1334) — all-pairs (Floyd-Warshall / Dijkstra per node).

---

**→ Next:** [`02-Cheapest-Flights-K-Stops.md`](./02-Cheapest-Flights-K-Stops.md) | [Problem set index](./00-Index.md)
