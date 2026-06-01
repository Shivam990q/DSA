# Word Search

**Platform**: LeetCode 79 · **Difficulty**: Medium · **Topics**: Array, String, Backtracking, Matrix, DFS · **Pattern**: Grid DFS + visited sentinel

---

## 📜 Problem Statement

Given an `m x n` grid of characters `board` and a string `word`, return `true` *if `word` exists in the grid*.

The word can be constructed from letters of **sequentially adjacent** cells, where adjacent cells are **horizontally or vertically** neighboring. The **same letter cell may not be used more than once**.

### Examples

**Example 1:**
```
Input:  board = [["A","B","C","E"],
                 ["S","F","C","S"],
                 ["A","D","E","E"]], word = "ABCCED"
Output: true
Explanation: A(0,0)→B(0,1)→C(0,2)→C(1,2)→E(2,2)→D(2,1).
```

**Example 2:**
```
Input:  board = [["A","B","C","E"],
                 ["S","F","C","S"],
                 ["A","D","E","E"]], word = "SEE"
Output: true
Explanation: S(1,3)→E(2,3)→E(2,2).
```

**Example 3:**
```
Input:  board = [["A","B","C","E"],
                 ["S","F","C","S"],
                 ["A","D","E","E"]], word = "ABCB"
Output: false
Explanation: The second B would need to reuse the (0,1) cell.
```

### Constraints
```
m == board.length
n == board[i].length
1 <= m, n <= 6
1 <= word.length <= 15
board and word consist of only lowercase and uppercase English letters.
```

---

## 🧠 Understanding the problem

We're searching for a **path** in the grid that spells `word`, moving only up/down/left/right, never stepping on the same cell twice within that path. Unlike the subset/permutation problems, the "choices" here are *directions to move*, and the "state" is *where we are and which cells the current path has already used*.

The natural strategy: try starting the word at every cell, and from each start do a depth-first walk that matches `word` one character at a time. The crucial backtracking detail is **marking a cell as visited before recursing and un-marking it afterward**, so a cell is blocked only for the *current* path, not for sibling paths that branch elsewhere. A neat trick avoids a separate `visited[][]` matrix: temporarily overwrite the cell with a sentinel character (e.g. `'#'`), then restore the original on the way back — that *is* the choose/un-choose ritual applied to the grid.

With `m, n <= 6` and `word.length <= 15`, the grid is small, but the branching factor (up to 4 directions per step) makes early mismatch-pruning important.

---

## Approach 1 — DFS with in-place sentinel marking ⭐

### Intuition
From a starting cell, attempt to match `word[i]`. If the current cell is out of bounds or its letter ≠ `word[i]`, this branch fails. If `i` has reached the end of the word, we've matched everything → success. Otherwise mark the cell used, try all four neighbors for `word[i+1]`, and restore the cell when we return. Launch this DFS from every cell; if any start succeeds, the word exists.

### Algorithm
1. For each cell `(r, c)`: if `dfs(r, c, 0)` is true → return `true`.
2. `dfs(r, c, i)`:
   - If `i == word.length` → return `true` (matched all chars).
   - If `(r,c)` out of bounds or `board[r][c] != word[i]` → return `false`.
   - **choose**: save `board[r][c]`, set it to `'#'`.
   - **explore**: recurse into the 4 neighbors with `i + 1`; OR their results.
   - **un-choose**: restore `board[r][c]`.
   - Return the OR result.

### Dry run on matching `"SEE"` (Example 2)
```
start (1,3)='S' == word[0] → mark '#'
  try (2,3)='E' == word[1] → mark '#'
    try (2,2)='E' == word[2] → mark '#'
       i==3 == len → TRUE  (path S→E→E found)
```
The first successful start short-circuits via the `||`/`any` so we stop immediately.

