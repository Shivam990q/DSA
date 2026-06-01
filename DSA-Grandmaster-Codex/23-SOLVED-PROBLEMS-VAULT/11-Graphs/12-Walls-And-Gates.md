# Walls and Gates

**Platform**: LeetCode 286 · **Difficulty**: Medium · **Topics**: Array, BFS, Matrix · **Pattern**: Multi-source BFS (distance to nearest source)

---

## 📜 Problem Statement

You are given an `m x n` grid `rooms` initialized with these three possible values:

- `-1` — A **wall** or an obstacle.
- `0` — A **gate**.
- `INF` — Infinity means an **empty room**. (`2^31 - 1 = 2147483647` is used to represent INF, as you may assume that the distance to a gate is less than `2147483647`.)

Fill each empty room with the distance to its *nearest* gate. If it is impossible to reach a gate, that room should remain `INF`.

You must modify the grid **in place**.

### Examples

**Example 1:**
```
Input: rooms = [
  [INF, -1,  0, INF],
  [INF, INF, INF, -1],
  [INF, -1,  INF, -1],
  [  0, -1,  INF, INF]
]
Output: [
  [3, -1, 0, 1],
  [2,  2, 1, -1],
  [1, -1, 2, -1],
  [0, -1, 3, 4]
]
```

**Example 2:**
```
Input: rooms = [[0]]
Output: [[0]]
```

**Example 3:**
```
Input: rooms = [[INF]]
Output: [[INF]]
Explanation: With no gate, the lone empty room stays INF.
```

### Constraints
```
m == rooms.length
n == rooms[i].length
1 <= m, n <= 250
rooms[i][j] is -1, 0, or 2^31 - 1.
```

---

## 🧠 Understanding the problem

Each empty room must record the distance to the *nearest* gate. The naive idea — BFS outward from every empty room until it finds a gate — repeats work badly.

Flip it: run **one multi-source BFS that starts from all gates at once**. Seed the queue with every gate (distance 0). BFS spreads outward in unit steps; the first time the wave reaches a room, that is its shortest distance to *some* gate (specifically the nearest, because all gates expand simultaneously and BFS visits nearer cells first). Walls block the wave. Rooms never reached stay `INF`.

This is the same engine as Rotting Oranges: simultaneous expansion from multiple sources gives each cell its minimum distance in a single linear sweep. Grid is ≤ 250 × 250, so O(m·n) is fast.

---

## Approach 1 — Multi-source BFS from all gates (recommended) ⭐

### Intuition
All gates are at distance 0. Push them all into the queue, then BFS. Because BFS expands the closest cells first and all gates start together, the first visit to any room is via its nearest gate.

### Algorithm
1. Enqueue every gate cell (`rooms[r][c] == 0`).
2. While the queue is non-empty: pop `(r, c)`; for each neighbor that is still `INF`, set it to `rooms[r][c] + 1` and enqueue it.
3. Walls (`-1`) are simply never matched (we only advance into `INF` cells), so they block naturally.

### Dry run on Example 1 (first ring)
```
Gates at (0,2) and (3,0), both distance 0, both enqueued.
Pop (0,2): neighbor (1,2) is INF → set 1, enqueue. (0,3) INF → set 1, enqueue.
Pop (3,0): neighbor (2,0) is INF → set 1, enqueue.
Next ring fills distance-2 rooms, and so on, until every reachable room is filled.
Rooms blocked by walls with no path stay INF (none in this example).
```

### Code

```cpp
class Solution {
public:
    void wallsAndGates(vector<vector<int>>& rooms) {
        int rows = rooms.size(), cols = rooms[0].size();
        const int INF = INT_MAX;
        queue<pair<int,int>> q;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (rooms[r][c] == 0) q.push({r, c});
        int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
        while (!q.empty()) {
            auto [r, c] = q.front(); q.pop();
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr >= 0 && nc >= 0 && nr < rows && nc < cols
                    && rooms[nr][nc] == INF) {
                    rooms[nr][nc] = rooms[r][c] + 1;
                    q.push({nr, nc});
                }
            }
        }
    }
};
```
```java
class Solution {
    public void wallsAndGates(int[][] rooms) {
        int rows = rooms.length, cols = rooms[0].length;
        final int INF = Integer.MAX_VALUE;
        Queue<int[]> q = new LinkedList<>();
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (rooms[r][c] == 0) q.offer(new int[]{r, c});
        int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
        while (!q.isEmpty()) {
            int[] cell = q.poll();
            for (int d = 0; d < 4; d++) {
                int nr = cell[0] + dr[d], nc = cell[1] + dc[d];
                if (nr >= 0 && nc >= 0 && nr < rows && nc < cols
                    && rooms[nr][nc] == INF) {
                    rooms[nr][nc] = rooms[cell[0]][cell[1]] + 1;
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
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        rows, cols = len(rooms), len(rooms[0])
        INF = 2 ** 31 - 1
        q = deque((r, c) for r in range(rows) for c in range(cols) if rooms[r][c] == 0)
        while q:
            r, c = q.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == INF:
                    rooms[nr][nc] = rooms[r][c] + 1
                    q.append((nr, nc))
```

