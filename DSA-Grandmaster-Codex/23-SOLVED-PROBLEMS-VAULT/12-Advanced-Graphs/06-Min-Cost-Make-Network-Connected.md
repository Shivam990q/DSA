# Number of Operations to Make Network Connected

**Platform**: LeetCode 1319 · **Difficulty**: Medium · **Topics**: Graph, DFS, BFS, Union-Find · **Pattern**: Components + spare-edge counting

---

## 📜 Problem Statement

There are `n` computers numbered from `0` to `n - 1` connected by ethernet cables `connections` forming a network where `connections[i] = [ai, bi]` represents a connection between computers `ai` and `bi`. Any computer can reach any other computer directly or indirectly through the network.

You are given an initial computer network `connections`. You can extract certain cables between two directly connected computers, and place them between any pair of disconnected computers to make them directly connected.

Return *the **minimum number of times** you need to do this in order to make all the computers connected*. If it is not possible, return `-1`.

### Examples

**Example 1:**
```
Input: n = 4, connections = [[0,1],[0,2],[1,2]]
Output: 1
Explanation: Remove the redundant cable between 1 and 2 and place it
between 1 (or 2) and computer 3.
```

**Example 2:**
```
Input: n = 6, connections = [[0,1],[0,2],[0,3],[1,2],[1,3]]
Output: 2
Explanation: Two redundant cables can be moved to connect computers 4 and 5.
```

**Example 3:**
```
Input: n = 6, connections = [[0,1],[0,2],[0,3],[1,2]]
Output: -1
Explanation: There are not enough cables: only 4 cables for 6 computers
(need at least 5).
```

### Constraints
```
1 <= n <= 10^5
1 <= connections.length <= min(n * (n - 1) / 2, 10^5)
connections[i].length == 2
0 <= ai, bi < n
ai != bi
There are no repeated connections.
No two computers are connected by more than one cable.
```

---

## 🧠 Understanding the problem

To connect `n` computers you need **at least `n − 1` cables**. So the first check is purely about supply:

> If `connections.length < n − 1`, it is impossible → return `-1`.

If you have enough cables, the question becomes: how many cable moves to merge everything into one network? Suppose the current network has `c` connected components. To fuse `c` components into one, you need to add **`c − 1` bridging cables**. And whenever you have a *redundant* cable (one inside a component that is already connected — part of a cycle), you can free it and reuse it as a bridge.

Here is the elegant part: **if `connections.length ≥ n − 1`, you are always guaranteed to have at least `c − 1` redundant cables to move.** Why? A spanning forest of `c` components uses exactly `n − c` cables; any cables beyond that are redundant. Since total cables `≥ n − 1 = (n − c) + (c − 1)`, there are at least `c − 1` spare cables — exactly enough. So the answer is simply **`c − 1`** once the supply check passes.

So the whole problem reduces to: count connected components `c`, and the answer is `c − 1` (or `-1` if too few cables).

---

## Approach 1 — Union-Find (recommended) ⭐

### Intuition
Count components with DSU. Each successful union (joining two different sets) drops the component count. After processing all cables, the number of components is `c`, and the answer is `c − 1` — provided we had at least `n − 1` cables.

### Algorithm
1. If `connections.size() < n − 1` → return `-1`.
2. DSU over `n` nodes; `components = n`.
3. For each cable `(a, b)`: if `find(a) != find(b)`, union and `components--`.
4. Return `components − 1`.

### Dry run on Example 1 (`n=4`, `[[0,1],[0,2],[1,2]]`)
```
cables = 3 >= n-1 = 3 → possible.
components=4.
[0,1]: differ → union → components=3.
[0,2]: differ → union → components=2.
[1,2]: 1 and 2 already in same set → no change (this is the redundant cable).
final components = 2 (set {0,1,2} and {3}). answer = 2 - 1 = 1. ✓
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
    int makeConnected(int n, vector<vector<int>>& connections) {
        if ((int)connections.size() < n - 1) return -1;
        parent.resize(n);
        rnk.assign(n, 0);
        iota(parent.begin(), parent.end(), 0);
        int components = n;
        for (auto& c : connections) {
            int ra = find(c[0]), rb = find(c[1]);
            if (ra != rb) {
                if (rnk[ra] < rnk[rb]) swap(ra, rb);
                parent[rb] = ra;
                if (rnk[ra] == rnk[rb]) rnk[ra]++;
                components--;
            }
        }
        return components - 1;
    }
};
```
```java
class Solution {
    private int[] parent, rank;

    public int makeConnected(int n, int[][] connections) {
        if (connections.length < n - 1) return -1;
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        int components = n;
        for (int[] c : connections) {
            int ra = find(c[0]), rb = find(c[1]);
            if (ra != rb) {
                if (rank[ra] < rank[rb]) { int t = ra; ra = rb; rb = t; }
                parent[rb] = ra;
                if (rank[ra] == rank[rb]) rank[ra]++;
                components--;
            }
        }
        return components - 1;
    }

    private int find(int x) {
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }
}
```
```python
class Solution:
    def makeConnected(self, n: int, connections: List[List[int]]) -> int:
        if len(connections) < n - 1:
            return -1
        parent = list(range(n))
        rank = [0] * n

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        components = n
        for a, b in connections:
            ra, rb = find(a), find(b)
            if ra != rb:
                if rank[ra] < rank[rb]:
                    ra, rb = rb, ra
                parent[rb] = ra
                if rank[ra] == rank[rb]:
                    rank[ra] += 1
                components -= 1
        return components - 1
```

