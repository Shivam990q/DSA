# Min Cost to Connect All Points

**Platform**: LeetCode 1584 · **Difficulty**: Medium · **Topics**: Array, Union-Find, Graph, Minimum Spanning Tree, Heap · **Pattern**: MST (Prim / Kruskal)

---

## 📜 Problem Statement

You are given an array `points` representing integer coordinates of some points on a 2D-plane, where `points[i] = [xi, yi]`.

The cost of connecting two points `[xi, yi]` and `[xj, yj]` is the **manhattan distance** between them: `|xi - xj| + |yi - yj|`, where `|val|` denotes the absolute value of `val`.

Return *the minimum cost to make all points connected.* All points are connected if there is **exactly one** simple path between any two points.

### Examples

**Example 1:**
```
Input: points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
Output: 20
Explanation: Connecting the points with the listed edges yields a tree
of total cost 20, and no cheaper connection exists.
```

**Example 2:**
```
Input: points = [[3,12],[-2,5],[-4,1]]
Output: 18
```

**Example 3:**
```
Input: points = [[0,0]]
Output: 0
Explanation: A single point needs no edges.
```

### Constraints
```
1 <= points.length <= 1000
-10^6 <= xi, yi <= 10^6
All pairs (xi, yi) are distinct.
```

---

## 🧠 Understanding the problem

"Connect all points with minimum total cost, exactly one path between any two" is the literal definition of a **Minimum Spanning Tree (MST)**. The graph is **complete**: every pair of points has an implicit edge whose weight is their Manhattan distance. With `n ≤ 1000`, there are up to ~500,000 edges.

Two classic MST algorithms:

- **Prim's**: grow the tree from an arbitrary start, repeatedly adding the cheapest edge that connects a new (unvisited) point to the tree. A min-heap (or, for dense graphs, an O(n²) array scan) tracks the cheapest connection to each outside point.
- **Kruskal's**: sort *all* edges by weight and add them cheapest-first, skipping any edge that would form a cycle (detected with Union-Find). Stop after `n − 1` edges.

Because the graph is dense (complete), Prim's with an adjacency-free O(n²) or heap formulation is natural; Kruskal's must materialize all O(n²) edges and sort them.

---

## Approach 1 — Prim's algorithm with a min-heap (recommended) ⭐

### Intuition
Start with one point in the tree. Keep a min-heap of `(cost, point)` candidates to pull the next-cheapest point into the tree. Each time we pop an unvisited point, we commit its connecting cost and push its distances to all remaining outside points.

### Algorithm
1. `inMST` all false; min-heap seeded with `(0, 0)` (start at point 0 with cost 0).
2. While the heap is non-empty and fewer than `n` points are in the tree:
   - Pop `(d, u)`. If `u` is already in the tree, skip.
   - Add `u`: `total += d`, mark `inMST[u]`, `used++`.
   - For each point `v` not in the tree, push `(manhattan(u, v), v)`.
3. Return `total`.

### Dry run on Example 2 `[[3,12],[-2,5],[-4,1]]`
```
Distances: 0-1 = |3+2|+|12-5| = 5+7 = 12; 0-2 = 7+11 = 18; 1-2 = 2+4 = 6.
Heap seeded (0,0).
Pop (0,0): add point 0. total=0. push (12,1),(18,2).
Pop (12,1): add point 1. total=12. push (6,2)  [and 18,2 already there].
Pop (6,2): add point 2. total=18.
All 3 points in tree → total = 18.
```

### Code

```cpp
class Solution {
public:
    int minCostConnectPoints(vector<vector<int>>& points) {
        int n = points.size(), total = 0, used = 0;
        vector<bool> inMST(n, false);
        priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
        pq.push({0, 0});
        while (!pq.empty() && used < n) {
            auto [d, u] = pq.top(); pq.pop();
            if (inMST[u]) continue;
            inMST[u] = true;
            total += d;
            used++;
            for (int v = 0; v < n; v++)
                if (!inMST[v]) {
                    int w = abs(points[u][0] - points[v][0])
                          + abs(points[u][1] - points[v][1]);
                    pq.push({w, v});
                }
        }
        return total;
    }
};
```
```java
class Solution {
    public int minCostConnectPoints(int[][] points) {
        int n = points.length, total = 0, used = 0;
        boolean[] inMST = new boolean[n];
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
        pq.offer(new int[]{0, 0});
        while (!pq.isEmpty() && used < n) {
            int[] cur = pq.poll();
            int d = cur[0], u = cur[1];
            if (inMST[u]) continue;
            inMST[u] = true;
            total += d;
            used++;
            for (int v = 0; v < n; v++)
                if (!inMST[v]) {
                    int w = Math.abs(points[u][0] - points[v][0])
                          + Math.abs(points[u][1] - points[v][1]);
                    pq.offer(new int[]{w, v});
                }
        }
        return total;
    }
}
```
```python
import heapq

class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        in_mst = [False] * n
        pq = [(0, 0)]
        total = used = 0
        while pq and used < n:
            d, u = heapq.heappop(pq)
            if in_mst[u]:
                continue
            in_mst[u] = True
            total += d
            used += 1
            for v in range(n):
                if not in_mst[v]:
                    w = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
                    heapq.heappush(pq, (w, v))
        return total
```

