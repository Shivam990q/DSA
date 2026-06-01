# Longest Increasing Path in a Matrix

**Platform**: LeetCode 329 · **Difficulty**: Hard · **Topics**: Array, DFS, BFS, Graph, Topological Sort, Memoization, Matrix · **Pattern**: DFS + memoization on an implicit DAG

---

## 📜 Problem Statement

Given an `m x n` integers `matrix`, return the **length of the longest increasing path** in `matrix`.

From each cell, you can move in **four directions**: left, right, up, or down. You **may not** move diagonally or move outside the boundary (i.e., wrap-around is not allowed).

### Examples

**Example 1:**
```
Input:  matrix = [[9,9,4],
                  [6,6,8],
                  [2,1,1]]
Output: 4
Explanation: The longest increasing path is [1, 2, 6, 9].
```

**Example 2:**
```
Input:  matrix = [[3,4,5],
                  [3,2,6],
                  [2,2,1]]
Output: 4
Explanation: The longest increasing path is [3, 4, 5, 6]. Moving diagonally is not allowed.
```

**Example 3:**
```
Input:  matrix = [[1]]
Output: 1
```

### Constraints
```
m == matrix.length
n == matrix[i].length
1 <= m, n <= 200
0 <= matrix[i][j] <= 2^31 - 1
```

---

## 🧠 Understanding the problem

We want the longest chain of **strictly increasing** cell values where consecutive cells are 4-directionally adjacent. The key structural observation:

> Build a directed graph: put an edge from cell `u` to neighbor `v` whenever `value(v) > value(u)`. Because every edge goes from a smaller value to a strictly larger one, the graph has **no cycles** — it's a **DAG**.

On a DAG, the longest path *starting at a cell* depends only on that cell, never on how we arrived. So `memo[r][c]` = length of the longest increasing path beginning at `(r, c)` is well-defined and reusable. That turns an exponential search into O(m·n).

5-step framework:
1. **State**: `memo[r][c]` = longest strictly increasing path starting at `(r, c)`.
2. **Transition**: `memo[r][c] = 1 + max(memo[nr][nc])` over neighbors with `value > value(r,c)` (0 if none).
3. **Base case**: a cell with no larger neighbor contributes length 1.
4. **Order**: DFS computes dependencies on demand; memo prevents recomputation.
5. **Answer**: `max(memo)` over all cells.

---

## Approach 1 — Brute-force DFS (no memo)

### Intuition
From every cell, DFS to all strictly-larger neighbors, returning `1 + best child`. No caching.

### Algorithm
1. `dfs(r, c)` returns `1 + max(dfs of larger neighbors)`.
2. Answer = max over all start cells.

### Dry run on Example 1
```
dfs(2,1)=1 (value 1): neighbor (2,0)=2 larger -> dfs(2,0)
dfs(2,0)=2: neighbor (1,0)=6 larger -> dfs(1,0)
dfs(1,0)=6: neighbor (0,0)=9 larger -> dfs(0,0)=9 leaf
so path 1->2->6->9 length 4
```

### Code
```cpp
class Solution {
    int m, n;
    int dfs(vector<vector<int>>& g, int r, int c) {
        int best = 1;
        int dr[] = {1,-1,0,0}, dc[] = {0,0,1,-1};
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr >= 0 && nc >= 0 && nr < m && nc < n && g[nr][nc] > g[r][c])
                best = max(best, 1 + dfs(g, nr, nc));
        }
        return best;
    }
public:
    int longestIncreasingPath(vector<vector<int>>& matrix) {
        m = matrix.size(); n = matrix[0].size();
        int ans = 0;
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++)
                ans = max(ans, dfs(matrix, r, c));
        return ans;
    }
};
```
```java
class Solution {
    private int m, n;
    private final int[] dr = {1,-1,0,0}, dc = {0,0,1,-1};
    private int dfs(int[][] g, int r, int c) {
        int best = 1;
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr >= 0 && nc >= 0 && nr < m && nc < n && g[nr][nc] > g[r][c])
                best = Math.max(best, 1 + dfs(g, nr, nc));
        }
        return best;
    }
    public int longestIncreasingPath(int[][] matrix) {
        m = matrix.length; n = matrix[0].length;
        int ans = 0;
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++)
                ans = Math.max(ans, dfs(matrix, r, c));
        return ans;
    }
}
```
```python
class Solution:
    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        m, n = len(matrix), len(matrix[0])

        def dfs(r: int, c: int) -> int:
            best = 1
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:
                    best = max(best, 1 + dfs(nr, nc))
            return best

        return max(dfs(r, c) for r in range(m) for c in range(n))
```

