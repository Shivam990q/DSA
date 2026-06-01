# Rotting Oranges

**Platform**: LeetCode 994 · **Difficulty**: Medium · **Topics**: Array, BFS, Matrix · **Pattern**: Multi-source BFS (level = time)

---

## 📜 Problem Statement

You are given an `m x n` grid where each cell can have one of three values:

- `0` representing an empty cell,
- `1` representing a fresh orange, or
- `2` representing a rotten orange.

Every minute, any fresh orange that is **4-directionally adjacent** to a rotten orange becomes rotten.

Return *the minimum number of minutes that must elapse until no cell has a fresh orange*. If this is impossible, return `-1`.

### Examples

**Example 1:**
```
Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
Output: 4
Explanation: Wave by wave the rot spreads outward; the last fresh orange
at the bottom-right rots at minute 4.
```

**Example 2:**
```
Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
Output: -1
Explanation: The fresh orange at the bottom-left corner (2,0) is never
adjacent to a rotten orange, so it can never rot.
```

**Example 3:**
```
Input: grid = [[0,2]]
Output: 0
Explanation: There are no fresh oranges at minute 0, so the answer is 0.
```

### Constraints
```
m == grid.length
n == grid[i].length
1 <= m, n <= 10
grid[i][j] is 0, 1, or 2.
```

---

## 🧠 Understanding the problem

Rot spreads simultaneously from **every** rotten orange each minute — that "all at once" wording is the signal for **multi-source BFS**. If we seed a BFS queue with *all* initially rotten oranges, then process the queue **level by level**, each level corresponds to exactly one minute of spreading. The number of levels needed to consume the last fresh orange is the answer.

Two things to track:
1. A `fresh` counter — how many fresh oranges remain. We need it to detect the impossible case (some fresh orange isolated from all rot) and to know when to stop.
2. `minutes` — incremented once per BFS level, but only when the level actually produced new rot.

If after the BFS any fresh oranges remain (`fresh > 0`), they were unreachable → return `-1`. If there were no fresh oranges to begin with, the answer is `0`.

Grid is at most 10 × 10, so this is purely about modeling time correctly, not performance.

---

## Approach 1 — Multi-source BFS (recommended) ⭐

### Intuition
Drop all the rotten oranges into the queue at time 0. Each round, every orange currently in the queue rots its fresh neighbors; those new rotten oranges form the next round. Counting rounds counts minutes. Because all sources start together, the BFS depth equals the real elapsed time.

### Algorithm
1. Scan the grid: enqueue every cell with value `2`; count cells with value `1` into `fresh`.
2. `minutes = 0`.
3. While the queue is non-empty **and** `fresh > 0`:
   - For each orange in the current level (snapshot the queue size):
     - Pop it; for each fresh neighbor: set it to `2`, decrement `fresh`, enqueue it.
   - After finishing the level, `minutes++`.
4. Return `fresh == 0 ? minutes : -1`.

### Dry run on Example 1 `[[2,1,1],[1,1,0],[0,1,1]]`
```
Initial: rotten at (0,0). fresh=6. queue=[(0,0)].
Minute 1: (0,0) rots (0,1) and (1,0). fresh=4. minutes=1.
Minute 2: (0,1)->(0,2); (1,0)->(1,1). fresh=2. minutes=2.
Minute 3: (0,2) no fresh nbr; (1,1)->(2,1). fresh=1. minutes=3.
Minute 4: (2,1)->(2,2). fresh=0. minutes=4.
Queue still has items but fresh==0 → stop. Answer = 4.
```

### Code

```cpp
class Solution {
public:
    int orangesRotting(vector<vector<int>>& grid) {
        int rows = grid.size(), cols = grid[0].size(), fresh = 0, minutes = 0;
        queue<pair<int,int>> q;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == 2) q.push({r, c});
                else if (grid[r][c] == 1) fresh++;
            }
        int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
        while (!q.empty() && fresh > 0) {
            int sz = q.size();
            for (int i = 0; i < sz; i++) {
                auto [r, c] = q.front(); q.pop();
                for (int d = 0; d < 4; d++) {
                    int nr = r + dr[d], nc = c + dc[d];
                    if (nr >= 0 && nc >= 0 && nr < rows && nc < cols
                        && grid[nr][nc] == 1) {
                        grid[nr][nc] = 2;
                        fresh--;
                        q.push({nr, nc});
                    }
                }
            }
            minutes++;
        }
        return fresh == 0 ? minutes : -1;
    }
};
```
```java
class Solution {
    public int orangesRotting(int[][] grid) {
        int rows = grid.length, cols = grid[0].length, fresh = 0, minutes = 0;
        Queue<int[]> q = new LinkedList<>();
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == 2) q.offer(new int[]{r, c});
                else if (grid[r][c] == 1) fresh++;
            }
        int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
        while (!q.isEmpty() && fresh > 0) {
            int sz = q.size();
            for (int i = 0; i < sz; i++) {
                int[] cell = q.poll();
                for (int d = 0; d < 4; d++) {
                    int nr = cell[0] + dr[d], nc = cell[1] + dc[d];
                    if (nr >= 0 && nc >= 0 && nr < rows && nc < cols
                        && grid[nr][nc] == 1) {
                        grid[nr][nc] = 2;
                        fresh--;
                        q.offer(new int[]{nr, nc});
                    }
                }
            }
            minutes++;
        }
        return fresh == 0 ? minutes : -1;
    }
}
```
```python
from collections import deque

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        q = deque()
        fresh = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    q.append((r, c))
                elif grid[r][c] == 1:
                    fresh += 1
        minutes = 0
        while q and fresh > 0:
            for _ in range(len(q)):
                r, c = q.popleft()
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh -= 1
                        q.append((nr, nc))
            minutes += 1
        return minutes if fresh == 0 else -1
```