### Complexity
- **Time**: O(n² log n) — for each added point we push up to `n` candidates; heap ops are log.
- **Space**: O(n²) heap entries in the worst case.

---

## Approach 2 — Prim's with an O(n²) array (no heap)

### Intuition
For a dense/complete graph, skip the heap. Keep `minDist[v]` = cheapest edge from the tree to outside point `v`. Each round, linearly pick the unvisited point with the smallest `minDist`, add it, and update neighbors. This is the classic dense-graph Prim and avoids heap overhead.

### Algorithm
1. `minDist` all `∞`, `minDist[0] = 0`; `inMST` all false.
2. Repeat `n` times: scan for the unvisited point `u` with the smallest `minDist`; add it (`total += minDist[u]`, mark visited). For each unvisited `v`, `minDist[v] = min(minDist[v], dist(u, v))`.
3. Return `total`.

### Dry run on Example 2
```
minDist=[0,∞,∞]. 
Pick 0 (0). total=0. update: minDist[1]=12, minDist[2]=18.
Pick 1 (12). total=12. update: minDist[2]=min(18,6)=6.
Pick 2 (6). total=18.
Answer 18.
```

### Code

```cpp
class Solution {
public:
    int minCostConnectPoints(vector<vector<int>>& points) {
        int n = points.size(), total = 0;
        vector<int> minDist(n, INT_MAX);
        vector<bool> inMST(n, false);
        minDist[0] = 0;
        for (int iter = 0; iter < n; iter++) {
            int u = -1;
            for (int v = 0; v < n; v++)
                if (!inMST[v] && (u == -1 || minDist[v] < minDist[u])) u = v;
            inMST[u] = true;
            total += minDist[u];
            for (int v = 0; v < n; v++)
                if (!inMST[v]) {
                    int w = abs(points[u][0] - points[v][0])
                          + abs(points[u][1] - points[v][1]);
                    if (w < minDist[v]) minDist[v] = w;
                }
        }
        return total;
    }
};
```
```java
class Solution {
    public int minCostConnectPoints(int[][] points) {
        int n = points.length, total = 0;
        int[] minDist = new int[n];
        Arrays.fill(minDist, Integer.MAX_VALUE);
        boolean[] inMST = new boolean[n];
        minDist[0] = 0;
        for (int iter = 0; iter < n; iter++) {
            int u = -1;
            for (int v = 0; v < n; v++)
                if (!inMST[v] && (u == -1 || minDist[v] < minDist[u])) u = v;
            inMST[u] = true;
            total += minDist[u];
            for (int v = 0; v < n; v++)
                if (!inMST[v]) {
                    int w = Math.abs(points[u][0] - points[v][0])
                          + Math.abs(points[u][1] - points[v][1]);
                    if (w < minDist[v]) minDist[v] = w;
                }
        }
        return total;
    }
}
```
```python
class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        min_dist = [float('inf')] * n
        in_mst = [False] * n
        min_dist[0] = 0
        total = 0
        for _ in range(n):
            u = -1
            for v in range(n):
                if not in_mst[v] and (u == -1 or min_dist[v] < min_dist[u]):
                    u = v
            in_mst[u] = True
            total += min_dist[u]
            for v in range(n):
                if not in_mst[v]:
                    w = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
                    if w < min_dist[v]:
                        min_dist[v] = w
        return total
```

### Complexity
- **Time**: O(n²) — two nested loops, no log factor.
- **Space**: O(n).

---

## Approach 3 — Kruskal's algorithm with Union-Find

### Intuition
Generate all `n(n−1)/2` candidate edges, sort by Manhattan distance, then greedily add the cheapest edge that joins two different components (use DSU to skip cycle-forming edges). Stop once `n − 1` edges are accepted.

### Algorithm
1. Build all edges `(dist, i, j)` for `i < j`; sort ascending.
2. DSU over `n` points; `total = 0`, `count = 0`.
3. For each edge in order: if endpoints are in different sets, union them, add the cost, `count++`. Stop when `count == n − 1`.
4. Return `total`.

