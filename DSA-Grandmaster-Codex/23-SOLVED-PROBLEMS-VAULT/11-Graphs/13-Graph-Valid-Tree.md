# Graph Valid Tree

**Platform**: LeetCode 261 · **Difficulty**: Medium · **Topics**: DFS, BFS, Union-Find, Graph · **Pattern**: Tree = connected + acyclic

---

## 📜 Problem Statement

You have a graph of `n` nodes labeled from `0` to `n - 1`. You are given an integer `n` and a list of `edges` where `edges[i] = [ai, bi]` indicates that there is an **undirected** edge between nodes `ai` and `bi` in the graph.

Return `true` *if the edges of the given graph make up a valid tree, and* `false` *otherwise*.

### Examples

**Example 1:**
```
Input: n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]
Output: true
Explanation: 5 nodes, 4 edges, fully connected, no cycle → valid tree.
```

**Example 2:**
```
Input: n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]
Output: false
Explanation: The edges 1-2, 2-3, 1-3 form a cycle, so it is not a tree.
```

**Example 3:**
```
Input: n = 1, edges = []
Output: true
Explanation: A single node with no edges is a valid (trivial) tree.
```

### Constraints
```
1 <= n <= 2000
0 <= edges.length <= 5000
edges[i].length == 2
0 <= ai, bi < n
ai != bi
There are no self-loops or repeated edges.
```

---

## 🧠 Understanding the problem

A graph is a **valid tree** iff it satisfies two conditions:

1. It is **connected** (every node reachable from any other).
2. It is **acyclic** (no cycle).

There is a powerful shortcut. A tree on `n` nodes has **exactly `n − 1` edges**. So:

> If `edges.length != n − 1`, it cannot be a tree — return `false` immediately.

Once the edge count is exactly `n − 1`, the two conditions collapse into one: **connected ⟺ acyclic**. With exactly `n − 1` edges, if the graph is connected it must be acyclic (a cycle would require an extra edge somewhere, leaving some node disconnected), and vice versa. So after the edge-count check, we only need to verify **one** of the two properties — typically connectivity (one full traversal reaches all `n` nodes) or "no union ever merges an already-connected pair."

Constraints are small, so any O(n + E) method works.

---

## Approach 1 — Union-Find (recommended) ⭐

### Intuition
Process edges; union endpoints. If an edge's endpoints are **already** in the same set, adding it forms a cycle → not a tree. If we get through all edges with no such conflict **and** end with a single component, it is a tree. The early `edges.size() == n − 1` check makes the component count automatic: no cycle with `n − 1` edges guarantees connectivity.

### Algorithm
1. If `edges.size() != n − 1` → return `false`.
2. `parent[i] = i`. For each edge `(a, b)`:
   - If `find(a) == find(b)` → cycle → return `false`.
   - Else union them.
3. Return `true` (with `n − 1` edges and no cycle, it is connected).

### Dry run on Example 2 (`n=5`, 5 edges)
```
edges.size() = 5, but n - 1 = 4 → 5 != 4 → return false immediately.
(Indeed it has a cycle.)
```
Dry run on Example 1 (`n=5`, 4 edges):
```
4 == n-1, proceed.
[0,1] union. [0,2] union. [0,3] union. [1,4] union.
No edge ever found endpoints already connected → return true.
```

### Code

```cpp
class Solution {
    vector<int> parent, rnk;
    int find(int x) {
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }
public:
    bool validTree(int n, vector<vector<int>>& edges) {
        if ((int)edges.size() != n - 1) return false;
        parent.resize(n);
        rnk.assign(n, 0);
        iota(parent.begin(), parent.end(), 0);
        for (auto& e : edges) {
            int ra = find(e[0]), rb = find(e[1]);
            if (ra == rb) return false;          // cycle
            if (rnk[ra] < rnk[rb]) swap(ra, rb);
            parent[rb] = ra;
            if (rnk[ra] == rnk[rb]) rnk[ra]++;
        }
        return true;
    }
};
```
```java
class Solution {
    private int[] parent, rank;

    public boolean validTree(int n, int[][] edges) {
        if (edges.length != n - 1) return false;
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        for (int[] e : edges) {
            int ra = find(e[0]), rb = find(e[1]);
            if (ra == rb) return false;
            if (rank[ra] < rank[rb]) { int t = ra; ra = rb; rb = t; }
            parent[rb] = ra;
            if (rank[ra] == rank[rb]) rank[ra]++;
        }
        return true;
    }

    private int find(int x) {
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }
}
```
```python
class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False
        parent = list(range(n))
        rank = [0] * n

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for a, b in edges:
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1
        return True
```

