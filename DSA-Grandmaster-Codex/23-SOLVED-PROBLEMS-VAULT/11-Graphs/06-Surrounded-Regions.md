# Surrounded Regions

**Platform**: LeetCode 130 · **Difficulty**: Medium · **Topics**: Array, DFS, BFS, Union-Find, Matrix · **Pattern**: Border-anchored flood-fill

---

## 📜 Problem Statement

You are given an `m x n` matrix `board` containing **letters** `'X'` and `'O'`, capture **regions** that are **surrounded**:

- **Connect**: A cell is connected to adjacent cells horizontally or vertically.
- **Region**: To form a region connect every `'O'` cell.
- **Surround**: The region is surrounded with `'X'` cells if you can connect the region with `'X'` cells and none of the region cells are on the edge of the board.

A surrounded region is **captured** by replacing all `'O'`s with `'X'`s in the input matrix `board`.

You must modify the board **in-place**.

### Examples

**Example 1:**
```
Input: board = [
  ["X","X","X","X"],
  ["X","O","O","X"],
  ["X","X","O","X"],
  ["X","O","X","X"]
]
Output: [
  ["X","X","X","X"],
  ["X","X","X","X"],
  ["X","X","X","X"],
  ["X","O","X","X"]
]
Explanation: The three surrounded 'O's (1,1),(1,2),(2,2) are captured.
The 'O' at (3,1) is on the border, so it (and anything connected to it) is NOT captured.
```

**Example 2:**
```
Input: board = [["X"]]
Output: [["X"]]
```

**Example 3:**
```
Input: board = [
  ["O","O"],
  ["O","O"]
]
Output: [
  ["O","O"],
  ["O","O"]
]
Explanation: Every 'O' touches the border, so nothing is captured.
```

### Constraints
```
m == board.length
n == board[i].length
1 <= m, n <= 200
board[i][j] is 'X' or 'O'.
```

---

## 🧠 Understanding the problem

An `'O'` region is captured **only if it does not touch the border**. So instead of trying to detect "fully surrounded" regions directly (hard — you would have to prove no escape), invert the logic:

> An `'O'` is **safe** (never captured) if and only if it is connected to a border `'O'`.

That flips a hard "is this enclosed?" question into an easy "is this reachable from the edge?" traversal. The plan:

1. From every `'O'` on the border, flood-fill and mark all connected `'O'`s as safe.
2. Sweep the board: every remaining (unmarked) `'O'` is surrounded → flip to `'X'`. Every marked-safe cell → restore to `'O'`.

This is the same border-anchored idea as Pacific Atlantic. Grid is up to 200 × 200, so a couple of linear sweeps are plenty.

---

## Approach 1 — Border DFS marking safe cells (recommended) ⭐

### Intuition
Border `'O'`s and anything connected to them can "escape" — they survive. Mark them with a temporary symbol (`'S'`). Whatever is still `'O'` afterward was trapped.

### Algorithm
1. For each cell on the four borders: if it is `'O'`, DFS and mark the whole connected `'O'` region as `'S'`.
2. Iterate over the whole board:
   - `'O'` → `'X'` (it was surrounded).
   - `'S'` → `'O'` (restore safe cells).

### Dry run on Example 1
```
Border 'O's: (3,1) is on the bottom border.
DFS from (3,1): only (3,1) itself is a border-connected 'O' (its neighbors are 'X').
Mark (3,1)='S'.
Now flip pass:
  (1,1),(1,2),(2,2) are still 'O' → become 'X' (captured).
  (3,1)='S' → restore to 'O'.
Matches expected output.
```

### Code

```cpp
class Solution {
    int rows, cols;
    void dfs(vector<vector<char>>& b, int r, int c) {
        if (r < 0 || c < 0 || r >= rows || c >= cols || b[r][c] != 'O') return;
        b[r][c] = 'S';
        dfs(b, r + 1, c); dfs(b, r - 1, c);
        dfs(b, r, c + 1); dfs(b, r, c - 1);
    }
public:
    void solve(vector<vector<char>>& board) {
        rows = board.size(); cols = board[0].size();
        for (int r = 0; r < rows; r++) { dfs(board, r, 0); dfs(board, r, cols - 1); }
        for (int c = 0; c < cols; c++) { dfs(board, 0, c); dfs(board, rows - 1, c); }
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                board[r][c] = (board[r][c] == 'S') ? 'O' : 'X';
    }
};
```
```java
class Solution {
    private int rows, cols;

    public void solve(char[][] board) {
        rows = board.length; cols = board[0].length;
        for (int r = 0; r < rows; r++) { dfs(board, r, 0); dfs(board, r, cols - 1); }
        for (int c = 0; c < cols; c++) { dfs(board, 0, c); dfs(board, rows - 1, c); }
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                board[r][c] = (board[r][c] == 'S') ? 'O' : 'X';
    }

    private void dfs(char[][] b, int r, int c) {
        if (r < 0 || c < 0 || r >= rows || c >= cols || b[r][c] != 'O') return;
        b[r][c] = 'S';
        dfs(b, r + 1, c); dfs(b, r - 1, c);
        dfs(b, r, c + 1); dfs(b, r, c - 1);
    }
}
```
```python
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        rows, cols = len(board), len(board[0])

        def dfs(r, c):
            if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != 'O':
                return
            board[r][c] = 'S'
            dfs(r + 1, c); dfs(r - 1, c)
            dfs(r, c + 1); dfs(r, c - 1)

        for r in range(rows):
            dfs(r, 0); dfs(r, cols - 1)
        for c in range(cols):
            dfs(0, c); dfs(rows - 1, c)

        for r in range(rows):
            for c in range(cols):
                board[r][c] = 'O' if board[r][c] == 'S' else 'X'
```