### Dry run on Example 2
```
Edges sorted: (6,1,2),(12,0,1),(18,0,2).
(6,1,2): 1,2 differ → union, total=6, count=1.
(12,0,1): 0 vs {1,2} differ → union, total=18, count=2 == n-1 → stop.
Answer 18.
```

### Code

```cpp
class Solution {
    vector<int> parent, rnk;
    int find(int x) {
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }
    bool unite(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return false;
        if (rnk[ra] < rnk[rb]) swap(ra, rb);
        parent[rb] = ra;
        if (rnk[ra] == rnk[rb]) rnk[ra]++;
        return true;
    }
public:
    int minCostConnectPoints(vector<vector<int>>& points) {
        int n = points.size();
        parent.resize(n);
        rnk.assign(n, 0);
        iota(parent.begin(), parent.end(), 0);
        vector<tuple<int,int,int>> edges;
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++) {
                int w = abs(points[i][0] - points[j][0])
                      + abs(points[i][1] - points[j][1]);
                edges.push_back({w, i, j});
            }
        sort(edges.begin(), edges.end());
        int total = 0, count = 0;
        for (auto& [w, i, j] : edges) {
            if (unite(i, j)) {
                total += w;
                if (++count == n - 1) break;
            }
        }
        return total;
    }
};
```
```java
class Solution {
    private int[] parent, rank;

    public int minCostConnectPoints(int[][] points) {
        int n = points.length;
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        List<int[]> edges = new ArrayList<>();
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++) {
                int w = Math.abs(points[i][0] - points[j][0])
                      + Math.abs(points[i][1] - points[j][1]);
                edges.add(new int[]{w, i, j});
            }
        edges.sort((a, b) -> a[0] - b[0]);
        int total = 0, count = 0;
        for (int[] e : edges) {
            if (unite(e[1], e[2])) {
                total += e[0];
                if (++count == n - 1) break;
            }
        }
        return total;
    }

    private int find(int x) {
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }

    private boolean unite(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return false;
        if (rank[ra] < rank[rb]) { int t = ra; ra = rb; rb = t; }
        parent[rb] = ra;
        if (rank[ra] == rank[rb]) rank[ra]++;
        return true;
    }
}
```
```python
class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        parent = list(range(n))
        rank = [0] * n

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def unite(a, b):
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1
            return True

        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                w = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                edges.append((w, i, j))
        edges.sort()

        total = count = 0
        for w, i, j in edges:
            if unite(i, j):
                total += w
                count += 1
                if count == n - 1:
                    break
        return total
```

### Complexity
- **Time**: O(n² log n) — dominated by sorting ~n² edges.
- **Space**: O(n²) to store all edges.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Prim's (heap) | O(n² log n) | O(n²) | clean; works on the implicit complete graph ⭐ |
| Prim's (O(n²) array) | O(n²) | O(n) | best for dense graphs; no heap, least memory |
| Kruskal's (DSU) | O(n² log n) | O(n²) | sort all edges; great when edges are given explicitly |

For this *complete-graph* problem, the **O(n²) array Prim** is theoretically the fastest and lightest. The heap Prim and Kruskal are both fine and showcase the two canonical MST algorithms.

---

## 🧪 Edge cases & pitfalls
- **Single point** → cost 0 (no edges needed).
- **Manhattan distance** uses absolute values — do not accidentally use Euclidean.
- **Integer overflow**: with `n = 1000` and coordinates up to 10⁶, individual distances fit in 32-bit, and the total MST cost also fits comfortably in a 32-bit `int` here, but using `long` for the accumulator is a safe habit.
- **Prim "skip if already in MST"** — popping a stale heap entry for an already-added point must be ignored, or you double-count.
- **Stop Kruskal at `n − 1` edges** — continuing wastes time (though it stays correct).

---

## 🔗 Related problems
- **Min Cost to Make Network Connected** (LC 1319) — connectivity via DSU (unweighted spare-edge logic).
- **Connecting Cities With Minimum Cost** (LC 1135) — MST on an explicit weighted graph.
- **Optimize Water Distribution in a Village** (LC 1168) — MST with a virtual node.
- **Network Delay Time** (LC 743) — shortest path (contrast with spanning tree).

---

**→ Next:** [`04-Swim-In-Rising-Water.md`](./04-Swim-In-Rising-Water.md) | **← Prev:** [`02-Cheapest-Flights-K-Stops.md`](./02-Cheapest-Flights-K-Stops.md) | [Problem set index](./00-Index.md)
