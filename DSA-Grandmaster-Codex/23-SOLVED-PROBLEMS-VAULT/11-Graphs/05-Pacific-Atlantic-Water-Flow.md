# Pacific Atlantic Water Flow

**Platform**: LeetCode 417 · **Difficulty**: Medium · **Topics**: Array, DFS, BFS, Matrix · **Pattern**: Reverse multi-source traversal from borders

---

## 📜 Problem Statement

There is an `m x n` rectangular island that borders both the **Pacific Ocean** and **Atlantic Ocean**. The Pacific Ocean touches the island's **left and top** edges, and the Atlantic Ocean touches the island's **right and bottom** edges.

The island is partitioned into a grid of square cells. You are given an `m x n` integer matrix `heights` where `heights[r][c]` represents the **height above sea level** of the cell at coordinate `(r, c)`.

The island receives a lot of rain, and the rain water can flow to neighboring cells directly north, south, east, and west if the neighboring cell's height is **less than or equal to** the current cell's height. Water can flow from any cell adjacent to an ocean into the ocean.

Return *a 2D list of grid coordinates* `result` where `result[i] = [ri, ci]` denotes that rain water can flow from cell `(ri, ci)` to **both** the Pacific and Atlantic oceans.

### Examples

**Example 1:**
```
Input: heights = [
  [1,2,2,3,5],
  [3,2,3,4,4],
  [2,4,5,3,1],
  [6,7,1,4,5],
  [5,1,1,2,4]
]
Output: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
```

**Example 2:**
```
Input: heights = [[1]]
Output: [[0,0]]
Explanation: The single cell touches both oceans.
```

**Example 3:**
```
Input: heights = [[2,1],[1,2]]
Output: [[0,0],[0,1],[1,0],[1,1]]
```

### Constraints
```
m == heights.length
n == heights[r].length
1 <= m, n <= 200
0 <= heights[r][c] <= 10^5
```

---

## 🧠 Understanding the problem

We need every cell from which water can reach **both** oceans. Water flows from a cell to a neighbor whose height is **≤** the current cell's height (downhill or flat).

The brute force instinct is: from each cell, simulate flowing downhill and check whether you can hit the Pacific border and the Atlantic border. That is O((m·n)²) in the worst case.

The clean idea is to **reverse the flow**. Instead of asking "can this cell reach an ocean going downhill", we start *at the oceans* and walk **uphill** (to neighbors with height ≥ current). A cell reachable this way from the Pacific border is exactly a cell that can flow *to* the Pacific. Do this for both oceans, producing two boolean sets `pacific` and `atlantic`. The answer is their intersection.

Why reverse works: "A flows to B downhill" is equivalent to "B reaches A uphill". Starting from all border cells of an ocean is a **multi-source traversal**, so each ocean is computed in one O(m·n) sweep.

---

## Approach 1 — Brute force per-cell downhill DFS

### Intuition
Literally test each cell: run a DFS following the downhill rule; mark whether the path touched a Pacific border and an Atlantic border. Include the cell if both are touched.

### Algorithm
1. For each cell `(r, c)`:
   - DFS from it, moving to neighbors with height ≤ current, tracking if we reach a Pacific edge and an Atlantic edge.
   - If both reached → add `(r, c)`.
2. Reset the visited matrix between cells.

### Dry run on Example 3 `[[2,1],[1,2]]`
```
Cell (0,0)=2: it's on top row (Pacific) and left col (Pacific); can it reach Atlantic?
   downhill to (0,1)=1 (right col → Atlantic) and (1,0)=1 (bottom row → Atlantic).
   reaches both → include.
... every cell ends up reaching both → all 4 included.
```

### Code