### Code
```cpp
class Solution {
public:
    bool dfs(vector<vector<char>>& b, int r, int c, const string& w, int i) {
        if (i == (int)w.size()) return true;
        if (r < 0 || c < 0 || r >= (int)b.size() || c >= (int)b[0].size()
            || b[r][c] != w[i]) return false;
        char tmp = b[r][c]; b[r][c] = '#';          // choose (mark visited)
        bool found = dfs(b, r+1, c, w, i+1) || dfs(b, r-1, c, w, i+1)
                  || dfs(b, r, c+1, w, i+1) || dfs(b, r, c-1, w, i+1);
        b[r][c] = tmp;                              // un-choose (restore)
        return found;
    }
    bool exist(vector<vector<char>>& board, string word) {
        for (int r = 0; r < (int)board.size(); r++)
            for (int c = 0; c < (int)board[0].size(); c++)
                if (dfs(board, r, c, word, 0)) return true;
        return false;
    }
};
```
```java
class Solution {
    public boolean exist(char[][] board, String word) {
        for (int r = 0; r < board.length; r++)
            for (int c = 0; c < board[0].length; c++)
                if (dfs(board, r, c, word, 0)) return true;
        return false;
    }
    private boolean dfs(char[][] b, int r, int c, String w, int i) {
        if (i == w.length()) return true;
        if (r < 0 || c < 0 || r >= b.length || c >= b[0].length
            || b[r][c] != w.charAt(i)) return false;
        char tmp = b[r][c]; b[r][c] = '#';           // choose (mark visited)
        boolean found = dfs(b, r+1, c, w, i+1) || dfs(b, r-1, c, w, i+1)
                     || dfs(b, r, c+1, w, i+1) || dfs(b, r, c-1, w, i+1);
        b[r][c] = tmp;                               // un-choose (restore)
        return found;
    }
}
```
```python
class Solution:
    def exist(self, board, word):
        R, C = len(board), len(board[0])
        def dfs(r, c, i):
            if i == len(word):
                return True
            if r < 0 or c < 0 or r >= R or c >= C or board[r][c] != word[i]:
                return False
            tmp = board[r][c]; board[r][c] = '#'      # choose (mark visited)
            found = (dfs(r+1, c, i+1) or dfs(r-1, c, i+1) or
                     dfs(r, c+1, i+1) or dfs(r, c-1, i+1))
            board[r][c] = tmp                         # un-choose (restore)
            return found
        return any(dfs(r, c, 0) for r in range(R) for c in range(C))
```

### Complexity
- **Time**: O(m · n · 4^L) where `L = word.length` — each of `m·n` starts launches a DFS that branches up to 4 ways for up to `L` steps (the first step has 4 options, the rest have 3 since we never step back, so more precisely O(m·n·3^L)).
- **Space**: O(L) recursion depth; sentinel marking uses no extra grid.

---

## Approach 2 — DFS with a separate `visited` matrix

### Intuition
Identical search, but track used cells in a boolean matrix instead of mutating `board`. Useful when the board must remain const, or in languages/contexts where mutating the input is undesirable (e.g. concurrent reads).

### Algorithm
Same as Approach 1, but `choose`/`un-choose` toggle `visited[r][c]` instead of overwriting the character; the failure check additionally rejects already-visited cells.

