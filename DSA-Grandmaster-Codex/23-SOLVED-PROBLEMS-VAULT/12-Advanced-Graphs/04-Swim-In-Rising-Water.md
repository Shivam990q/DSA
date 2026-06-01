# Swim in Rising Water

**Platform**: LeetCode 778 · **Difficulty**: Hard · **Topics**: Array, Binary Search, DFS, BFS, Union-Find, Heap, Matrix · **Pattern**: Min-max path (Dijkstra / binary search / Kruskal)

---

## 📜 Problem Statement

You are given an `n x n` integer matrix `grid` where each value `grid[i][j]` represents the elevation at that point `(i, j)`.

The rain starts to fall. At time `t`, the depth of the water everywhere is `t`. You can swim from a square to another 4-directionally adjacent square if and only if the elevation of **both** squares individually are at most `t`. You can swim infinite distances in zero time. Of course, you must stay within the boundaries of the grid during your swim.

Return *the least time until you can reach the bottom right square `(n - 1, n - 1)` if you start at the top left square `(0, 0)`*.

### Examples

**Example 1:**
```
Input: grid = [[0,2],[1,3]]
Output: 3
Explanation: At time 0 you are at (0,0). You cannot move because the
adjacent cells have elevation > 0. At time 3 the water level allows you
to swim through (0,0)->(0,1)? elevation 2<=3 yes ->(1,1) elevation 3<=3.
The destination (1,1) has elevation 3, so the earliest time is 3.
```

**Example 2:**
```
Input: grid = [
  [0,1,2,3,4],
  [24,23,22,21,5],
  [12,13,14,15,16],
  [11,17,18,19,20],
  [10,9,8,7,6]
]
Output: 16
Explanation: The final route's highest elevation along the way is 16.
```

**Example 3:**
```
Input: grid = [[0,1],[2,3]]
Output: 3
```

### Constraints
```
n == grid.length
n == grid[i].length
1 <= n <= 50
0 <= grid[i][j] < n^2
Each value grid[i][j] is unique.
```

---

## 🧠 Understanding the problem

You can move freely once the water level `t` is at least the elevation of both the cell you're on and the cell you're moving to. Since you swim infinitely fast, the only thing that matters is: **what is the minimum water level that makes a path from `(0,0)` to `(n-1,n-1)` fully passable?**

A path is passable at time `t` iff **every** cell on it has elevation `≤ t`. So the cost of a path is its **maximum elevation** (its bottleneck). We want the path that *minimizes that maximum* — a classic **minimax path / bottleneck shortest path** problem. The answer is the smallest possible bottleneck over all paths.

Three angles:
- **Dijkstra-flavored**: like shortest path, but the cost of reaching a cell is `max(cost so far, that cell's elevation)`. A min-heap always expands the lowest current bottleneck; the first time we pop the destination, that's the answer.
- **Binary search + reachability**: guess a level `t`, check with DFS/BFS whether the destination is reachable using only cells `≤ t`. Binary search the smallest feasible `t`.
- **Kruskal/Union-Find**: add cells in increasing elevation order; the answer is the elevation at which `(0,0)` and `(n-1,n-1)` first become connected.

`n ≤ 50` (≤ 2500 cells), so all three are fast.

---

## Approach 1 — Dijkstra on the bottleneck (recommended) ⭐

### Intuition
Treat the "time to reach a cell" as the maximum elevation encountered on the best path to it. A min-heap keyed by this bottleneck pops cells in increasing order of their minimal required water level. When the destination is popped, its key is the minimum time.

### Algorithm
1. Min-heap of `(time, r, c)`; start with `(grid[0][0], 0, 0)`. `seen` matrix.
2. Pop `(t, r, c)`. If already seen, skip; mark seen. If `(r, c)` is the destination, return `t`.
3. For each neighbor `(nr, nc)`, push `(max(t, grid[nr][nc]), nr, nc)`.
4. Continue until the destination is popped.