### Complexity
- **Time**: O(m·n) — border DFS plus a final sweep.
- **Space**: O(m·n) recursion stack in the worst case.

---

## Approach 2 — Border BFS marking safe cells

### Intuition
Same border-anchored marking, but iterative. Seed a queue with all border `'O'`s, BFS to mark connected `'O'`s as `'S'`. Avoids deep recursion on a board that is mostly one big border-connected `'O'` blob.

### Algorithm
1. Enqueue every border `'O'`, mark it `'S'`.
2. BFS: pop a cell, enqueue any neighboring `'O'`, marking each `'S'` as enqueued.
3. Final sweep: `'O'` → `'X'`, `'S'` → `'O'`.

### Dry run on Example 1
```
Border scan finds (3,1)='O' → enqueue, mark 'S'.
BFS pops (3,1): no neighboring 'O'. Queue empties.
Final sweep flips (1,1),(1,2),(2,2) to 'X' and restores (3,1) to 'O'.
```

### Code

```cpp
class Solution {
public:
    void solve(vector<vector<char>>& board) {
        int rows = board.size(), cols = board[0].size();
        queue<pair<int,int>> q;
        auto seed = [&](int r, int c) {
            if (board[r][c] == 'O') { board[r][c] = 'S'; q.push({r, c}); }
        };
        for (int r = 0; r < rows; r++) { seed(r, 0); seed(r, cols - 1); }
        for (int c = 0; c < cols; c++) { seed(0, c); seed(rows - 1, c); }
        int dr[] = {1, -1, 0, 0}, dc[] = {0, 0, 1, -1};
        while (!q.empty()) {
            auto [r, c] = q.front(); q.pop();
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr >= 0 && nc >= 0 && nr < rows && nc < cols && board[nr][nc] == 'O') {
                    board[nr][nc] = 'S';
                    q.push({nr, nc});
                }
            }
        }
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                board[r][c] = (board[r][c] == 'S') ? 'O' : 'X';
    }
};
```
```java
class Solution {
    public void solve(char[][] board) {
        int rows = board.length, cols = board[0].length;
        Queue<int[]> q = new LinkedList<>();
        for (int r = 0; r < rows; r++) {
            seed(board, q, r, 0); seed(board, q, r, cols - 1);
        }
        for (int c = 0; c < cols; c++) {
            seed(board, q, 0, c); seed(board, q, rows - 1, c);
        }
        int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
        while (!q.isEmpty()) {
            int[] cell = q.poll();
            for (int d = 0; d < 4; d++) {
                int nr = cell[0] + dr[d], nc = cell[1] + dc[d];
                if (nr >= 0 && nc >= 0 && nr < rows && nc < cols && board[nr][nc] == 'O') {
                    board[nr][nc] = 'S';
                    q.offer(new int[]{nr, nc});
                }
            }
        }
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                board[r][c] = (board[r][c] == 'S') ? 'O' : 'X';
    }

    private void seed(char[][] board, Queue<int[]> q, int r, int c) {
        if (board[r][c] == 'O') { board[r][c] = 'S'; q.offer(new int[]{r, c}); }
    }
}
```
```python
from collections import deque

class Solution:
    def solve(self, board: List[List[str]]) -> None:
        rows, cols = len(board), len(board[0])
        q = deque()

        def seed(r, c):
            if board[r][c] == 'O':
                board[r][c] = 'S'
                q.append((r, c))

        for r in range(rows):
            seed(r, 0); seed(r, cols - 1)
        for c in range(cols):
            seed(0, c); seed(rows - 1, c)

        while q:
            r, c = q.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 'O':
                    board[nr][nc] = 'S'
                    q.append((nr, nc))

        for r in range(rows):
            for c in range(cols):
                board[r][c] = 'O' if board[r][c] == 'S' else 'X'
```

### Complexity
- **Time**: O(m·n).
- **Space**: O(m·n) for the queue worst case.

---

## Approach 3 — Union-Find with a virtual "border" node