```cpp
class Solution {
    int rows, cols;
    int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
    void dfs(vector<vector<int>>& h, int r, int c,
             vector<vector<bool>>& seen, bool& pac, bool& atl) {
        seen[r][c] = true;
        if (r == 0 || c == 0) pac = true;
        if (r == rows - 1 || c == cols - 1) atl = true;
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr >= 0 && nc >= 0 && nr < rows && nc < cols
                && !seen[nr][nc] && h[nr][nc] <= h[r][c])
                dfs(h, nr, nc, seen, pac, atl);
        }
    }
public:
    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {
        rows = heights.size(); cols = heights[0].size();
        vector<vector<int>> res;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) {
                vector<vector<bool>> seen(rows, vector<bool>(cols, false));
                bool pac = false, atl = false;
                dfs(heights, r, c, seen, pac, atl);
                if (pac && atl) res.push_back({r, c});
            }
        return res;
    }
};
```
```java
class Solution {
    private int rows, cols;
    private int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
    private boolean pac, atl;

    public List<List<Integer>> pacificAtlantic(int[][] heights) {
        rows = heights.length; cols = heights[0].length;
        List<List<Integer>> res = new ArrayList<>();
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) {
                boolean[][] seen = new boolean[rows][cols];
                pac = false; atl = false;
                dfs(heights, r, c, seen);
                if (pac && atl) res.add(Arrays.asList(r, c));
            }
        return res;
    }

    private void dfs(int[][] h, int r, int c, boolean[][] seen) {
        seen[r][c] = true;
        if (r == 0 || c == 0) pac = true;
        if (r == rows - 1 || c == cols - 1) atl = true;
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr >= 0 && nc >= 0 && nr < rows && nc < cols
                && !seen[nr][nc] && h[nr][nc] <= h[r][c])
                dfs(h, nr, nc, seen);
        }
    }
}
```
```python
class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        rows, cols = len(heights), len(heights[0])
        res = []

        def dfs(r, c, seen, flags):
            seen.add((r, c))
            if r == 0 or c == 0:
                flags[0] = True            # Pacific
            if r == rows - 1 or c == cols - 1:
                flags[1] = True            # Atlantic
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen \
                        and heights[nr][nc] <= heights[r][c]:
                    dfs(nr, nc, seen, flags)

        for r in range(rows):
            for c in range(cols):
                flags = [False, False]
                dfs(r, c, set(), flags)
                if flags[0] and flags[1]:
                    res.append([r, c])
        return res
```

### Complexity
- **Time**: O((m·n)²) — a full DFS per cell. Too slow near the upper bound (200 × 200).
- **Space**: O(m·n) per DFS.

### Verdict
Correct, but quadratic in the number of cells. Good only as the baseline that motivates reversing the flow.

---

## Approach 2 — Reverse DFS from ocean borders (recommended) ⭐

### Intuition
Flip the question. From each ocean's border cells, climb **uphill** (neighbor height ≥ current). Every cell you can reach this way can send water back down to that ocean. Compute the reachable set for each ocean once, then intersect.

### Algorithm
1. Create two boolean matrices `pac` and `atl`.
2. Seed Pacific from the top row and left column; seed Atlantic from the bottom row and right column.
3. From each seed, DFS to neighbors with height ≥ current, marking the corresponding matrix.
4. The answer is all cells where `pac && atl`.

### Dry run on Example 1 (corner intuition)
```
Pacific DFS starts on top row + left col; climbs uphill marking reachable cells.
Atlantic DFS starts on bottom row + right col; climbs uphill likewise.
Cell (2,2)=5 is a local peak reachable from both border climbs → in both sets → included.
The 7 cells in the expected output are exactly the overlap of the two reachable sets.
```

### Code

