# Valid Sudoku

**Platform**: LeetCode 36 · **Difficulty**: Medium · **Topics**: Array, Hash Table, Matrix · **Pattern**: Constraint tracking with sets

---

## 📜 Problem Statement

Determine if a `9 x 9` Sudoku board is **valid**. Only the filled cells need to be validated according to the following rules:

1. Each **row** must contain the digits `1-9` without repetition.
2. Each **column** must contain the digits `1-9` without repetition.
3. Each of the nine `3 x 3` **sub-boxes** must contain the digits `1-9` without repetition.

Empty cells are represented by `'.'`. The board may be partially filled, and you only need to check the **current** placement (not whether it's ultimately solvable).

### Examples

**Example 1:**
```
Input: board =
[["5","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: true
```

**Example 2:** (same board but top-left becomes '8', clashing with the '8' in its column/box)
```
Output: false
```

### Constraints
```
board.length == 9, board[i].length == 9
board[i][j] is a digit '1'-'9' or '.'.
```

---

## 🧠 Understanding the problem

We're not solving the puzzle — just checking that no row, column, or 3×3 box already contains a repeated digit. For each filled cell we must answer: "has this digit already appeared in its row / column / box?" That's three membership checks → three sets per dimension.

The only trick is computing the **box index** from `(r, c)`: `boxIndex = (r / 3) * 3 + (c / 3)`, giving 0–8.

---

## Approach 1 — Three separate passes

### Intuition
Validate all rows, then all columns, then all boxes, each as an independent check.

### Algorithm
1. For each row, collect digits, ensure no repeats.
2. For each column, same.
3. For each 3×3 box, same.

### Code
```cpp
bool isValidSudoku(vector<vector<char>>& board) {
    // rows
    for (int r = 0; r < 9; r++) {
        set<char> seen;
        for (int c = 0; c < 9; c++)
            if (board[r][c] != '.' && !seen.insert(board[r][c]).second) return false;
    }
    // cols
    for (int c = 0; c < 9; c++) {
        set<char> seen;
        for (int r = 0; r < 9; r++)
            if (board[r][c] != '.' && !seen.insert(board[r][c]).second) return false;
    }
    // boxes
    for (int br = 0; br < 9; br += 3)
        for (int bc = 0; bc < 9; bc += 3) {
            set<char> seen;
            for (int r = br; r < br+3; r++)
                for (int c = bc; c < bc+3; c++)
                    if (board[r][c] != '.' && !seen.insert(board[r][c]).second) return false;
        }
    return true;
}
```
```java
public boolean isValidSudoku(char[][] board) {
    // rows
    for (int r = 0; r < 9; r++) {
        Set<Character> seen = new HashSet<>();
        for (int c = 0; c < 9; c++)
            if (board[r][c] != '.' && !seen.add(board[r][c])) return false;
    }
    // cols
    for (int c = 0; c < 9; c++) {
        Set<Character> seen = new HashSet<>();
        for (int r = 0; r < 9; r++)
            if (board[r][c] != '.' && !seen.add(board[r][c])) return false;
    }
    // boxes
    for (int br = 0; br < 9; br += 3)
        for (int bc = 0; bc < 9; bc += 3) {
            Set<Character> seen = new HashSet<>();
            for (int r = br; r < br+3; r++)
                for (int c = bc; c < bc+3; c++)
                    if (board[r][c] != '.' && !seen.add(board[r][c])) return false;
        }
    return true;
}
```
```python
def isValidSudoku(board):
    def ok(cells):
        vals = [x for x in cells if x != '.']
        return len(vals) == len(set(vals))
    # rows
    for r in range(9):
        if not ok(board[r]): return False
    # cols
    for c in range(9):
        if not ok([board[r][c] for r in range(9)]): return False
    # boxes
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            box = [board[r][c] for r in range(br, br+3) for c in range(bc, bc+3)]
            if not ok(box): return False
    return True
```

### Complexity
- **Time**: O(81) = O(1) (board is fixed size, but conceptually O(n²) for an n×n board).
- **Space**: O(9) per check.

### Verdict
Clear and correct. We traverse the board three times. We can do it in one pass.

---

## Approach 2 — One pass with three sets (optimal) ⭐

### Intuition
For each cell, simultaneously check and record its digit in the row set, column set, and box set. One traversal, all three rules.

### Algorithm
1. Maintain `rows[9]`, `cols[9]`, `boxes[9]` sets.
2. For each cell `(r,c)` that isn't `'.'`:
   - `b = (r/3)*3 + c/3`.
   - If the digit is in `rows[r]`, `cols[c]`, or `boxes[b]` → return `false`.
   - Insert it into all three.
3. Return `true`.

### Dry run (conflict case)
```
Suppose board[0][0]='8' and board[3][0]='8' (same column 0).
At (0,0): insert 8 into rows[0], cols[0], boxes[0].
At (3,0): 8 already in cols[0] → return false.
```

### Code
```cpp
bool isValidSudoku(vector<vector<char>>& board) {
    vector<set<char>> rows(9), cols(9), boxes(9);
    for (int r = 0; r < 9; r++)
        for (int c = 0; c < 9; c++) {
            char v = board[r][c];
            if (v == '.') continue;
            int b = (r / 3) * 3 + c / 3;
            if (rows[r].count(v) || cols[c].count(v) || boxes[b].count(v))
                return false;
            rows[r].insert(v);
            cols[c].insert(v);
            boxes[b].insert(v);
        }
    return true;
}
```
```java
public boolean isValidSudoku(char[][] board) {
    List<Set<Character>> rows = new ArrayList<>(), cols = new ArrayList<>(), boxes = new ArrayList<>();
    for (int i = 0; i < 9; i++) {
        rows.add(new HashSet<>());
        cols.add(new HashSet<>());
        boxes.add(new HashSet<>());
    }
    for (int r = 0; r < 9; r++)
        for (int c = 0; c < 9; c++) {
            char v = board[r][c];
            if (v == '.') continue;
            int b = (r / 3) * 3 + c / 3;
            if (rows.get(r).contains(v) || cols.get(c).contains(v) || boxes.get(b).contains(v))
                return false;
            rows.get(r).add(v);
            cols.get(c).add(v);
            boxes.get(b).add(v);
        }
    return true;
}
```
```python
def isValidSudoku(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    for r in range(9):
        for c in range(9):
            v = board[r][c]
            if v == '.':
                continue
            b = (r // 3) * 3 + c // 3
            if v in rows[r] or v in cols[c] or v in boxes[b]:
                return False
            rows[r].add(v); cols[c].add(v); boxes[b].add(v)
    return True
```

### Complexity
- **Time**: O(81) = O(1) for a 9×9 board.
- **Space**: O(81) = O(1) for the fixed sets.

### Verdict
**The optimal answer.** Single pass, all three constraints, the elegant box-index formula. This is the expected interview solution.

---

## Approach 3 — Bitmask sets (micro-optimization)

### Intuition
Replace each set with a 9-bit integer; bit `d` means "digit d+1 seen". Checking/setting is a bit-AND/OR. Same O(1) but no hashing overhead.

### Code
```cpp
bool isValidSudoku(vector<vector<char>>& board) {
    int rows[9] = {0}, cols[9] = {0}, boxes[9] = {0};
    for (int r = 0; r < 9; r++)
        for (int c = 0; c < 9; c++) {
            if (board[r][c] == '.') continue;
            int d = board[r][c] - '1';        // 0..8
            int mask = 1 << d;
            int b = (r / 3) * 3 + c / 3;
            if ((rows[r] & mask) || (cols[c] & mask) || (boxes[b] & mask))
                return false;
            rows[r] |= mask; cols[c] |= mask; boxes[b] |= mask;
        }
    return true;
}
```
```java
public boolean isValidSudoku(char[][] board) {
    int[] rows = new int[9], cols = new int[9], boxes = new int[9];
    for (int r = 0; r < 9; r++)
        for (int c = 0; c < 9; c++) {
            if (board[r][c] == '.') continue;
            int d = board[r][c] - '1';        // 0..8
            int mask = 1 << d;
            int b = (r / 3) * 3 + c / 3;
            if ((rows[r] & mask) != 0 || (cols[c] & mask) != 0 || (boxes[b] & mask) != 0)
                return false;
            rows[r] |= mask; cols[c] |= mask; boxes[b] |= mask;
        }
    return true;
}
```

### Verdict
Fastest in practice; a great "can you optimize further?" follow-up. Functionally identical to Approach 2.

---

## ⚖️ Approach comparison

| Approach | Passes | Space | Notes |
|----------|--------|-------|-------|
| Three passes | 3 | O(9) | clearest to reason about |
| One pass + sets | 1 | O(81) | the standard optimal ⭐ |
| One pass + bitmask | 1 | O(9) ints | fastest, no hashing |

---

## 🧪 Edge cases & pitfalls
- **Empty cells (`.`)** are skipped — only filled digits are validated.
- **Box index formula**: `(r/3)*3 + c/3` — a common bug is writing `r/3 + c/3` (collapses distinct boxes).
- **We only check current validity**, not solvability — don't try to solve the puzzle.

---

## 🔗 Related problems
- **Sudoku Solver** (LC 37) — actually solve it via backtracking (uses this validity check).
- **N-Queens** (LC 51) — similar diagonal/column constraint tracking with sets/bitmasks.

---

**→ Done with Arrays & Hashing.** Next topic: Two Pointers (folder `02-Two-Pointers/`). | Prev: [`07-Longest-Consecutive-Sequence.md`](./07-Longest-Consecutive-Sequence.md) | [Index](./00-Index.md)