### Complexity
- **Time**: exponential in the worst case (paths overlap and are recomputed).
- **Space**: O(m·n) recursion depth.

### Verdict
Correct but recomputes shared sub-paths. The single missing ingredient is memoization.

---

## Approach 2 — DFS + memoization (optimal) ⭐

### Intuition
Cache `memo[r][c]` the first time it's computed. Each cell is then expanded once; subsequent visits read the cached value in O(1).

### Algorithm
1. `memo` initialized to 0 (= "not computed").
2. `dfs(r, c)`: if cached, return it; else compute `1 + max(dfs larger neighbors)`, store, return.
3. Answer = max over all cells.

### Dry run on Example 2
```
memo fills as DFS explores; e.g. cell with value 3 -> 4 -> 5 -> 6 gives 4
shared subresults (e.g. the chain to 6) are reused, not recomputed
answer = 4
```

### Code
```cpp
class Solution {
    int m, n;
    int dfs(vector<vector<int>>& g, int r, int c, vector<vector<int>>& memo) {
        if (memo[r][c]) return memo[r][c];
        int best = 1;
        int dr[] = {1,-1,0,0}, dc[] = {0,0,1,-1};
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr >= 0 && nc >= 0 && nr < m && nc < n && g[nr][nc] > g[r][c])
                best = max(best, 1 + dfs(g, nr, nc, memo));
        }
        return memo[r][c] = best;
    }
public:
    int longestIncreasingPath(vector<vector<int>>& matrix) {
        m = matrix.size(); n = matrix[0].size();
        vector<vector<int>> memo(m, vector<int>(n, 0));
        int ans = 0;
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++)
                ans = max(ans, dfs(matrix, r, c, memo));
        return ans;
    }
};
```
```java
class Solution {
    private int m, n;
    private final int[] dr = {1,-1,0,0}, dc = {0,0,1,-1};
    private int dfs(int[][] g, int r, int c, int[][] memo) {
        if (memo[r][c] != 0) return memo[r][c];
        int best = 1;
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr >= 0 && nc >= 0 && nr < m && nc < n && g[nr][nc] > g[r][c])
                best = Math.max(best, 1 + dfs(g, nr, nc, memo));
        }
        return memo[r][c] = best;
    }
    public int longestIncreasingPath(int[][] matrix) {
        m = matrix.length; n = matrix[0].length;
        int[][] memo = new int[m][n];
        int ans = 0;
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++)
                ans = Math.max(ans, dfs(matrix, r, c, memo));
        return ans;
    }
}
```
```python
class Solution:
    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        from functools import lru_cache
        m, n = len(matrix), len(matrix[0])

        @lru_cache(maxsize=None)
        def dfs(r: int, c: int) -> int:
            best = 1
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:
                    best = max(best, 1 + dfs(nr, nc))
            return best

        return max(dfs(r, c) for r in range(m) for c in range(n))
```

### Complexity
- **Time**: O(m × n) — each cell computed once, constant neighbors.
- **Space**: O(m × n) memo + recursion depth.

### Verdict
**The standard optimal.** Memoized DFS is exactly DP on the DAG.

---

## Approach 3 — Topological sort by peeling (iterative, no recursion)

### Intuition
Avoid recursion by processing cells from "peaks" inward. Treat each cell's **out-degree** = number of strictly-larger neighbors. Cells with out-degree 0 are local maxima (path length 1). Peel them like Kahn's algorithm: removing a cell decrements the out-degree of smaller neighbors; the number of peeling rounds is the answer.

### Algorithm
1. Compute out-degree for every cell (edges to larger neighbors).
2. Queue all cells with out-degree 0.
3. BFS in layers; each layer is one more unit of path length. When a cell is dequeued, for each *smaller* neighbor decrement its out-degree; if it hits 0, enqueue it.
4. The number of layers processed is the longest path.