### Intuition
Create a dummy node that represents "the border / safe". Union every border `'O'` with this dummy, and union each `'O'` with its `'O'` neighbors. At the end, any `'O'` **not** connected to the dummy is surrounded and gets captured.

### Algorithm
1. Allocate DSU over `m·n + 1` nodes; the extra index `dummy = m·n` is the border anchor.
2. For each `'O'` cell:
   - If it is on the border, union it with `dummy`.
   - Union it with right/down neighbor if that neighbor is `'O'`.
3. Sweep: any `'O'` whose root differs from `find(dummy)` becomes `'X'`.

### Dry run on Example 1
```
dummy = 16 (for a 4x4 board).
(3,1) is a border 'O' → union(id(3,1), dummy). Its 'O' neighbors: none.
Interior 'O's (1,1),(1,2),(2,2) union among themselves but never touch dummy.
Sweep: (1,1),(1,2),(2,2) not connected to dummy → 'X'.
(3,1) connected to dummy → stays 'O'.
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
    void solve(vector<vector<char>>& board) {
        int rows = board.size(), cols = board[0].size(), dummy = rows * cols;
        parent.resize(rows * cols + 1);
        iota(parent.begin(), parent.end(), 0);
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (board[r][c] == 'O') {
                    int id = r * cols + c;
                    if (r == 0 || c == 0 || r == rows - 1 || c == cols - 1)
                        unite(id, dummy);
                    if (r + 1 < rows && board[r + 1][c] == 'O') unite(id, (r + 1) * cols + c);
                    if (c + 1 < cols && board[r][c + 1] == 'O') unite(id, r * cols + c + 1);
                }
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (board[r][c] == 'O' && find(r * cols + c) != find(dummy))
                    board[r][c] = 'X';
    }
};
```
```java
class Solution {
    private int[] parent;

    public void solve(char[][] board) {
        int rows = board.length, cols = board[0].length, dummy = rows * cols;
        parent = new int[rows * cols + 1];
        for (int i = 0; i <= rows * cols; i++) parent[i] = i;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (board[r][c] == 'O') {
                    int id = r * cols + c;
                    if (r == 0 || c == 0 || r == rows - 1 || c == cols - 1)
                        unite(id, dummy);
                    if (r + 1 < rows && board[r + 1][c] == 'O') unite(id, (r + 1) * cols + c);
                    if (c + 1 < cols && board[r][c + 1] == 'O') unite(id, r * cols + c + 1);
                }
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (board[r][c] == 'O' && find(r * cols + c) != find(dummy))
                    board[r][c] = 'X';
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
    def solve(self, board: List[List[str]]) -> None:
        rows, cols = len(board), len(board[0])
        dummy = rows * cols
        parent = list(range(rows * cols + 1))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def unite(a, b):
            parent[find(a)] = find(b)

        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'O':
                    idx = r * cols + c
                    if r == 0 or c == 0 or r == rows - 1 or c == cols - 1:
                        unite(idx, dummy)
                    if r + 1 < rows and board[r + 1][c] == 'O':
                        unite(idx, (r + 1) * cols + c)
                    if c + 1 < cols and board[r][c + 1] == 'O':
                        unite(idx, r * cols + c + 1)

        root = find(dummy)
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'O' and find(r * cols + c) != root:
                    board[r][c] = 'X'
```

### Complexity
- **Time**: O(m·n·α(m·n)) ≈ O(m·n).
- **Space**: O(m·n) for the DSU arrays.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Border DFS | O(m·n) | O(m·n) stack | cleanest; mark safe then flip ⭐ |
| Border BFS | O(m·n) | O(m·n) queue | safe against deep recursion |
| Union-Find + dummy | O(m·n·α) | O(m·n) | elegant; overkill unless dynamic |

DFS/BFS share the "mark border-connected `'O'`s, then flip the rest" idea and are the natural answers. Union-find is a nice alternative that frames "safe" as "connected to a virtual border node."

---

## 🧪 Edge cases & pitfalls
- **Every `'O'` on or touching the border** → nothing captured (Example 3).
- **Single row / single column** → every `'O'` is on the border → no captures.
- **Forgetting to restore `'S'` back to `'O'`** leaves stray markers in the output.
- **Capturing border `'O'`s by mistake** — only flip cells *not* reachable from the border.
- The board must be modified **in place**; do not return a new board.

---

## 🔗 Related problems
- **Number of Islands** (LC 200) — base flood-fill technique.
- **Pacific Atlantic Water Flow** (LC 417) — also anchors traversal at the borders.
- **Number of Enclaves** (LC 1020) — count land cells that cannot reach the border.
- **Number of Closed Islands** (LC 1254) — islands not touching the border.

---

**→ Next:** [`07-Course-Schedule.md`](./07-Course-Schedule.md) | **← Prev:** [`05-Pacific-Atlantic-Water-Flow.md`](./05-Pacific-Atlantic-Water-Flow.md) | [Problem set index](./00-Index.md)
