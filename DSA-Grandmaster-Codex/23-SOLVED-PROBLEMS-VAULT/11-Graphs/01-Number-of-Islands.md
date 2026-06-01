# Number of Islands

**Platform**: LeetCode 200 · **Difficulty**: Medium · **Topics**: Array, DFS, BFS, Union-Find, Matrix · **Pattern**: Grid flood-fill

---

## 📜 Problem Statement

Given an `m x n` 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return *the number of islands*.

An **island** is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.

### Examples

**Example 1:**
```
Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1
Explanation: All the 1s connect into a single island.
```

**Example 2:**
```
Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3
Explanation: Top-left block, the single cell in the middle, and the bottom-right pair.
```

**Example 3:**
```
Input: grid = [["1"]]
Output: 1
```

### Constraints
```
m == grid.length
n == grid[i].length
1 <= m, n <= 300
grid[i][j] is '0' or '1'.
```

---

## 🧠 Understanding the problem

An "island" is exactly a **connected component** of `'1'` cells, where "connected" means reachable through up/down/left/right moves (no diagonals). So the question "how many islands?" is precisely "how many connected components of land are there?"

The classic trick: scan the grid cell by cell. The moment we hit a land cell we have not visited, we have discovered a *new* island — increment the counter, then **flood-fill** (traverse and mark) the whole component so we never count any of its cells again. Because every land cell is consumed by exactly one flood-fill, the number of times we *start* a flood-fill equals the number of islands.

Grid size is up to 300 × 300 = 90,000 cells, so any linear pass over the grid is fast.

---

## Approach 1 — DFS flood-fill (recommended) ⭐

### Intuition
When you step onto fresh land, you want to "claim" the entire island so it is counted once. Depth-first search naturally walks outward from a cell to every reachable land cell. We mark each visited land cell as `'0'` (sink it) so it cannot be revisited or recounted.

### Algorithm
1. Initialize `count = 0`.
2. For every cell `(r, c)`:
   - If `grid[r][c] == '1'`, increment `count` and run `dfs(r, c)`.
3. `dfs(r, c)`:
   - If out of bounds or the cell is not `'1'`, return.
   - Set `grid[r][c] = '0'` (mark visited).
   - Recurse into the four neighbors.
4. Return `count`.

### Dry run on Example 2
```
Scan row 0: (0,0)='1' → count=1, DFS sinks the whole top-left 2x2 block.
            remaining cells in that block are now '0'.
Continue scanning... (2,2)='1' → count=2, DFS sinks that lone cell.
Continue... (3,3)='1' → count=3, DFS sinks (3,3) and (3,4).
No more '1's → answer = 3.
```

### Code

```cpp
class Solution {
public:
    int numIslands(vector<vector<char>>& grid) {
        int rows = grid.size(), cols = grid[0].size(), count = 0;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (grid[r][c] == '1') {
                    count++;
                    dfs(grid, r, c);
                }
        return count;
    }
private:
    void dfs(vector<vector<char>>& grid, int r, int c) {
        if (r < 0 || c < 0 || r >= (int)grid.size() || c >= (int)grid[0].size()
            || grid[r][c] != '1')
            return;
        grid[r][c] = '0';
        dfs(grid, r + 1, c);
        dfs(grid, r - 1, c);
        dfs(grid, r, c + 1);
        dfs(grid, r, c - 1);
    }
};
```
```java
class Solution {
    public int numIslands(char[][] grid) {
        int rows = grid.length, cols = grid[0].length, count = 0;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (grid[r][c] == '1') {
                    count++;
                    dfs(grid, r, c);
                }
        return count;
    }

    private void dfs(char[][] grid, int r, int c) {
        if (r < 0 || c < 0 || r >= grid.length || c >= grid[0].length
            || grid[r][c] != '1')
            return;
        grid[r][c] = '0';
        dfs(grid, r + 1, c);
        dfs(grid, r - 1, c);
        dfs(grid, r, c + 1);
        dfs(grid, r, c - 1);
    }
}
```
```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        rows, cols = len(grid), len(grid[0])

        def dfs(r, c):
            if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != '1':
                return
            grid[r][c] = '0'
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        count = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    count += 1
                    dfs(r, c)
        return count
```

