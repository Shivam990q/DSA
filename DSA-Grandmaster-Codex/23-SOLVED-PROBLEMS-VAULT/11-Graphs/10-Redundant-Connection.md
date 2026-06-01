# Redundant Connection

**Platform**: LeetCode 684 · **Difficulty**: Medium · **Topics**: DFS, BFS, Union-Find, Graph · **Pattern**: Cycle-creating edge via DSU

---

## 📜 Problem Statement

In this problem, a tree is an **undirected graph** that is connected and has no cycles.

You are given a graph that started as a tree with `n` nodes labeled from `1` to `n`, with one additional edge added. The added edge has two **different** vertices chosen from `1` to `n`, and was not an edge that already existed. The graph is represented as an array `edges` of length `n` where `edges[i] = [ai, bi]` indicates that there is an edge between nodes `ai` and `bi` in the graph.

Return *an edge that can be removed so that the resulting graph is a tree of `n` nodes*. If there are multiple answers, return the answer that occurs **last** in the input.

### Examples

**Example 1:**
```
Input: edges = [[1,2],[1,3],[2,3]]
Output: [2,3]
Explanation: Adding [2,3] closes the cycle 1-2-3-1. Removing it restores a tree.
```

**Example 2:**
```
Input: edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
Output: [1,4]
Explanation: The cycle is 1-2-3-4-1. The edge [1,4] is the one that closes it.
```

**Example 3:**
```
Input: edges = [[1,2],[1,3],[2,3]]
Output: [2,3]
```

### Constraints
```
n == edges.length
3 <= n <= 1000
edges[i].length == 2
1 <= ai < bi <= n
ai != bi
There are no repeated edges.
The given graph is connected.
```

---

## 🧠 Understanding the problem

We have a tree (`n` nodes, `n−1` edges, no cycle) with **exactly one extra edge** added, making `n` edges total and creating **exactly one cycle**. We must return the edge that, when removed, makes it a tree again — and if several edges lie on the cycle, return the **one that appears last** in the input.

Key observation: process the edges **in input order** and incrementally connect nodes. A tree edge always joins two **previously unconnected** components. The **first** edge whose two endpoints are *already* connected is the edge that closes the cycle — and because we scan left to right, it is automatically the last such edge in input order. That edge is the answer.

This is the textbook use of **Union-Find**: `find` to test connectivity, `union` to merge. Constraints are tiny (n ≤ 1000), so the only real subtlety is the "return the last one" requirement, which the in-order scan satisfies naturally.

---

## Approach 1 — Union-Find (recommended) ⭐

### Intuition
Build the graph edge by edge. Union endpoints that are in different sets. The moment an edge connects two nodes already in the same set, adding it would create a cycle — that's the redundant edge.

### Algorithm
1. `parent[i] = i` for `i` in `1..n`.
2. For each edge `(a, b)` in order:
   - If `find(a) == find(b)` → return `(a, b)` (it closes a cycle).
   - Else union them.
3. (Problem guarantees an answer exists.)

### Dry run on Example 2 (`[1,2],[2,3],[3,4],[1,4],[1,5]`)
```
[1,2]: find(1)=1, find(2)=2 → union.
[2,3]: find(2)=1, find(3)=3 → union.
[3,4]: find(3)=1, find(4)=4 → union.   (now {1,2,3,4} connected)
[1,4]: find(1)=1, find(4)=1 → SAME → return [1,4].
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
    vector<int> findRedundantConnection(vector<vector<int>>& edges) {
        int n = edges.size();
        parent.resize(n + 1);
        rnk.assign(n + 1, 0);
        iota(parent.begin(), parent.end(), 0);
        for (auto& e : edges) {
            int ra = find(e[0]), rb = find(e[1]);
            if (ra == rb) return e;          // already connected → cycle
            if (rnk[ra] < rnk[rb]) swap(ra, rb);
            parent[rb] = ra;
            if (rnk[ra] == rnk[rb]) rnk[ra]++;
        }
        return {};
    }
};
```
```java
class Solution {
    private int[] parent, rank;

    public int[] findRedundantConnection(int[][] edges) {
        int n = edges.length;
        parent = new int[n + 1];
        rank = new int[n + 1];
        for (int i = 0; i <= n; i++) parent[i] = i;
        for (int[] e : edges) {
            int ra = find(e[0]), rb = find(e[1]);
            if (ra == rb) return e;
            if (rank[ra] < rank[rb]) { int t = ra; ra = rb; rb = t; }
            parent[rb] = ra;
            if (rank[ra] == rank[rb]) rank[ra]++;
        }
        return new int[0];
    }

    private int find(int x) {
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }
}
```
```python
class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        parent = list(range(n + 1))
        rank = [0] * (n + 1)

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for a, b in edges:
            ra, rb = find(a), find(b)
            if ra == rb:
                return [a, b]
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1
        return []
```