### Complexity
- **Time**: O(n + E·α(n)) ≈ O(n + E).
- **Space**: O(n) for the DSU arrays.

---

## Approach 2 — DFS component counting

### Intuition
After the supply check, just count connected components with a DFS over the adjacency list. Each new DFS launch from an unvisited node marks one component. The answer is `components − 1`.

### Algorithm
1. If `connections.size() < n − 1` → return `-1`.
2. Build the undirected adjacency list.
3. For each unvisited node, `components++` and DFS to mark its whole component.
4. Return `components − 1`.

### Dry run on Example 2 (`n=6`, edges among {0,1,2,3})
```
cables = 5 >= 5 → possible.
DFS from 0 marks {0,1,2,3} → components=1.
Node 4 unvisited → components=2 (isolated).
Node 5 unvisited → components=3 (isolated).
answer = 3 - 1 = 2. ✓
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
    int makeConnected(int n, vector<vector<int>>& connections) {
        if ((int)connections.size() < n - 1) return -1;
        adj.assign(n, {});
        visited.assign(n, false);
        for (auto& c : connections) {
            adj[c[0]].push_back(c[1]);
            adj[c[1]].push_back(c[0]);
        }
        int components = 0;
        for (int i = 0; i < n; i++)
            if (!visited[i]) { components++; dfs(i); }
        return components - 1;
    }
};
```
```java
class Solution {
    private List<List<Integer>> adj;
    private boolean[] visited;

    public int makeConnected(int n, int[][] connections) {
        if (connections.length < n - 1) return -1;
        adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        visited = new boolean[n];
        for (int[] c : connections) {
            adj.get(c[0]).add(c[1]);
            adj.get(c[1]).add(c[0]);
        }
        int components = 0;
        for (int i = 0; i < n; i++)
            if (!visited[i]) { components++; dfs(i); }
        return components - 1;
    }

    private void dfs(int u) {
        visited[u] = true;
        for (int v : adj.get(u))
            if (!visited[v]) dfs(v);
    }
}
```
```python
import sys

class Solution:
    def makeConnected(self, n: int, connections: List[List[int]]) -> int:
        if len(connections) < n - 1:
            return -1
        adj = [[] for _ in range(n)]
        for a, b in connections:
            adj[a].append(b)
            adj[b].append(a)
        visited = [False] * n

        sys.setrecursionlimit(200000)

        def dfs(u):
            visited[u] = True
            for v in adj[u]:
                if not visited[v]:
                    dfs(v)

        components = 0
        for i in range(n):
            if not visited[i]:
                components += 1
                dfs(i)
        return components - 1
```

### Complexity
- **Time**: O(n + E).
- **Space**: O(n + E) for the adjacency list plus O(n) recursion/visited.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Union-Find | O(n + E·α) | O(n) | no adjacency list; minimal memory ⭐ |
| DFS counting | O(n + E) | O(n + E) | intuitive; watch recursion depth at n = 10⁵ |

Both compute the same `components − 1`. Union-Find is leaner (no adjacency list) and avoids the deep-recursion concern that DFS faces at the upper bound (use an iterative DFS/BFS if you go that route). The conceptual heart is the same: **answer = components − 1, after confirming `cables ≥ n − 1`.**

---

## 🧪 Edge cases & pitfalls
- **Too few cables** (`< n − 1`) → `-1`. This check must come first.
- **Already fully connected** → 1 component → `0` moves.
- **You never need to count redundant cables explicitly** — the supply check guarantees enough spares exist, so `components − 1` is always achievable.
- **Recursion depth**: at `n = 10⁵`, a recursive DFS over one giant chain can overflow the stack; prefer Union-Find or an iterative traversal.
- **Undirected edges in DFS** — add both directions in the adjacency list.

---

## 🔗 Related problems
- **Number of Connected Components** (LC 323) — the core component count this builds on.
- **Graph Valid Tree** (LC 261) — `n − 1` edges + connected ⇒ tree.
- **Min Cost to Connect All Points** (LC 1584) — weighted connection (MST).
- **Redundant Connection** (LC 684) — identify the spare (cycle-closing) cable.

---

**← Prev:** [`05-Reconstruct-Itinerary.md`](./05-Reconstruct-Itinerary.md) | [Problem set index](./00-Index.md) | **→ Next topic:** [`../13-1D-Dynamic-Programming/00-Index.md`](../13-1D-Dynamic-Programming/00-Index.md)