```cpp
class Solution {
    int rows, cols;
    int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
    void dfs(vector<vector<int>>& h, int r, int c, vector<vector<bool>>& ocean) {
        ocean[r][c] = true;
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr >= 0 && nc >= 0 && nr < rows && nc < cols
                && !ocean[nr][nc] && h[nr][nc] >= h[r][c])
                dfs(h, nr, nc, ocean);
        }
    }
public:
    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {
        rows = heights.size(); cols = heights[0].size();
        vector<vector<bool>> pac(rows, vector<bool>(cols, false));
        vector<vector<bool>> atl(rows, vector<bool>(cols, false));
        for (int r = 0; r < rows; r++) { dfs(heights, r, 0, pac); dfs(heights, r, cols - 1, atl); }
        for (int c = 0; c < cols; c++) { dfs(heights, 0, c, pac); dfs(heights, rows - 1, c, atl); }
        vector<vector<int>> res;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (pac[r][c] && atl[r][c]) res.push_back({r, c});
        return res;
    }
};
```
```java
class Solution {
    private int rows, cols;
    private int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};

    public List<List<Integer>> pacificAtlantic(int[][] heights) {
        rows = heights.length; cols = heights[0].length;
        boolean[][] pac = new boolean[rows][cols];
        boolean[][] atl = new boolean[rows][cols];
        for (int r = 0; r < rows; r++) { dfs(heights, r, 0, pac); dfs(heights, r, cols - 1, atl); }
        for (int c = 0; c < cols; c++) { dfs(heights, 0, c, pac); dfs(heights, rows - 1, c, atl); }
        List<List<Integer>> res = new ArrayList<>();
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (pac[r][c] && atl[r][c]) res.add(Arrays.asList(r, c));
        return res;
    }

    private void dfs(int[][] h, int r, int c, boolean[][] ocean) {
        ocean[r][c] = true;
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr >= 0 && nc >= 0 && nr < rows && nc < cols
                && !ocean[nr][nc] && h[nr][nc] >= h[r][c])
                dfs(h, nr, nc, ocean);
        }
    }
}
```
```python
class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        rows, cols = len(heights), len(heights[0])
        pac = [[False] * cols for _ in range(rows)]
        atl = [[False] * cols for _ in range(rows)]

        def dfs(r, c, ocean):
            ocean[r][c] = True
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and not ocean[nr][nc] \
                        and heights[nr][nc] >= heights[r][c]:
                    dfs(nr, nc, ocean)

        for r in range(rows):
            dfs(r, 0, pac)
            dfs(r, cols - 1, atl)
        for c in range(cols):
            dfs(0, c, pac)
            dfs(rows - 1, c, atl)

        return [[r, c] for r in range(rows) for c in range(cols)
                if pac[r][c] and atl[r][c]]
```

### Complexity
- **Time**: O(m·n) — each cell visited at most once per ocean.
- **Space**: O(m·n) for the two boolean matrices plus recursion.

---

## Approach 3 — Reverse BFS from ocean borders

### Intuition
Identical reverse-flow logic, but seed two queues with the border cells and BFS uphill. Useful when recursion depth is a worry (a 200 × 200 monotone grid could recurse 40,000 deep).

### Algorithm
1. Enqueue all Pacific border cells into `qPac` and mark `pac`; same for Atlantic.
2. BFS each queue uphill (neighbor height ≥ current), marking its matrix.
3. Intersect.

### Dry run (mechanism)
```
qPac initially = entire top row + left column (all marked pac).
Pop a border cell, push uphill neighbors, mark them pac, continue until queue empties.
Repeat for Atlantic. Cells true in both → answer.
```

### Code

