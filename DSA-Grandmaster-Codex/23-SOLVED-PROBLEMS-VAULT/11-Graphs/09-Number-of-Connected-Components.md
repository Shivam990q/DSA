# Number of Connected Components in an Undirected Graph

**Platform**: LeetCode 323 · **Difficulty**: Medium · **Topics**: DFS, BFS, Union-Find, Graph · **Pattern**: Connected components / DSU

---

## 📜 Problem Statement

You have a graph of `n` nodes labeled from `0` to `n - 1`. You are given an integer `n` and a list of `edges` where `edges[i] = [ai, bi]` indicates that there is an **undirected** edge between nodes `ai` and `bi` in the graph.

Return *the number of connected components in the graph*.

### Examples

**Example 1:**
```
Input: n = 5, edges = [[0,1],[1,2],[3,4]]
Output: 2
Explanation: Nodes {0,1,2} form one component and {3,4} form another.
```

**Example 2:**
```
Input: n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]
Output: 1
Explanation: All five nodes are chained into a single component.
```

**Example 3:**
```
Input: n = 4, edges = []
Output: 4
Explanation: With no edges, every node is its own component.
```

### Constraints
```
1 <= n <= 2000
0 <= edges.length <= 5000
edges[i].length == 2
0 <= ai, bi < n
ai != bi
There are no repeated edges.
```

---

## 🧠 Understanding the problem

A **connected component** is a maximal set of nodes that can all reach one another. We must count how many such clusters the graph splits into.

Two classic strategies:

- **Traversal counting (DFS/BFS)**: visit nodes; each time we launch a fresh traversal from an unvisited node, we have found a new component, and the traversal marks everything reachable from it.
- **Union-Find (DSU)**: start with `n` singleton sets. Each edge tries to merge the two endpoints' sets; a *successful* merge (they were in different sets) reduces the component count by 1. The final count is the answer.

The union-find view is especially crisp: **answer = n − (number of merges that actually joined two distinct sets)**. Constraints are small, so all approaches run comfortably.

---

## Approach 1 — Union-Find (recommended) ⭐

### Intuition
Every node starts alone, so we begin with `n` components. Process each edge: if its endpoints are already in the same set, the edge is redundant (no change). If they are in different sets, joining them fuses two components into one, so decrement the count.

### Algorithm
1. `parent[i] = i`, `rank[i] = 0`, `components = n`.
2. For each edge `(a, b)`:
   - `ra = find(a)`, `rb = find(b)`.
   - If `ra != rb`: union by rank, `components--`.
3. Return `components`.

### Dry run on Example 1 (`edges [0,1],[1,2],[3,4]`, n=5)
```
components=5.
[0,1]: find(0)=0, find(1)=1 → differ → union → components=4.
[1,2]: find(1)=0, find(2)=2 → differ → union → components=3.
[3,4]: find(3)=3, find(4)=4 → differ → union → components=2.
Answer = 2.
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
    int countComponents(int n, vector<vector<int>>& edges) {
        parent.resize(n);
        rnk.assign(n, 0);
        iota(parent.begin(), parent.end(), 0);
        int components = n;
        for (auto& e : edges) {
            int ra = find(e[0]), rb = find(e[1]);
            if (ra != rb) {
                if (rnk[ra] < rnk[rb]) swap(ra, rb);
                parent[rb] = ra;
                if (rnk[ra] == rnk[rb]) rnk[ra]++;
                components--;
            }
        }
        return components;
    }
};
```
```java
class Solution {
    private int[] parent, rank;

    public int countComponents(int n, int[][] edges) {
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        int components = n;
        for (int[] e : edges) {
            int ra = find(e[0]), rb = find(e[1]);
            if (ra != rb) {
                if (rank[ra] < rank[rb]) { int t = ra; ra = rb; rb = t; }
                parent[rb] = ra;
                if (rank[ra] == rank[rb]) rank[ra]++;
                components--;
            }
        }
        return components;
    }

    private int find(int x) {
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }
}
```
```python
class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        parent = list(range(n))
        rank = [0] * n

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        components = n
        for a, b in edges:
            ra, rb = find(a), find(b)
            if ra != rb:
                if rank[ra] < rank[rb]:
                    ra, rb = rb, ra
                parent[rb] = ra
                if rank[ra] == rank[rb]:
                    rank[ra] += 1
                components -= 1
        return components
```