### Dry run on Example 1 `[[0,2],[1,3]]`
```
Heap: (0,0,0).
Pop (0,0,0): seen. neighbors: (max(0,2),0,1)=(2,0,1); (max(0,1),1,0)=(1,1,0).
Pop (1,1,0): seen. neighbor (1,1): (max(1,3),1,1)=(3,1,1). neighbor (0,0) seen.
Pop (2,0,1): seen. neighbor (1,1): (max(2,3),1,1)=(3,1,1).
Pop (3,1,1): destination → return 3.
```

### Code

```cpp
class Solution {
public:
    int swimInWater(vector<vector<int>>& grid) {
        int n = grid.size();
        priority_queue<tuple<int,int,int>, vector<tuple<int,int,int>>, greater<>> pq;
        vector<vector<bool>> seen(n, vector<bool>(n, false));
        pq.push({grid[0][0], 0, 0});
        int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
        while (!pq.empty()) {
            auto [t, r, c] = pq.top(); pq.pop();
            if (seen[r][c]) continue;
            seen[r][c] = true;
            if (r == n - 1 && c == n - 1) return t;
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr >= 0 && nc >= 0 && nr < n && nc < n && !seen[nr][nc])
                    pq.push({max(t, grid[nr][nc]), nr, nc});
            }
        }
        return -1;
    }
};
```
```java
class Solution {
    public int swimInWater(int[][] grid) {
        int n = grid.length;
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
        boolean[][] seen = new boolean[n][n];
        pq.offer(new int[]{grid[0][0], 0, 0});
        int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            int t = cur[0], r = cur[1], c = cur[2];
            if (seen[r][c]) continue;
            seen[r][c] = true;
            if (r == n - 1 && c == n - 1) return t;
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr >= 0 && nc >= 0 && nr < n && nc < n && !seen[nr][nc])
                    pq.offer(new int[]{Math.max(t, grid[nr][nc]), nr, nc});
            }
        }
        return -1;
    }
}
```
```python
import heapq

class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        pq = [(grid[0][0], 0, 0)]
        seen = [[False] * n for _ in range(n)]
        while pq:
            t, r, c = heapq.heappop(pq)
            if seen[r][c]:
                continue
            seen[r][c] = True
            if r == n - 1 and c == n - 1:
                return t
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and not seen[nr][nc]:
                    heapq.heappush(pq, (max(t, grid[nr][nc]), nr, nc))
        return -1
```

### Complexity
- **Time**: O(n² log n) — each of the n² cells is pushed/popped with log-time heap ops.
- **Space**: O(n²) for the heap and `seen` matrix.

---

## Approach 2 — Binary search on time + DFS reachability

### Intuition
The answer lies in `[0, n²−1]`. For a fixed `t`, "can I reach the destination using only cells `≤ t`?" is a simple flood-fill. Feasibility is **monotonic** — if level `t` works, any larger level also works — so binary search the smallest feasible `t`.

### Algorithm
1. `lo = grid[0][0]`, `hi = n² − 1`.
2. While `lo < hi`: `mid = (lo + hi) / 2`. If `canReach(mid)` (DFS from `(0,0)` through cells `≤ mid` reaches the corner), set `hi = mid`; else `lo = mid + 1`.
3. Return `lo`.

### Dry run on Example 1 `[[0,2],[1,3]]`
```
lo=0, hi=3.
mid=1: cells ≤1 are (0,0)=0,(1,0)=1. Cannot reach (1,1)=3. → lo=2.
mid=2: cells ≤2: (0,0),(0,1)=2,(1,0). Still cannot reach (1,1). → lo=3.
lo==hi==3 → answer 3.
```

### Code