### Complexity
- **Time**: O(m·n) — every cell is visited a constant number of times.
- **Space**: O(m·n) worst case — the recursion stack when the grid is one giant island (e.g., a long snake).

---

## Approach 2 — BFS flood-fill

### Intuition
Same flood-fill idea, but use an explicit queue instead of recursion. This avoids the deep call stack that can overflow on a 300 × 300 grid that is all land (90,000 deep recursion in some languages).

### Algorithm
1. For every unvisited land cell, increment `count` and BFS from it.
2. BFS: push the cell, mark it `'0'`, then repeatedly pop a cell and enqueue any neighboring `'1'` (marking each `'0'` as it is enqueued so it is queued once).

### Dry run on Example 2 (first island)
```
Start (0,0): queue=[(0,0)], mark '0'.
Pop (0,0): neighbors (1,0),(0,1) are '1' → mark '0', enqueue.
Pop (1,0): neighbor (1,1) is '1' → mark, enqueue.
Pop (0,1): neighbor (1,1) already '0'.
Pop (1,1): no new land. Queue empty → island fully sunk. count=1.
```

### Code

```cpp
class Solution {
public:
    int numIslands(vector<vector<char>>& grid) {
        int rows = grid.size(), cols = grid[0].size(), count = 0;
        int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (grid[r][c] == '1') {
                    count++;
                    queue<pair<int,int>> q;
                    q.push({r, c});
                    grid[r][c] = '0';
                    while (!q.empty()) {
                        auto [cr, cc] = q.front(); q.pop();
                        for (int d = 0; d < 4; d++) {
                            int nr = cr + dr[d], nc = cc + dc[d];
                            if (nr >= 0 && nc >= 0 && nr < rows && nc < cols
                                && grid[nr][nc] == '1') {
                                grid[nr][nc] = '0';
                                q.push({nr, nc});
                            }
                        }
                    }
                }
        return count;
    }
};
```
```java
class Solution {
    public int numIslands(char[][] grid) {
        int rows = grid.length, cols = grid[0].length, count = 0;
        int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (grid[r][c] == '1') {
                    count++;
                    Queue<int[]> q = new LinkedList<>();
                    q.offer(new int[]{r, c});
                    grid[r][c] = '0';
                    while (!q.isEmpty()) {
                        int[] cell = q.poll();
                        for (int d = 0; d < 4; d++) {
                            int nr = cell[0] + dr[d], nc = cell[1] + dc[d];
                            if (nr >= 0 && nc >= 0 && nr < rows && nc < cols
                                && grid[nr][nc] == '1') {
                                grid[nr][nc] = '0';
                                q.offer(new int[]{nr, nc});
                            }
                        }
                    }
                }
        return count;
    }
}
```
```python
from collections import deque

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        rows, cols = len(grid), len(grid[0])
        count = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    count += 1
                    q = deque([(r, c)])
                    grid[r][c] = '0'
                    while q:
                        cr, cc = q.popleft()
                        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                            nr, nc = cr + dr, cc + dc
                            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                                grid[nr][nc] = '0'
                                q.append((nr, nc))
        return count
```

### Complexity
- **Time**: O(m·n).
- **Space**: O(min(m, n)) for the queue in the worst case — strictly better stack behavior than recursive DFS.

---

## Approach 3 — Union-Find (Disjoint Set Union)

### Intuition
Treat each land cell as its own set. Walk the grid and **union** every land cell with its right and down land neighbors. After all unions, the number of distinct sets among land cells equals the number of islands. This shines when the grid is dynamic (e.g., the follow-up "Number of Islands II" where land is added one cell at a time).

### Algorithm
1. Map each cell `(r, c)` to a 1D id `r*cols + c`.
2. Initialize DSU; set component count = number of land cells.
3. For each land cell, union with its right and down neighbor if they are land (decrement count on a successful merge).
4. Return the final count.

### Dry run on Example 2 (top-left block)
```
Land cells (0,0),(0,1),(1,0),(1,1) start as 4 separate sets → count includes 4.
union (0,0)-(0,1): merge → count drops by 1.
union (0,0)-(1,0): merge → count drops by 1.
union (0,1)-(1,1): merge → count drops by 1.
union (1,0)-(1,1): already same set → no change.
The 2x2 block collapses to a single set → contributes 1 island.
```

### Code

