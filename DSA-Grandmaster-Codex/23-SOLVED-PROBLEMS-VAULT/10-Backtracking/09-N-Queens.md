# N-Queens

**Platform**: LeetCode 51 · **Difficulty**: Hard · **Topics**: Array, Backtracking · **Pattern**: Row-by-row placement + conflict sets

---

## 📜 Problem Statement

The **n-queens** puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other.

Given an integer `n`, return *all distinct solutions to the n-queens puzzle*. You may return the answer in **any order**.

Each solution contains a distinct board configuration of the n-queens' placement, where `'Q'` and `'.'` both indicate a queen and an empty space, respectively.

### Examples

**Example 1:**
```
Input:  n = 4
Output: [[".Q..",   ["..Q.",
          "...Q",    "Q...",
          "Q...",    "...Q",
          "..Q."],   ".Q.."]]
Explanation: There are exactly two distinct solutions to the 4-queens puzzle.
```

**Example 2:**
```
Input:  n = 1
Output: [["Q"]]
Explanation: A single queen on a 1x1 board.
```

**Example 3:**
```
Input:  n = 3
Output: []
Explanation: No way to place 3 non-attacking queens on a 3x3 board.
```

### Constraints
```
1 <= n <= 9
```

---

## 🧠 Understanding the problem

A queen attacks along its **row**, **column**, and **both diagonals**. The first simplification: since no two queens can share a row, we place **exactly one queen per row** and only decide *which column* it goes in. That collapses the search to "choose a column for row 0, then row 1, …, then row n-1," recording a solution when all `n` rows are filled.

For each candidate column in the current row we must check it isn't attacked by any already-placed queen. Three constraints capture every attack:
- **same column** `c`,
- **same "/" diagonal** — cells where `row + col` is constant,
- **same "\" diagonal** — cells where `row - col` is constant.

By tracking the occupied columns and the two diagonal keys in sets/boolean arrays, each "is this square safe?" test is **O(1)**. The choose/explore/un-choose ritual toggles these sets as we descend and backtrack. With `n <= 9`, the search is small, but the diagonal bookkeeping is what makes it elegant and fast.

A subtlety for diagonals: `row - col` ranges over `-(n-1) .. (n-1)`, so when using a boolean array we offset by `n` to keep indices non-negative.

---

## Approach 1 — Row-by-row backtracking with conflict sets ⭐

