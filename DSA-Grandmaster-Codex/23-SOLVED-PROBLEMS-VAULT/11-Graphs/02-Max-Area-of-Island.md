# Max Area of Island

**Platform**: LeetCode 695 · **Difficulty**: Medium · **Topics**: Array, DFS, BFS, Union-Find, Matrix · **Pattern**: Grid flood-fill (measure component size)

---

## 📜 Problem Statement

You are given an `m x n` binary matrix `grid`. An **island** is a group of `1`'s (representing land) connected **4-directionally** (horizontal or vertical). You may assume all four edges of the grid are surrounded by water.

The **area** of an island is the number of cells with a value `1` in the island.

Return *the maximum area of an island* in `grid`. If there is no island, return `0`.

### Examples

**Example 1:**
```
Input: grid = [
  [0,0,1,0,0,0,0,1,0,0,0,0,0],
  [0,0,0,0,0,0,0,1,1,1,0,0,0],
  [0,1,1,0,1,0,0,0,0,0,0,0,0],
  [0,1,0,0,1,1,0,0,1,0,1,0,0],
  [0,1,0,0,1,1,0,0,1,1,1,0,0],
  [0,0,0,0,0,0,0,0,0,0,1,0,0],
  [0,0,0,0,0,0,0,1,1,1,0,0,0],
  [0,0,0,0,0,0,0,1,1,0,0,0,0]
]
Output: 6
Explanation: The largest connected block of 1s has 6 cells.
```

**Example 2:**
```
Input: grid = [[0,0,0,0,0,0,0,0]]
Output: 0
Explanation: There is no island, so the maximum area is 0.
```

**Example 3:**
```
Input: grid = [[1,1,0],[0,1,0],[1,0,1]]
Output: 3
Explanation: The top-left L-shaped block of three 1s is the largest island.
```

### Constraints
```
m == grid.length
n == grid[i].length
1 <= m, n <= 50
grid[i][j] is either 0 or 1.
```

---

## 🧠 Understanding the problem

This is **Number of Islands** with a twist: instead of *counting* components we *measure* the largest one. The flood-fill skeleton is identical — scan for fresh land, sink the whole island — but each flood-fill must **return how many cells it sank**. We keep a running maximum over all islands.

The key realization: an island's area is just the count of cells visited during its flood-fill. If DFS returns `1 + (areas of the four neighbor recursions)`, the top-level call returns the full island size for free.

Grid is tiny (≤ 50 × 50 = 2,500 cells), so efficiency is a non-issue; correctness of the "sum the visited cells" logic is what matters.

---

## Approach 1 — DFS returning area (recommended) ⭐

### Intuition
Make the recursion *return a number*. A water cell or out-of-bounds contributes `0`. A land cell contributes `1` for itself plus whatever its four neighbors contribute. Mark each visited cell so it is counted exactly once.

### Algorithm
1. `best = 0`.
2. For each cell `(r, c)`: if it is land, `best = max(best, dfs(r, c))`.
3. `dfs(r, c)`:
   - If out of bounds or `grid[r][c] == 0` → return `0`.
   - Set `grid[r][c] = 0` (mark visited).
   - Return `1 + dfs(up) + dfs(down) + dfs(left) + dfs(right)`.
4. Return `best`.

### Dry run on Example 3 `[[1,1,0],[0,1,0],[1,0,1]]`
```
(0,0) land → dfs:
   visit (0,0)=1, go right (0,1)=1, from (0,1) go down (1,1)=1.
   that L-block totals 3. best=3.
(2,0) land → dfs returns 1. best stays 3.
(2,2) land → dfs returns 1. best stays 3.
Answer = 3.
```

### Code

```cpp
class Solution {
public:
    int maxAreaOfIsland(vector<vector<int>>& grid) {
        int best = 0;
        for (int r = 0; r < (int)grid.size(); r++)
            for (int c = 0; c < (int)grid[0].size(); c++)
                if (grid[r][c] == 1)
                    best = max(best, dfs(grid, r, c));
        return best;
    }
private:
    int dfs(vector<vector<int>>& grid, int r, int c) {
        if (r < 0 || c < 0 || r >= (int)grid.size() || c >= (int)grid[0].size()
            || grid[r][c] == 0)
            return 0;
        grid[r][c] = 0;
        return 1 + dfs(grid, r + 1, c) + dfs(grid, r - 1, c)
                 + dfs(grid, r, c + 1) + dfs(grid, r, c - 1);
    }
};
```
```java
class Solution {
    public int maxAreaOfIsland(int[][] grid) {
        int best = 0;
        for (int r = 0; r < grid.length; r++)
            for (int c = 0; c < grid[0].length; c++)
                if (grid[r][c] == 1)
                    best = Math.max(best, dfs(grid, r, c));
        return best;
    }

    private int dfs(int[][] grid, int r, int c) {
        if (r < 0 || c < 0 || r >= grid.length || c >= grid[0].length
            || grid[r][c] == 0)
            return 0;
        grid[r][c] = 0;
        return 1 + dfs(grid, r + 1, c) + dfs(grid, r - 1, c)
                 + dfs(grid, r, c + 1) + dfs(grid, r, c - 1);
    }
}
```
```python
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])

        def dfs(r, c):
            if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == 0:
                return 0
            grid[r][c] = 0
            return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)

        best = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    best = max(best, dfs(r, c))
        return best
```