```cpp
class Solution {
    int n;
    bool canReach(vector<vector<int>>& grid, int t) {
        if (grid[0][0] > t) return false;
        vector<vector<bool>> seen(n, vector<bool>(n, false));
        return dfs(grid, 0, 0, t, seen);
    }
    bool dfs(vector<vector<int>>& grid, int r, int c, int t, vector<vector<bool>>& seen) {
        if (r < 0 || c < 0 || r >= n || c >= n || seen[r][c] || grid[r][c] > t)
            return false;
        if (r == n - 1 && c == n - 1) return true;
        seen[r][c] = true;
        return dfs(grid, r + 1, c, t, seen) || dfs(grid, r - 1, c, t, seen)
            || dfs(grid, r, c + 1, t, seen) || dfs(grid, r, c - 1, t, seen);
    }
public:
    int swimInWater(vector<vector<int>>& grid) {
        n = grid.size();
        int lo = grid[0][0], hi = n * n - 1;
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (canReach(grid, mid)) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
};
```
```java
class Solution {
    private int n;

    public int swimInWater(int[][] grid) {
        n = grid.length;
        int lo = grid[0][0], hi = n * n - 1;
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (canReach(grid, mid)) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }

    private boolean canReach(int[][] grid, int t) {
        if (grid[0][0] > t) return false;
        return dfs(grid, 0, 0, t, new boolean[n][n]);
    }

    private boolean dfs(int[][] grid, int r, int c, int t, boolean[][] seen) {
        if (r < 0 || c < 0 || r >= n || c >= n || seen[r][c] || grid[r][c] > t)
            return false;
        if (r == n - 1 && c == n - 1) return true;
        seen[r][c] = true;
        return dfs(grid, r + 1, c, t, seen) || dfs(grid, r - 1, c, t, seen)
            || dfs(grid, r, c + 1, t, seen) || dfs(grid, r, c - 1, t, seen);
    }
}
```
```python
class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)

        def can_reach(t):
            if grid[0][0] > t:
                return False
            seen = [[False] * n for _ in range(n)]

            def dfs(r, c):
                if r < 0 or c < 0 or r >= n or c >= n or seen[r][c] or grid[r][c] > t:
                    return False
                if r == n - 1 and c == n - 1:
                    return True
                seen[r][c] = True
                return (dfs(r + 1, c) or dfs(r - 1, c)
                        or dfs(r, c + 1) or dfs(r, c - 1))

            return dfs(0, 0)

        lo, hi = grid[0][0], n * n - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if can_reach(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
```

### Complexity
- **Time**: O(n² log(n²)) = O(n² log n) — each feasibility check is O(n²); binary search does O(log n²) checks.
- **Space**: O(n²) for the `seen` matrix and recursion.

---

## Approach 3 — Kruskal / Union-Find by increasing elevation

### Intuition
Because each elevation value is unique and lies in `[0, n²−1]`, add cells one at a time in elevation order. When a cell is "activated", union it with already-activated neighbors. The answer is the elevation at which `(0,0)` and `(n-1,n-1)` first land in the same component.

### Algorithm
1. Record the position of each elevation value (`pos[elev] = (r, c)`).
2. DSU over `n²` cells; `active` matrix all false.
3. For `t = 0, 1, ..., n²−1`: activate `pos[t]`; union it with active neighbors. After processing, if `find(0)` == `find(n²−1)`, return `t`.

### Dry run on Example 1 `[[0,2],[1,3]]` (ids: (0,0)=0,(0,1)=1,(1,0)=2,(1,1)=3)
```
t=0: activate elevation 0 at (0,0). no active neighbors.
t=1: activate elevation 1 at (1,0). neighbor (0,0) active → union {(0,0),(1,0)}.
t=2: activate elevation 2 at (0,1). neighbor (0,0) active → union → {(0,0),(0,1),(1,0)}.
t=3: activate elevation 3 at (1,1). neighbors (0,1),(1,0) active → union → all connected.
     find(start)==find(end) → return 3.
```

### Code