### Code
```cpp
class Solution {
public:
    int longestIncreasingPath(vector<vector<int>>& matrix) {
        int m = matrix.size(), n = matrix[0].size();
        vector<vector<int>> out(m, vector<int>(n, 0));
        int dr[] = {1,-1,0,0}, dc[] = {0,0,1,-1};
        queue<pair<int,int>> q;
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++) {
                for (int d = 0; d < 4; d++) {
                    int nr = r+dr[d], nc = c+dc[d];
                    if (nr>=0 && nc>=0 && nr<m && nc<n && matrix[nr][nc] > matrix[r][c])
                        out[r][c]++;
                }
                if (out[r][c] == 0) q.push({r, c});
            }
        int layers = 0;
        while (!q.empty()) {
            layers++;
            int sz = q.size();
            while (sz--) {
                auto [r, c] = q.front(); q.pop();
                for (int d = 0; d < 4; d++) {
                    int nr = r+dr[d], nc = c+dc[d];
                    if (nr>=0 && nc>=0 && nr<m && nc<n && matrix[nr][nc] < matrix[r][c])
                        if (--out[nr][nc] == 0) q.push({nr, nc});
                }
            }
        }
        return layers;
    }
};
```
```java
class Solution {
    public int longestIncreasingPath(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        int[][] out = new int[m][n];
        int[] dr = {1,-1,0,0}, dc = {0,0,1,-1};
        java.util.Queue<int[]> q = new java.util.ArrayDeque<>();
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++) {
                for (int d = 0; d < 4; d++) {
                    int nr = r+dr[d], nc = c+dc[d];
                    if (nr>=0 && nc>=0 && nr<m && nc<n && matrix[nr][nc] > matrix[r][c])
                        out[r][c]++;
                }
                if (out[r][c] == 0) q.add(new int[]{r, c});
            }
        int layers = 0;
        while (!q.isEmpty()) {
            layers++;
            int sz = q.size();
            while (sz-- > 0) {
                int[] cell = q.poll();
                int r = cell[0], c = cell[1];
                for (int d = 0; d < 4; d++) {
                    int nr = r+dr[d], nc = c+dc[d];
                    if (nr>=0 && nc>=0 && nr<m && nc<n && matrix[nr][nc] < matrix[r][c])
                        if (--out[nr][nc] == 0) q.add(new int[]{nr, nc});
                }
            }
        }
        return layers;
    }
}
```
```python
class Solution:
    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        from collections import deque
        m, n = len(matrix), len(matrix[0])
        out = [[0] * n for _ in range(m)]
        dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
        q = deque()
        for r in range(m):
            for c in range(n):
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:
                        out[r][c] += 1
                if out[r][c] == 0:
                    q.append((r, c))
        layers = 0
        while q:
            layers += 1
            for _ in range(len(q)):
                r, c = q.popleft()
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] < matrix[r][c]:
                        out[nr][nc] -= 1
                        if out[nr][nc] == 0:
                            q.append((nr, nc))
        return layers
```

### Complexity
- **Time**: O(m × n).
- **Space**: O(m × n).

### Verdict
Same complexity, no recursion stack — safer for very deep paths. A great way to *show* the DAG structure explicitly.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute DFS | exponential | O(mn) | baseline, recomputes |
| DFS + memo | **O(mn)** | O(mn) | the standard answer ⭐ |
| Topological peeling | O(mn) | O(mn) | iterative, no recursion |

---

## 🧪 Edge cases & pitfalls
- **Single cell** → 1.
- **All equal values** → 1 (strict increase means no edges).
- **Strictly sorted snake** → can reach `m·n` (a Hamiltonian increasing path).
- **Pitfall — forgetting memo resets nothing**: `memo == 0` doubles as "uncomputed" because every real path length is ≥ 1. Clean sentinel.
- **Pitfall — `>=` vs `>`**: edges require **strictly** greater neighbors. Using `>=` would create cycles among equal cells and break the DAG assumption.
- **Pitfall — deep recursion**: up to 200×200 = 40000 cells; a degenerate path can recurse that deep. Either rely on a generous stack or use the topological approach.

---

## 🔗 Related problems
- **Longest Increasing Subsequence** (LC 300) — the 1D ancestor of this idea.
- **Course Schedule** (LC 207) / **II** (LC 210) — topological sorting on explicit DAGs.
- **Pacific Atlantic Water Flow** (LC 417) — multi-source grid DFS with monotonic moves.
- **Number of Increasing Paths in a Grid** (LC 2328) — count (not just length) increasing paths.

---

**→ Next:** [`09-Best-Time-Buy-Sell-Cooldown.md`](./09-Best-Time-Buy-Sell-Cooldown.md) | **→ Prev:** [`07-Interleaving-String.md`](./07-Interleaving-String.md) | Back to [`00-Index.md`](./00-Index.md)