### Complexity
- **Time**: O(m·n) — each cell enqueued and processed at most once.
- **Space**: O(m·n) for the queue in the worst case (all oranges rotten at start).

---

## Approach 2 — BFS storing time with each cell (no level snapshot)

### Intuition
Instead of processing level by level, store `(row, col, time)` in the queue. When an orange rots a neighbor, that neighbor's time is `time + 1`. The answer is the maximum time stamped on any orange. This removes the inner "for each item in level" loop, at the cost of carrying a counter per cell.

### Algorithm
1. Enqueue every rotten orange as `(r, c, 0)`; count `fresh`.
2. `result = 0`.
3. Pop `(r, c, t)`; for each fresh neighbor, set rotten, `fresh--`, `result = max(result, t + 1)`, enqueue `(nr, nc, t + 1)`.
4. Return `fresh == 0 ? result : -1`.

### Dry run on Example 1
```
queue=[(0,0,0)], fresh=6.
Pop (0,0,0): rot (0,1,1),(1,0,1). result=1. fresh=4.
Pop (0,1,1): rot (0,2,2). result=2.  Pop (1,0,1): rot (1,1,2). result=2. fresh=2.
Pop (0,2,2): none. Pop (1,1,2): rot (2,1,3). result=3. fresh=1.
Pop (2,1,3): rot (2,2,4). result=4. fresh=0.
Answer = 4.
```

### Code

```cpp
class Solution {
public:
    int orangesRotting(vector<vector<int>>& grid) {
        int rows = grid.size(), cols = grid[0].size(), fresh = 0, result = 0;
        queue<tuple<int,int,int>> q;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == 2) q.push({r, c, 0});
                else if (grid[r][c] == 1) fresh++;
            }
        int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
        while (!q.empty()) {
            auto [r, c, t] = q.front(); q.pop();
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr >= 0 && nc >= 0 && nr < rows && nc < cols
                    && grid[nr][nc] == 1) {
                    grid[nr][nc] = 2;
                    fresh--;
                    result = max(result, t + 1);
                    q.push({nr, nc, t + 1});
                }
            }
        }
        return fresh == 0 ? result : -1;
    }
};
```
```java
class Solution {
    public int orangesRotting(int[][] grid) {
        int rows = grid.length, cols = grid[0].length, fresh = 0, result = 0;
        Queue<int[]> q = new LinkedList<>();
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == 2) q.offer(new int[]{r, c, 0});
                else if (grid[r][c] == 1) fresh++;
            }
        int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
        while (!q.isEmpty()) {
            int[] cell = q.poll();
            int r = cell[0], c = cell[1], t = cell[2];
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr >= 0 && nc >= 0 && nr < rows && nc < cols
                    && grid[nr][nc] == 1) {
                    grid[nr][nc] = 2;
                    fresh--;
                    result = Math.max(result, t + 1);
                    q.offer(new int[]{nr, nc, t + 1});
                }
            }
        }
        return fresh == 0 ? result : -1;
    }
}
```
```python
from collections import deque

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        q = deque()
        fresh = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    q.append((r, c, 0))
                elif grid[r][c] == 1:
                    fresh += 1
        result = 0
        while q:
            r, c, t = q.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    result = max(result, t + 1)
                    q.append((nr, nc, t + 1))
        return result if fresh == 0 else -1
```

### Complexity
- **Time**: O(m·n).
- **Space**: O(m·n).

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Level-snapshot BFS | O(m·n) | O(m·n) | minutes = number of levels; intuitive ⭐ |
| Time-stamped BFS | O(m·n) | O(m·n) | answer = max stamped time; no inner loop |

Functionally equivalent. The level-snapshot version maps most directly to the "every minute" wording; the time-stamped version is handy if you want each cell's individual rot time.

---

## 🧪 Edge cases & pitfalls
- **No fresh oranges at start** → answer `0` (the `while fresh > 0` guard never spreads, `minutes` stays 0).
- **A fresh orange unreachable from any rot** → `fresh` never hits 0 → return `-1`.
- **Counting an extra minute**: without the `fresh > 0` guard in Approach 1, you may run one empty BFS level and overcount by 1. The guard stops as soon as the last fresh orange rots.
- **Forgetting to decrement `fresh`** breaks the impossible-case detection.
- **All cells empty / all rotten** → 0 either way (no fresh oranges).

---

## 🔗 Related problems
- **Walls and Gates** (LC 286) — multi-source BFS computing distance to the nearest gate.
- **01 Matrix** (LC 542) — multi-source BFS distance to the nearest `0`.
- **Shortest Bridge** (LC 934) — flood-fill one island, then BFS outward.
- **As Far from Land as Possible** (LC 1162) — multi-source BFS maximizing distance.

---

**→ Next:** [`05-Pacific-Atlantic-Water-Flow.md`](./05-Pacific-Atlantic-Water-Flow.md) | **← Prev:** [`03-Clone-Graph.md`](./03-Clone-Graph.md) | [Problem set index](./00-Index.md)