### Complexity
- **Time**: O(n·α(n)) ≈ O(n).
- **Space**: O(n) for the DSU arrays.

---

## Approach 2 — DFS connectivity check before adding each edge

### Intuition
Without DSU, you can still detect the closing edge: before adding edge `(a, b)`, check whether `a` and `b` are *already* connected using a DFS/BFS over the edges added so far. If they are, `(a, b)` is redundant.

### Algorithm
1. Maintain an adjacency list of edges added so far.
2. For each edge `(a, b)`:
   - If a DFS from `a` already reaches `b` → return `(a, b)`.
   - Otherwise add the edge to the adjacency list (both directions).

### Dry run on Example 1 (`[1,2],[1,3],[2,3]`)
```
[1,2]: 1 cannot reach 2 (graph empty) → add edge.
[1,3]: 1 cannot reach 3 → add edge.
[2,3]: DFS from 2: 2→1→3 reaches 3 → already connected → return [2,3].
```

### Code

```cpp
class Solution {
    vector<vector<int>> adj;
    bool dfs(int u, int target, vector<bool>& seen) {
        if (u == target) return true;
        seen[u] = true;
        for (int v : adj[u])
            if (!seen[v] && dfs(v, target, seen)) return true;
        return false;
    }
public:
    vector<int> findRedundantConnection(vector<vector<int>>& edges) {
        int n = edges.size();
        adj.assign(n + 1, {});
        for (auto& e : edges) {
            vector<bool> seen(n + 1, false);
            if (!adj[e[0]].empty() && !adj[e[1]].empty() && dfs(e[0], e[1], seen))
                return e;
            adj[e[0]].push_back(e[1]);
            adj[e[1]].push_back(e[0]);
        }
        return {};
    }
};
```
```java
class Solution {
    private List<List<Integer>> adj;

    public int[] findRedundantConnection(int[][] edges) {
        int n = edges.length;
        adj = new ArrayList<>();
        for (int i = 0; i <= n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) {
            boolean[] seen = new boolean[n + 1];
            if (!adj.get(e[0]).isEmpty() && !adj.get(e[1]).isEmpty()
                && dfs(e[0], e[1], seen))
                return e;
            adj.get(e[0]).add(e[1]);
            adj.get(e[1]).add(e[0]);
        }
        return new int[0];
    }

    private boolean dfs(int u, int target, boolean[] seen) {
        if (u == target) return true;
        seen[u] = true;
        for (int v : adj.get(u))
            if (!seen[v] && dfs(v, target, seen)) return true;
        return false;
    }
}
```
```python
class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        adj = [[] for _ in range(n + 1)]

        def dfs(u, target, seen):
            if u == target:
                return True
            seen[u] = True
            for v in adj[u]:
                if not seen[v] and dfs(v, target, seen):
                    return True
            return False

        for a, b in edges:
            if adj[a] and adj[b] and dfs(a, b, [False] * (n + 1)):
                return [a, b]
            adj[a].append(b)
            adj[b].append(a)
        return []
```

### Complexity
- **Time**: O(n²) — up to a full DFS (O(n)) per edge.
- **Space**: O(n) for the adjacency list and the visited array.

### Verdict
Correct and intuitive, but quadratic. Fine for n ≤ 1000, yet union-find is strictly better and just as short.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Union-Find | O(n·α) | O(n) | first "already-connected" edge = answer ⭐ |
| DFS per edge | O(n²) | O(n) | no DSU needed; slower |

The in-order scan is what guarantees we return the *last* cycle edge: since exactly one cycle exists, the first edge that finds its endpoints already connected is precisely the latest edge completing that cycle.

---

## 🧪 Edge cases & pitfalls
- **The answer must be the last cycle-closing edge** — scanning edges in input order delivers this automatically; do not sort or reorder.
- **1-indexed nodes** — size the `parent` array as `n + 1` and ignore index 0.
- **Forgetting union after a non-cycle edge** breaks connectivity tracking and yields a wrong answer.
- In the DFS variant, guard against DFS-ing into nodes with no edges yet (minor optimization) and reset `seen` per edge.
- The graph is guaranteed connected with exactly one extra edge, so an answer always exists.

---

## 🔗 Related problems
- **Redundant Connection II** (LC 685) — directed version; handle in-degree-2 nodes plus cycles.
- **Number of Connected Components** (LC 323) — DSU component counting.
- **Graph Valid Tree** (LC 261) — DSU detects any cycle (return false instead of the edge).
- **Accounts Merge** (LC 721) — DSU to merge overlapping groups.

---

**→ Next:** [`11-Word-Ladder.md`](./11-Word-Ladder.md) | **← Prev:** [`09-Number-of-Connected-Components.md`](./09-Number-of-Connected-Components.md) | [Problem set index](./00-Index.md)