### Complexity
- **Time**: O(n + E·α(n)) ≈ O(n + E).
- **Space**: O(n) for the DSU arrays.

---

## Approach 2 — DFS counting components

### Intuition
Build an adjacency list. Walk every node; whenever you find one not yet visited, that node opens a new component — increment the counter and DFS to mark the whole cluster visited.

### Algorithm
1. Build the undirected adjacency list.
2. `visited` all false; `count = 0`.
3. For each node `i`: if not visited, `count++` and `dfs(i)` to mark its component.
4. Return `count`.

### Dry run on Example 2 (one chain, n=5)
```
adj: 0-1, 1-2, 2-3, 3-4.
i=0 unvisited → count=1, DFS marks 0,1,2,3,4.
i=1..4 already visited → no new components.
Answer = 1.
```

### Code

```cpp
class Solution {
    vector<vector<int>> adj;
    vector<bool> visited;
    void dfs(int u) {
        visited[u] = true;
        for (int v : adj[u])
            if (!visited[v]) dfs(v);
    }
public:
    int countComponents(int n, vector<vector<int>>& edges) {
        adj.assign(n, {});
        visited.assign(n, false);
        for (auto& e : edges) {
            adj[e[0]].push_back(e[1]);
            adj[e[1]].push_back(e[0]);
        }
        int count = 0;
        for (int i = 0; i < n; i++)
            if (!visited[i]) { count++; dfs(i); }
        return count;
    }
};
```
```java
class Solution {
    private List<List<Integer>> adj;
    private boolean[] visited;

    public int countComponents(int n, int[][] edges) {
        adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        visited = new boolean[n];
        for (int[] e : edges) {
            adj.get(e[0]).add(e[1]);
            adj.get(e[1]).add(e[0]);
        }
        int count = 0;
        for (int i = 0; i < n; i++)
            if (!visited[i]) { count++; dfs(i); }
        return count;
    }

    private void dfs(int u) {
        visited[u] = true;
        for (int v : adj.get(u))
            if (!visited[v]) dfs(v);
    }
}
```
```python
class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        adj = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
        visited = [False] * n

        def dfs(u):
            visited[u] = True
            for v in adj[u]:
                if not visited[v]:
                    dfs(v)

        count = 0
        for i in range(n):
            if not visited[i]:
                count += 1
                dfs(i)
        return count
```

### Complexity
- **Time**: O(n + E).
- **Space**: O(n + E) for the adjacency list plus O(n) recursion/visited.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Union-Find | O(n + E·α) | O(n) | least memory; great for streaming edges ⭐ |
| DFS counting | O(n + E) | O(n + E) | intuitive; needs the adjacency list |

Union-Find avoids building an adjacency list and reads each edge once, making it the leanest. DFS/BFS counting is the most direct mental model. All are linear in practice.

---

## 🧪 Edge cases & pitfalls
- **No edges** → `n` components (each node isolated).
- **All nodes in one chain/tree** → 1 component.
- **Undirected edges in DFS**: you must add the edge **both ways** in the adjacency list, otherwise you miss reverse traversal.
- **Path compression matters**: a naive `find` without it can degrade to O(n) per call on a long chain.
- **Single node, no edges** → 1.

---

## 🔗 Related problems
- **Number of Islands** (LC 200) — connected components on a grid.
- **Graph Valid Tree** (LC 261) — 1 component AND exactly n−1 edges.
- **Redundant Connection** (LC 684) — DSU detects the edge that merges an already-connected pair.
- **Number of Provinces** (LC 547) — components from an adjacency matrix.

---

**→ Next:** [`10-Redundant-Connection.md`](./10-Redundant-Connection.md) | **← Prev:** [`08-Course-Schedule-II.md`](./08-Course-Schedule-II.md) | [Problem set index](./00-Index.md)