```cpp
class Solution {
    vector<int> parent;
    int find(int x) {
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }
    void unite(int a, int b) { parent[find(a)] = find(b); }
public:
    int swimInWater(vector<vector<int>>& grid) {
        int n = grid.size();
        vector<pair<int,int>> pos(n * n);
        for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++)
                pos[grid[r][c]] = {r, c};
        parent.resize(n * n);
        iota(parent.begin(), parent.end(), 0);
        vector<vector<bool>> active(n, vector<bool>(n, false));
        int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
        for (int t = 0; t < n * n; t++) {
            auto [r, c] = pos[t];
            active[r][c] = true;
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr >= 0 && nc >= 0 && nr < n && nc < n && active[nr][nc])
                    unite(r * n + c, nr * n + nc);
            }
            if (find(0) == find(n * n - 1)) return t;
        }
        return n * n - 1;
    }
};
```
```java
class Solution {
    private int[] parent;

    public int swimInWater(int[][] grid) {
        int n = grid.length;
        int[][] pos = new int[n * n][2];
        for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++) {
                pos[grid[r][c]][0] = r;
                pos[grid[r][c]][1] = c;
            }
        parent = new int[n * n];
        for (int i = 0; i < n * n; i++) parent[i] = i;
        boolean[][] active = new boolean[n][n];
        int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
        for (int t = 0; t < n * n; t++) {
            int r = pos[t][0], c = pos[t][1];
            active[r][c] = true;
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr >= 0 && nc >= 0 && nr < n && nc < n && active[nr][nc])
                    unite(r * n + c, nr * n + nc);
            }
            if (find(0) == find(n * n - 1)) return t;
        }
        return n * n - 1;
    }

    private int find(int x) {
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }

    private void unite(int a, int b) { parent[find(a)] = find(b); }
}
```
```python
class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        pos = [(0, 0)] * (n * n)
        for r in range(n):
            for c in range(n):
                pos[grid[r][c]] = (r, c)
        parent = list(range(n * n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def unite(a, b):
            parent[find(a)] = find(b)

        active = [[False] * n for _ in range(n)]
        for t in range(n * n):
            r, c = pos[t]
            active[r][c] = True
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and active[nr][nc]:
                    unite(r * n + c, nr * n + nc)
            if find(0) == find(n * n - 1):
                return t
        return n * n - 1
```

### Complexity
- **Time**: O(n²·α(n²)) ≈ O(n²).
- **Space**: O(n²) for the DSU, `pos`, and `active`.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Dijkstra (min bottleneck) | O(n² log n) | O(n²) | direct minimax path; cleanest mental model ⭐ |
| Binary search + DFS | O(n² log n) | O(n²) | leans on monotonic feasibility |
| Kruskal / Union-Find | O(n²·α) | O(n²) | exploits unique elevations in `[0, n²−1]` |

All three target the same quantity — the minimum bottleneck. Dijkstra is the most common interview answer; the DSU approach is elegant given the unique-value guarantee.

---

## 🧪 Edge cases & pitfalls
- **The cost is `max` along the path, not the sum** — using `dist + w` (Dijkstra-sum) instead of `max(t, elevation)` is the central trap.
- **Answer is at least `grid[0][0]` and `grid[n-1][n-1]`** — you must wait for the water to cover both endpoints.
- **`n = 1`** → answer is `grid[0][0]` (start == destination).
- **Binary search bounds**: start `lo` at `grid[0][0]` (you can never leave before that) and `hi` at `n²−1` (the max possible elevation).
- In Dijkstra, **skip stale popped cells** (`seen` check) to avoid reprocessing.

---

## 🔗 Related problems
- **Path With Minimum Effort** (LC 1631) — minimax on absolute height differences.
- **Network Delay Time** (LC 743) — standard sum-based Dijkstra (contrast the cost metric).
- **Min Cost to Connect All Points** (LC 1584) — Kruskal/Prim MST.
- **Kth Smallest Element in a Sorted Matrix** (LC 378) — binary-search-on-answer pattern.

---

**→ Next:** [`05-Reconstruct-Itinerary.md`](./05-Reconstruct-Itinerary.md) | **← Prev:** [`03-Min-Cost-Connect-Points.md`](./03-Min-Cost-Connect-Points.md) | [Problem set index](./00-Index.md)