### Intuition
Place one queen per row. Maintain three boolean arrays: `col[c]`, `diag[row+col]` ("/" diagonals), and `anti[row-col+n]` ("\" diagonals). For the current row, try each column whose three keys are all free; mark them, place `'Q'`, recurse to the next row, then unmark and remove the queen. When `row == n`, snapshot the board.

### Algorithm
1. Init board of `'.'`, and `col`, `diag` (size `2n`), `anti` (size `2n`) all `false`.
2. `backtrack(row)`:
   - If `row == n`: record a copy of the board; return.
   - For `c` from `0` to `n-1`:
     - If `col[c]` or `diag[row+c]` or `anti[row-c+n]` → skip (attacked).
     - **choose**: set those three true, place `board[row][c] = 'Q'`.
     - **explore**: `backtrack(row + 1)`.
     - **un-choose**: reset the three, `board[row][c] = '.'`.

### Dry run on `n = 4` (first solution)
```
row0: c=1 ok → place .Q..      (col1, diag1, anti 1-? set)
 row1: c=3 ok → place ...Q
  row2: c=0 ok → place Q...
   row3: c=2 ok → place ..Q.   row==4 → RECORD
        .Q.. / ...Q / Q... / ..Q.
backtrack continues → finds the mirror solution ..Q./Q.../...Q/.Q..
```

### Code
```cpp
class Solution {
public:
    vector<vector<string>> solveNQueens(int n) {
        vector<vector<string>> res;
        vector<string> board(n, string(n, '.'));
        vector<bool> col(n, false), diag(2*n, false), anti(2*n, false);
        function<void(int)> bt = [&](int row) {
            if (row == n) { res.push_back(board); return; }
            for (int c = 0; c < n; c++) {
                if (col[c] || diag[row + c] || anti[row - c + n]) continue;
                col[c] = diag[row+c] = anti[row-c+n] = true;   // choose
                board[row][c] = 'Q';
                bt(row + 1);                                   // explore
                board[row][c] = '.';                           // un-choose
                col[c] = diag[row+c] = anti[row-c+n] = false;
            }
        };
        bt(0);
        return res;
    }
};
```
```java
class Solution {
    public List<List<String>> solveNQueens(int n) {
        List<List<String>> res = new ArrayList<>();
        char[][] board = new char[n][n];
        for (char[] row : board) Arrays.fill(row, '.');
        boolean[] col = new boolean[n], diag = new boolean[2*n], anti = new boolean[2*n];
        backtrack(0, n, board, col, diag, anti, res);
        return res;
    }
    private void backtrack(int row, int n, char[][] board, boolean[] col,
                           boolean[] diag, boolean[] anti, List<List<String>> res) {
        if (row == n) {
            List<String> snap = new ArrayList<>();
            for (char[] r : board) snap.add(new String(r));
            res.add(snap); return;
        }
        for (int c = 0; c < n; c++) {
            if (col[c] || diag[row + c] || anti[row - c + n]) continue;
            col[c] = diag[row+c] = anti[row-c+n] = true;       // choose
            board[row][c] = 'Q';
            backtrack(row + 1, n, board, col, diag, anti, res); // explore
            board[row][c] = '.';                                // un-choose
            col[c] = diag[row+c] = anti[row-c+n] = false;
        }
    }
}
```
```python
class Solution:
    def solveNQueens(self, n):
        res = []
        board = [['.'] * n for _ in range(n)]
        cols, diag, anti = set(), set(), set()
        def backtrack(row):
            if row == n:
                res.append(["".join(r) for r in board]); return
            for c in range(n):
                if c in cols or (row + c) in diag or (row - c) in anti:
                    continue
                cols.add(c); diag.add(row + c); anti.add(row - c)   # choose
                board[row][c] = 'Q'
                backtrack(row + 1)                                 # explore
                board[row][c] = '.'                                # un-choose
                cols.discard(c); diag.discard(row + c); anti.discard(row - c)
        backtrack(0)
        return res
```

### Complexity
- **Time**: O(n!) loosely — row 0 has `n` choices, row 1 has at most `n-1` safe columns, etc., with the diagonal constraints pruning far below `n!` in practice.
- **Space**: O(n) for the three conflict sets + recursion depth; O(n²) per solution board for the output.

---

## Approach 2 — Bitmask conflict tracking (fastest)

### Intuition
Represent the three constraint sets as **bits of integers** instead of arrays. `cols`, `diag1` ("/"), and `diag2` ("\") are bitmasks of occupied lines for the current row. The set of *available* columns is `avail = ~(cols | diag1 | diag2) & ((1<<n)-1)`. Pick the lowest set bit, recurse with the masks shifted (diagonals shift by one column per row), and clear that bit. This avoids index arithmetic and is the classic competitive-programming form.

### Algorithm
1. `place(row, cols, d1, d2)`:
   - If `row == n`: increment/record; reconstruct board from chosen columns.
   - `avail = full & ~(cols | d1 | d2)`.
   - While `avail`: take `p = avail & -avail` (lowest bit); recurse `(row+1, cols|p, (d1|p)<<1, (d2|p)>>1)`; clear `avail ^= p`.

To return boards (not just a count), we track the chosen column index per row.

### Code
```cpp
class Solution {
public:
    int n;
    vector<vector<string>> res;
    vector<int> queenCol;                  // column of the queen in each row
    void place(int row, int cols, int d1, int d2) {
        if (row == n) {
            vector<string> board(n, string(n, '.'));
            for (int r = 0; r < n; r++) board[r][queenCol[r]] = 'Q';
            res.push_back(board);
            return;
        }
        int full = (1 << n) - 1;
        int avail = full & ~(cols | d1 | d2);
        while (avail) {
            int p = avail & (-avail);          // lowest available column bit
            int c = __builtin_ctz(p);          // its index
            queenCol[row] = c;
            place(row + 1, cols | p, (d1 | p) << 1, (d2 | p) >> 1);
            avail ^= p;                         // clear that bit (un-choose)
        }
    }
    vector<vector<string>> solveNQueens(int N) {
        n = N; queenCol.assign(n, 0);
        place(0, 0, 0, 0);
        return res;
    }
};
```
```java
class Solution {
    private int n;
    private List<List<String>> res;
    private int[] queenCol;                     // column of the queen in each row
    public List<List<String>> solveNQueens(int N) {
        n = N; res = new ArrayList<>(); queenCol = new int[n];
        place(0, 0, 0, 0);
        return res;
    }
    private void place(int row, int cols, int d1, int d2) {
        if (row == n) {
            List<String> board = new ArrayList<>();
            for (int r = 0; r < n; r++) {
                char[] line = new char[n];
                Arrays.fill(line, '.');
                line[queenCol[r]] = 'Q';
                board.add(new String(line));
            }
            res.add(board); return;
        }
        int full = (1 << n) - 1;
        int avail = full & ~(cols | d1 | d2);
        while (avail != 0) {
            int p = avail & (-avail);              // lowest available column bit
            int c = Integer.numberOfTrailingZeros(p);
            queenCol[row] = c;
            place(row + 1, cols | p, (d1 | p) << 1, (d2 | p) >> 1);
            avail ^= p;                            // clear that bit (un-choose)
        }
    }
}
```
```python
class Solution:
    def solveNQueens(self, n):
        res = []
        queen_col = [0] * n
        full = (1 << n) - 1
        def place(row, cols, d1, d2):
            if row == n:
                board = []
                for r in range(n):
                    line = ['.'] * n
                    line[queen_col[r]] = 'Q'
                    board.append("".join(line))
                res.append(board); return
            avail = full & ~(cols | d1 | d2)
            while avail:
                p = avail & (-avail)               # lowest available column bit
                c = p.bit_length() - 1             # its index
                queen_col[row] = c
                place(row + 1, cols | p, (d1 | p) << 1, (d2 | p) >> 1)
                avail ^= p                          # clear that bit (un-choose)
        place(0, 0, 0, 0)
        return res
```

### Complexity
- **Time**: O(n!) worst case, with very tight constant factors (bit ops, no array indexing).
- **Space**: O(n) recursion depth + O(n) for `queenCol`; O(n²) per output board.

---

## ⚖️ Approach comparison

| Approach | Time | Space | When to mention |
|----------|------|-------|-----------------|
| Conflict sets (arrays/sets) | O(n!) pruned | O(n) | clearest to explain the row/col/diagonal model ⭐ |
| Bitmask | O(n!) pruned | O(n) | fastest; the go-to when only the **count** is needed (LC 52) |

Both prune identically; the bitmask version just trades readability for speed. For **N-Queens II** (count solutions, LC 52) the bitmask form is the standard answer.

---

## 🧪 Edge cases & pitfalls
- **n = 1** → one solution `[["Q"]]`.
- **n = 2 and n = 3** → **no** solutions, return `[]`. A classic gotcha — make sure the code returns empty rather than crashing.
- **Diagonal key offsets**: `row + col` ranges `0..2n-2`; `row - col` ranges `-(n-1)..(n-1)`. With boolean arrays add `n` (or `n-1`) so indices stay non-negative — a size-`2n` array is safe. With hash sets you can use the raw `row - col`.
- **Pitfall — only checking column, forgetting diagonals**: produces illegal boards that look plausible. You need *both* diagonal families.
- **Pitfall — wrong diagonal shift in the bitmask version**: `d1` (the `/` diagonal) shifts **left** as the row increases, `d2` (the `\` diagonal) shifts **right**; swapping them silently breaks pruning.
- **Pitfall — recording the board by reference / forgetting to reset** `board[row][c]` to `'.'` on backtrack corrupts other solutions.
- **Pitfall — not restoring conflict sets** after the recursive call leaves stale "attacked" markers that block valid placements in sibling branches.

---

## 🔗 Related problems
- **N-Queens II** (LC 52) — just count the solutions; bitmask form shines (return an int instead of boards).
- **Sudoku Solver** (LC 37) — constraint backtracking with row/col/box sets.
- **Permutations** (LC 46) — placing one queen per row is essentially permuting columns with diagonal constraints. → [04-Permutations.md](./04-Permutations.md)
- **Word Search** (LC 79) — the other classic constraint-DFS in this set. → [06-Word-Search.md](./06-Word-Search.md)

---

**→ Next:** [`../11-Graphs/00-Index.md`](../11-Graphs/00-Index.md) | [Problem set index](./00-Index.md) | **← Prev:** [`08-Letter-Combinations-Phone-Number.md`](./08-Letter-Combinations-Phone-Number.md)