```cpp
class Solution {
    vector<int> parent, rnk;
    int find(int x) {
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }
    void unite(int a, int b, int& count) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return;
        if (rnk[ra] < rnk[rb]) swap(ra, rb);
        parent[rb] = ra;
        if (rnk[ra] == rnk[rb]) rnk[ra]++;
        count--;
    }
public:
    int numIslands(vector<vector<char>>& grid) {
        int rows = grid.size(), cols = grid[0].size(), count = 0;
        parent.resize(rows * cols);
        rnk.assign(rows * cols, 0);
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (grid[r][c] == '1') { parent[r * cols + c] = r * cols + c; count++; }
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (grid[r][c] == '1') {
                    if (r + 1 < rows && grid[r + 1][c] == '1')
                        unite(r * cols + c, (r + 1) * cols + c, count);
                    if (c + 1 < cols && grid[r][c + 1] == '1')
                        unite(r * cols + c, r * cols + c + 1, count);
                }
        return count;
    }
};
```
```java
class Solution {
    private int[] parent, rank;
    private int count;

    public int numIslands(char[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        parent = new int[rows * cols];
        rank = new int[rows * cols];
        count = 0;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (grid[r][c] == '1') { parent[r * cols + c] = r * cols + c; count++; }
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (grid[r][c] == '1') {
                    if (r + 1 < rows && grid[r + 1][c] == '1')
                        unite(r * cols + c, (r + 1) * cols + c);
                    if (c + 1 < cols && grid[r][c + 1] == '1')
                        unite(r * cols + c, r * cols + c + 1);
                }
        return count;
    }

    private int find(int x) {
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }

    private void unite(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return;
        if (rank[ra] < rank[rb]) { int t = ra; ra = rb; rb = t; }
        parent[rb] = ra;
        if (rank[ra] == rank[rb]) rank[ra]++;
        count--;
    }
}
```
```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        rows, cols = len(grid), len(grid[0])
        parent = list(range(rows * cols))
        rank = [0] * (rows * cols)
        self.count = 0

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def unite(a, b):
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1
            self.count -= 1

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    self.count += 1

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    if r + 1 < rows and grid[r + 1][c] == '1':
                        unite(r * cols + c, (r + 1) * cols + c)
                    if c + 1 < cols and grid[r][c + 1] == '1':
                        unite(r * cols + c, r * cols + c + 1)
        return self.count
```

### Complexity
- **Time**: O(m·n·α(m·n)) ≈ O(m·n) with path compression + union by rank.
- **Space**: O(m·n) for the parent/rank arrays.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Mutates grid | When to use |
|----------|------|-------|--------------|-------------|
| DFS flood-fill | O(m·n) | O(m·n) stack | yes | default, cleanest to write ⭐ |
| BFS flood-fill | O(m·n) | O(min(m,n)) | yes | when recursion depth risks stack overflow |
| Union-Find | O(m·n·α) | O(m·n) | no | dynamic connectivity / "Islands II" follow-up |

All three are linear in the number of cells. DFS is the most concise; BFS is the safe choice for very large all-land grids; union-find is the tool you reach for when edges/land arrive incrementally.

---

## 🧪 Edge cases & pitfalls
- **Single cell** `[["1"]]` → 1; `[["0"]]` → 0. Loops handle both.
- **All water** → 0. **All land** → 1 (and deepest recursion — prefer BFS here).
- **Diagonal land is NOT connected** — only 4-directional moves count. A common bug is adding the 4 diagonal offsets.
- **Don't forget to mark visited** *before* recursing/enqueuing, otherwise the same cell gets pushed many times and you may double-count or blow up memory.
- If you are not allowed to mutate the input, keep a separate `visited` boolean matrix instead of overwriting `'1'` → `'0'`.

---

## 🔗 Related problems
- **Max Area of Island** (LC 695) — same flood-fill, return the largest component size.
- **Number of Islands II** (LC 305) — land added incrementally; union-find shines.
- **Surrounded Regions** (LC 130) — flood-fill from the borders to find "safe" regions.
- **Number of Connected Components in an Undirected Graph** (LC 323) — the non-grid version of the same counting idea.
- **Making A Large Island** (LC 827) — flood-fill + merge analysis.

---

**→ Next:** [`02-Max-Area-of-Island.md`](./02-Max-Area-of-Island.md) | [Problem set index](./00-Index.md)