### Code
```cpp
class Solution {
public:
    bool dfs(vector<vector<char>>& b, vector<vector<bool>>& vis,
             int r, int c, const string& w, int i) {
        if (i == (int)w.size()) return true;
        if (r < 0 || c < 0 || r >= (int)b.size() || c >= (int)b[0].size()
            || vis[r][c] || b[r][c] != w[i]) return false;
        vis[r][c] = true;                           // choose
        bool found = dfs(b, vis, r+1, c, w, i+1) || dfs(b, vis, r-1, c, w, i+1)
                  || dfs(b, vis, r, c+1, w, i+1) || dfs(b, vis, r, c-1, w, i+1);
        vis[r][c] = false;                          // un-choose
        return found;
    }
    bool exist(vector<vector<char>>& board, string word) {
        int m = board.size(), n = board[0].size();
        vector<vector<bool>> vis(m, vector<bool>(n, false));
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++)
                if (dfs(board, vis, r, c, word, 0)) return true;
        return false;
    }
};
```
```java
class Solution {
    public boolean exist(char[][] board, String word) {
        int m = board.length, n = board[0].length;
        boolean[][] vis = new boolean[m][n];
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++)
                if (dfs(board, vis, r, c, word, 0)) return true;
        return false;
    }
    private boolean dfs(char[][] b, boolean[][] vis, int r, int c, String w, int i) {
        if (i == w.length()) return true;
        if (r < 0 || c < 0 || r >= b.length || c >= b[0].length
            || vis[r][c] || b[r][c] != w.charAt(i)) return false;
        vis[r][c] = true;                            // choose
        boolean found = dfs(b, vis, r+1, c, w, i+1) || dfs(b, vis, r-1, c, w, i+1)
                     || dfs(b, vis, r, c+1, w, i+1) || dfs(b, vis, r, c-1, w, i+1);
        vis[r][c] = false;                           // un-choose
        return found;
    }
}
```
```python
class Solution:
    def exist(self, board, word):
        R, C = len(board), len(board[0])
        vis = [[False] * C for _ in range(R)]
        def dfs(r, c, i):
            if i == len(word):
                return True
            if (r < 0 or c < 0 or r >= R or c >= C
                    or vis[r][c] or board[r][c] != word[i]):
                return False
            vis[r][c] = True                          # choose
            found = (dfs(r+1, c, i+1) or dfs(r-1, c, i+1) or
                     dfs(r, c+1, i+1) or dfs(r, c-1, i+1))
            vis[r][c] = False                         # un-choose
            return found
        return any(dfs(r, c, 0) for r in range(R) for c in range(C))
```

### Complexity
- **Time**: O(m · n · 3^L) — same as Approach 1.
- **Space**: O(m · n) for the `visited` matrix + O(L) recursion.

---

## ⚖️ Approach comparison

| Approach | Time | Space | When to mention |
|----------|------|-------|-----------------|
| In-place sentinel | O(m·n·3^L) | O(L) | least memory; the slick standard answer ⭐ |
| `visited` matrix | O(m·n·3^L) | O(m·n) | when the board must stay immutable |

**Optional pruning** (worth mentioning): if the multiset of letters in `word` isn't a subset of the board's letters, return `false` immediately. Also, starting the DFS from the rarer endpoint of `word` (front vs. reversed) can prune faster.

---

## 🧪 Edge cases & pitfalls
- **Single cell board** with `word` of length 1 → matches iff that cell equals the char.
- **Word longer than the grid has cells** → can still partially match but ultimately fails; bounds + visited handle it.
- **Repeated letters forcing reuse** (`"ABCB"` in Example 3) → fails because the sentinel/visited blocks reusing `(0,1)`.
- **Pitfall — forgetting to restore** the cell (sentinel or `visited`) on return: later starts/branches see a falsely-blocked cell and miss valid words.
- **Pitfall — checking bounds after indexing**: always test `r/c` in range *before* reading `board[r][c]`, or you'll index out of bounds.
- **Pitfall — base case order**: check `i == word.length()` (success) *before* the bounds/mismatch check, so a fully-matched word returns true even at the grid edge.
- **Pitfall — marking the start but returning early** without unmarking on the success path is fine for a boolean search, but if you later need to find *all* paths, restore consistently.

---

## 🔗 Related problems
- **Word Search II** (LC 212) — find many words at once; build a **Trie** over the dictionary and DFS the grid once.
- **Number of Islands** (LC 200) — grid DFS/flood fill (no backtrack-restore needed).
- **Surrounded Regions** (LC 130) — grid DFS from borders.
- **Letter Combinations of a Phone Number** (LC 17) — positional DFS without a grid. → [08-Letter-Combinations-Phone-Number.md](./08-Letter-Combinations-Phone-Number.md)

---

**→ Next:** [`07-Palindrome-Partitioning.md`](./07-Palindrome-Partitioning.md) | [Problem set index](./00-Index.md) | **← Prev:** [`05-Subsets-II.md`](./05-Subsets-II.md)