### Complexity
- **Time**: O(n·α(n)) ≈ O(n).
- **Space**: O(n) for the DSU arrays.

---

## Approach 2 — DFS/BFS connectivity check

### Intuition
After confirming `edges.size() == n − 1`, the graph is a tree iff it is **connected**. Build the adjacency list and run one traversal from node 0; if it reaches all `n` nodes, it is connected (and, given the edge count, acyclic) → a tree.

### Algorithm
1. If `edges.size() != n − 1` → return `false`.
2. Build the undirected adjacency list.
3. BFS/DFS from node 0, counting visited nodes.
4. Return `visitedCount == n`.

### Dry run on Example 1
```
4 == n-1, proceed. adj built.
BFS from 0: visit 0 → 1,2,3 → from 1 visit 4. visited = {0,1,2,3,4} = 5 = n.
return true.
```

### Code

```cpp
class Solution {
public:
    bool validTree(int n, vector<vector<int>>& edges) {
        if ((int)edges.size() != n - 1) return false;
        vector<vector<int>> adj(n);
        for (auto& e : edges) {
            adj[e[0]].push_back(e[1]);
            adj[e[1]].push_back(e[0]);
        }
        vector<bool> visited(n, false);
        queue<int> q;
        q.push(0);
        visited[0] = true;
        int count = 0;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            count++;
            for (int v : adj[u])
                if (!visited[v]) { visited[v] = true; q.push(v); }
        }
        return count == n;
    }
};
```
```java
class Solution {
    public boolean validTree(int n, int[][] edges) {
        if (edges.length != n - 1) return false;
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) {
            adj.get(e[0]).add(e[1]);
            adj.get(e[1]).add(e[0]);
        }
        boolean[] visited = new boolean[n];
        Queue<Integer> q = new LinkedList<>();
        q.offer(0);
        visited[0] = true;
        int count = 0;
        while (!q.isEmpty()) {
            int u = q.poll();
            count++;
            for (int v : adj.get(u))
                if (!visited[v]) { visited[v] = true; q.offer(v); }
        }
        return count == n;
    }
}
```
```python
from collections import deque

class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False
        adj = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
        visited = [False] * n
        q = deque([0])
        visited[0] = True
        count = 0
        while q:
            u = q.popleft()
            count += 1
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    q.append(v)
        return count == n
```

### Complexity
- **Time**: O(n + E).
- **Space**: O(n + E) for the adjacency list and queue.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Union-Find | O(n·α) | O(n) | edge-count check + no-cycle test ⭐ |
| DFS/BFS connectivity | O(n + E) | O(n + E) | edge-count check + reach-all test |

Both lean on the same theorem: **`n` nodes + exactly `n − 1` edges + (connected OR acyclic) ⇒ tree**. The edge-count guard is the elegant first move that makes either verification trivial.

---

## 🧪 Edge cases & pitfalls
- **Single node, no edges** (`n=1`, `edges=[]`) → `0 == n − 1` and trivially connected → `true`.
- **Too many edges** (`> n − 1`) → guaranteed cycle → `false` (caught by the count check).
- **Too few edges** (`< n − 1`) → cannot be connected → `false`.
- **Skipping the edge-count check** forces you to verify *both* connectivity and acyclicity separately — more code and more bug surface.
- **Undirected adjacency** — add each edge in both directions for the traversal approach.

---

## 🔗 Related problems
- **Number of Connected Components** (LC 323) — count clusters (drop the "single tree" requirement).
- **Redundant Connection** (LC 684) — find the edge that makes a tree non-tree.
- **Course Schedule** (LC 207) — cycle detection in the *directed* setting.
- **Minimum Height Trees** (LC 310) — operates on a tree to find its centroids.

---

**← Prev:** [`12-Walls-And-Gates.md`](./12-Walls-And-Gates.md) | [Problem set index](./00-Index.md) | **→ Next topic:** [`../12-Advanced-Graphs/00-Index.md`](../12-Advanced-Graphs/00-Index.md)