### Complexity
- **Time**: O(m·n) — each room set and enqueued at most once.
- **Space**: O(m·n) for the queue in the worst case.

---

## Approach 2 — DFS from each gate (brute, for contrast)

### Intuition
From every gate, DFS outward writing increasing distances, but only overwrite a room when the new distance is **smaller** than what is already stored. Running this for all gates leaves each room with its minimum. Simpler to reason about but can revisit cells many times.

### Algorithm
1. For each gate cell, DFS with `distance = 0`.
2. `dfs(r, c, dist)`:
   - Out of bounds, a wall, or `rooms[r][c] < dist` → stop (a shorter path already wrote here).
   - Set `rooms[r][c] = dist`.
   - Recurse into the four neighbors with `dist + 1`.

### Dry run on Example 2 `[[0]]`
```
Gate at (0,0). dfs(0,0,0): set rooms[0][0]=0. neighbors all out of bounds → done.
Output [[0]].
```

### Code

```cpp
class Solution {
    int rows, cols;
    void dfs(vector<vector<int>>& rooms, int r, int c, int dist) {
        if (r < 0 || c < 0 || r >= rows || c >= cols || rooms[r][c] < dist) return;
        rooms[r][c] = dist;
        dfs(rooms, r + 1, c, dist + 1);
        dfs(rooms, r - 1, c, dist + 1);
        dfs(rooms, r, c + 1, dist + 1);
        dfs(rooms, r, c - 1, dist + 1);
    }
public:
    void wallsAndGates(vector<vector<int>>& rooms) {
        rows = rooms.size(); cols = rooms[0].size();
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (rooms[r][c] == 0) dfs(rooms, r, c, 0);
    }
};
```
```java
class Solution {
    private int rows, cols;

    public void wallsAndGates(int[][] rooms) {
        rows = rooms.length; cols = rooms[0].length;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (rooms[r][c] == 0) dfs(rooms, r, c, 0);
    }

    private void dfs(int[][] rooms, int r, int c, int dist) {
        if (r < 0 || c < 0 || r >= rows || c >= cols || rooms[r][c] < dist) return;
        rooms[r][c] = dist;
        dfs(rooms, r + 1, c, dist + 1);
        dfs(rooms, r - 1, c, dist + 1);
        dfs(rooms, r, c + 1, dist + 1);
        dfs(rooms, r, c - 1, dist + 1);
    }
}
```
```python
class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        rows, cols = len(rooms), len(rooms[0])

        def dfs(r, c, dist):
            if r < 0 or c < 0 or r >= rows or c >= cols or rooms[r][c] < dist:
                return
            rooms[r][c] = dist
            dfs(r + 1, c, dist + 1)
            dfs(r - 1, c, dist + 1)
            dfs(r, c + 1, dist + 1)
            dfs(r, c - 1, dist + 1)

        for r in range(rows):
            for c in range(cols):
                if rooms[r][c] == 0:
                    dfs(r, c, 0)
```

### Complexity
- **Time**: O(m·n·G) worst case (G = number of gates), since a room may be re-written from several gates.
- **Space**: O(m·n) recursion depth.

### Verdict
Correct because the `rooms[r][c] < dist` guard keeps only the minimum, but it can revisit cells repeatedly. BFS visits each cell once and is the preferred answer.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Multi-source BFS | O(m·n) | O(m·n) | each room filled once with its nearest distance ⭐ |
| Per-gate DFS | O(m·n·G) | O(m·n) | simpler to state; redundant revisits |

The multi-source BFS is optimal: seeding all gates at level 0 means the wavefront reaches each room exactly when it is at its minimum distance, so no cell is ever updated twice.

---

## 🧪 Edge cases & pitfalls
- **No gates** → grid unchanged; every `INF` stays `INF`.
- **Room unreachable from any gate** (walled off) → stays `INF`.
- **Only update `INF` cells in BFS** — this single check simultaneously skips walls, gates, and already-filled rooms, and is why each cell is processed once.
- **Don't BFS from rooms** — start from gates; BFS from each empty room separately is far slower.
- The grid must be modified **in place** (no return value).

---

## 🔗 Related problems
- **Rotting Oranges** (LC 994) — multi-source BFS measuring spread time.
- **01 Matrix** (LC 542) — distance to nearest `0`, same multi-source pattern.
- **As Far from Land as Possible** (LC 1162) — multi-source BFS maximizing distance.
- **Shortest Distance from All Buildings** (LC 317) — BFS from each building, accumulate.

---

**→ Next:** [`13-Graph-Valid-Tree.md`](./13-Graph-Valid-Tree.md) | **← Prev:** [`11-Word-Ladder.md`](./11-Word-Ladder.md) | [Problem set index](./00-Index.md)