```cpp
class Solution {
public:
    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {
        int rows = heights.size(), cols = heights[0].size();
        vector<vector<bool>> pac(rows, vector<bool>(cols, false));
        vector<vector<bool>> atl(rows, vector<bool>(cols, false));
        queue<pair<int,int>> qp, qa;
        for (int r = 0; r < rows; r++) {
            qp.push({r, 0}); pac[r][0] = true;
            qa.push({r, cols - 1}); atl[r][cols - 1] = true;
        }
        for (int c = 0; c < cols; c++) {
            qp.push({0, c}); pac[0][c] = true;
            qa.push({rows - 1, c}); atl[rows - 1][c] = true;
        }
        bfs(heights, qp, pac);
        bfs(heights, qa, atl);
        vector<vector<int>> res;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (pac[r][c] && atl[r][c]) res.push_back({r, c});
        return res;
    }
private:
    void bfs(vector<vector<int>>& h, queue<pair<int,int>>& q, vector<vector<bool>>& ocean) {
        int rows = h.size(), cols = h[0].size();
        int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
        while (!q.empty()) {
            auto [r, c] = q.front(); q.pop();
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr >= 0 && nc >= 0 && nr < rows && nc < cols
                    && !ocean[nr][nc] && h[nr][nc] >= h[r][c]) {
                    ocean[nr][nc] = true;
                    q.push({nr, nc});
                }
            }
        }
    }
};
```
```java
class Solution {
    public List<List<Integer>> pacificAtlantic(int[][] heights) {
        int rows = heights.length, cols = heights[0].length;
        boolean[][] pac = new boolean[rows][cols];
        boolean[][] atl = new boolean[rows][cols];
        Queue<int[]> qp = new LinkedList<>(), qa = new LinkedList<>();
        for (int r = 0; r < rows; r++) {
            qp.offer(new int[]{r, 0}); pac[r][0] = true;
            qa.offer(new int[]{r, cols - 1}); atl[r][cols - 1] = true;
        }
        for (int c = 0; c < cols; c++) {
            qp.offer(new int[]{0, c}); pac[0][c] = true;
            qa.offer(new int[]{rows - 1, c}); atl[rows - 1][c] = true;
        }
        bfs(heights, qp, pac);
        bfs(heights, qa, atl);
        List<List<Integer>> res = new ArrayList<>();
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (pac[r][c] && atl[r][c]) res.add(Arrays.asList(r, c));
        return res;
    }

    private void bfs(int[][] h, Queue<int[]> q, boolean[][] ocean) {
        int rows = h.length, cols = h[0].length;
        int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
        while (!q.isEmpty()) {
            int[] cell = q.poll();
            for (int d = 0; d < 4; d++) {
                int nr = cell[0] + dr[d], nc = cell[1] + dc[d];
                if (nr >= 0 && nc >= 0 && nr < rows && nc < cols
                    && !ocean[nr][nc] && h[nr][nc] >= h[cell[0]][cell[1]]) {
                    ocean[nr][nc] = true;
                    q.offer(new int[]{nr, nc});
                }
            }
        }
    }
}
```
```python
from collections import deque

class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        rows, cols = len(heights), len(heights[0])
        pac = [[False] * cols for _ in range(rows)]
        atl = [[False] * cols for _ in range(rows)]
        qp, qa = deque(), deque()
        for r in range(rows):
            qp.append((r, 0)); pac[r][0] = True
            qa.append((r, cols - 1)); atl[r][cols - 1] = True
        for c in range(cols):
            qp.append((0, c)); pac[0][c] = True
            qa.append((rows - 1, c)); atl[rows - 1][c] = True

        def bfs(q, ocean):
            while q:
                r, c = q.popleft()
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and not ocean[nr][nc] \
                            and heights[nr][nc] >= heights[r][c]:
                        ocean[nr][nc] = True
                        q.append((nr, nc))

        bfs(qp, pac)
        bfs(qa, atl)
        return [[r, c] for r in range(rows) for c in range(cols)
                if pac[r][c] and atl[r][c]]
```

### Complexity
- **Time**: O(m·n).
- **Space**: O(m·n).

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Per-cell downhill DFS | O((m·n)²) | O(m·n) | brute baseline; too slow at 200×200 |
| Reverse DFS from borders | O(m·n) | O(m·n) | clean and optimal ⭐ |
| Reverse BFS from borders | O(m·n) | O(m·n) | same, no recursion depth risk |

The "reverse the flow" insight collapses a quadratic search into two linear sweeps. DFS vs BFS is a stylistic choice; both are optimal.

---

## 🧪 Edge cases & pitfalls
- **Single cell** → touches all four edges → belongs to both oceans → `[[0,0]]`.
- **Direction of the inequality**: forward flow uses `≤`, but the *reverse* climb uses `≥`. Mixing them is the classic bug.
- **Corners are seeded into both oceans** (e.g., top-right is on the top row → Pacific, and the right column → Atlantic). That is correct, not a double-count.
- **Mark border cells as reachable when seeding** — they trivially reach their own ocean.
- Output order does not matter; LeetCode accepts any permutation of the correct cells.

---

## 🔗 Related problems
- **Number of Islands** (LC 200) — grid flood-fill foundation.
- **Surrounded Regions** (LC 130) — also solved by traversing inward from the borders.
- **Walls and Gates** (LC 286) — multi-source BFS from special cells.
- **Shortest Path in Binary Matrix** (LC 1091) — grid BFS shortest path.

---

**→ Next:** [`06-Surrounded-Regions.md`](./06-Surrounded-Regions.md) | **← Prev:** [`04-Rotting-Oranges.md`](./04-Rotting-Oranges.md) | [Problem set index](./00-Index.md)