### Complexity
- **Time**: O(m·n) — each cell visited once.
- **Space**: O(m·n) recursion stack worst case (one big island).

---

## Approach 2 — BFS returning area

### Intuition
Same measurement, iterative. Count cells as you pop them from the queue. Avoids deep recursion (irrelevant here given small bounds, but a good habit and the safe pattern for larger grids).

### Algorithm
1. For each fresh land cell, BFS the component, incrementing a local `area` for every cell dequeued.
2. Mark cells `0` as they are enqueued so each is counted once.
3. Track the maximum `area`.

### Dry run on Example 3 (top-left island)
```
Start (0,0): mark 0, area starts at 0, queue=[(0,0)].
Pop (0,0): area=1; enqueue (0,1) [land] mark 0.
Pop (0,1): area=2; enqueue (1,1) [land] mark 0.
Pop (1,1): area=3; no new land.
Queue empty → island area = 3. best=3.
```

### Code

```cpp
class Solution {
public:
    int maxAreaOfIsland(vector<vector<int>>& grid) {
        int rows = grid.size(), cols = grid[0].size(), best = 0;
        int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (grid[r][c] == 1) {
                    int area = 0;
                    queue<pair<int,int>> q;
                    q.push({r, c});
                    grid[r][c] = 0;
                    while (!q.empty()) {
                        auto [cr, cc] = q.front(); q.pop();
                        area++;
                        for (int d = 0; d < 4; d++) {
                            int nr = cr + dr[d], nc = cc + dc[d];
                            if (nr >= 0 && nc >= 0 && nr < rows && nc < cols
                                && grid[nr][nc] == 1) {
                                grid[nr][nc] = 0;
                                q.push({nr, nc});
                            }
                        }
                    }
                    best = max(best, area);
                }
        return best;
    }
};
```
```java
class Solution {
    public int maxAreaOfIsland(int[][] grid) {
        int rows = grid.length, cols = grid[0].length, best = 0;
        int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (grid[r][c] == 1) {
                    int area = 0;
                    Queue<int[]> q = new LinkedList<>();
                    q.offer(new int[]{r, c});
                    grid[r][c] = 0;
                    while (!q.isEmpty()) {
                        int[] cell = q.poll();
                        area++;
                        for (int d = 0; d < 4; d++) {
                            int nr = cell[0] + dr[d], nc = cell[1] + dc[d];
                            if (nr >= 0 && nc >= 0 && nr < rows && nc < cols
                                && grid[nr][nc] == 1) {
                                grid[nr][nc] = 0;
                                q.offer(new int[]{nr, nc});
                            }
                        }
                    }
                    best = Math.max(best, area);
                }
        return best;
    }
}
```
```python
from collections import deque

class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        best = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    area = 0
                    q = deque([(r, c)])
                    grid[r][c] = 0
                    while q:
                        cr, cc = q.popleft()
                        area += 1
                        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                            nr, nc = cr + dr, cc + dc
                            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                                grid[nr][nc] = 0
                                q.append((nr, nc))
                    best = max(best, area)
        return best
```

### Complexity
- **Time**: O(m·n).
- **Space**: O(min(m, n)) for the queue.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| DFS (returns area) | O(m·n) | O(m·n) stack | most concise; the recursion sum *is* the area ⭐ |
| BFS (counts dequeues) | O(m·n) | O(min(m,n)) | safer stack behavior; explicit counter |

Both are optimal in time. DFS is the idiomatic interview answer; BFS is the defensive choice when recursion depth is a concern.

---

## 🧪 Edge cases & pitfalls
- **No island at all** → return `0` (the `best` initial value covers it).
- **Single-cell island** → area `1`.
- **Off-by-one in the return**: forgetting the `+1` for the current cell undercounts every island.
- **Counting at the wrong moment in BFS**: increment `area` when you *dequeue*, or when you *mark-and-enqueue* — pick one consistently. Doing both double-counts.
- **Diagonals are not connected** — only the 4 orthogonal neighbors.

---

## 🔗 Related problems
- **Number of Islands** (LC 200) — count components instead of measuring the biggest.
- **Island Perimeter** (LC 463) — measure boundary length instead of area.
- **Making A Large Island** (LC 827) — flip one `0` to `1` to maximize area; needs per-island labeling.
- **Max Area of Island** generalizes to any "largest connected component" query on a grid or graph.

---

**→ Next:** [`03-Clone-Graph.md`](./03-Clone-Graph.md) | **← Prev:** [`01-Number-of-Islands.md`](./01-Number-of-Islands.md) | [Problem set index](./00-Index.md)
