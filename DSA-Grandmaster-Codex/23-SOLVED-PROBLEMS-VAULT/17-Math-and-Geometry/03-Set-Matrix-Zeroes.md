# Set Matrix Zeroes

**Platform**: LeetCode 73 · **Difficulty**: Medium · **Topics**: Array, Hash Table, Matrix · **Pattern**: In-place markers (first row/col)

---

## 📜 Problem Statement

Given an `m x n` integer matrix `matrix`, if an element is `0`, set its entire row and column to `0`'s.

You must do it **in place**.

### Examples

**Example 1:**
```
Input:  matrix = [[1,1,1],[1,0,1],[1,1,1]]
Output: [[1,0,1],[0,0,0],[1,0,1]]
```

**Example 2:**
```
Input:  matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
Output: [[0,0,0,0],[0,4,5,0],[0,3,1,0]]
```

**Example 3:**
```
Input:  matrix = [[1,2,3]]
Output: [[1,2,3]]
Explanation: No zeros, nothing changes.
```

### Constraints
```
m == matrix.length
n == matrix[0].length
1 <= m, n <= 200
-2^31 <= matrix[i][j] <= 2^31 - 1
```

**Follow up**: A straightforward O(mn) space solution is trivial. Could you devise an O(m + n) solution? Could you devise a solution with O(1) space?

---

## 🧠 Understanding the problem

The trap is **order of operations**: if you naively zero a row's column the moment you see a `0`, you'll create new zeros and then wrongly propagate *those*. You must first **find** all the original zero positions, then apply the zeroing.

Three levels of space efficiency:

1. **O(mn)**: copy the matrix; decide zeros from the copy.
2. **O(m+n)**: record which rows and which columns contain a zero in two boolean arrays, then zero accordingly.
3. **O(1)** (the follow-up): reuse the matrix's own **first row and first column** as those marker arrays. Because the first row/col would themselves get clobbered, track separately (with two booleans) whether the first row and first column originally contained a zero, and handle them last.

---

## Approach 1 — Two marker arrays, O(m+n) space

### Intuition
Scan once to flag every row and column that holds a zero. Scan again to zero any cell whose row or column was flagged.

### Algorithm
1. `rowZero[m]`, `colZero[n]`, all false.
2. Pass 1: for each `0` at `(r,c)`, set `rowZero[r] = colZero[c] = true`.
3. Pass 2: zero `matrix[r][c]` if `rowZero[r] || colZero[c]`.

### Dry run on `[[1,1,1],[1,0,1],[1,1,1]]`
```
pass1: zero at (1,1) → rowZero[1]=true, colZero[1]=true
pass2: zero cells where row==1 or col==1
→ [[1,0,1],[0,0,0],[1,0,1]]  ✓
```

### Code
```cpp
void setZeroes(vector<vector<int>>& matrix) {
    int m = matrix.size(), n = matrix[0].size();
    vector<bool> rowZero(m, false), colZero(n, false);
    for (int r = 0; r < m; r++)
        for (int c = 0; c < n; c++)
            if (matrix[r][c] == 0) { rowZero[r] = true; colZero[c] = true; }
    for (int r = 0; r < m; r++)
        for (int c = 0; c < n; c++)
            if (rowZero[r] || colZero[c]) matrix[r][c] = 0;
}
```
```java
public void setZeroes(int[][] matrix) {
    int m = matrix.length, n = matrix[0].length;
    boolean[] rowZero = new boolean[m], colZero = new boolean[n];
    for (int r = 0; r < m; r++)
        for (int c = 0; c < n; c++)
            if (matrix[r][c] == 0) { rowZero[r] = true; colZero[c] = true; }
    for (int r = 0; r < m; r++)
        for (int c = 0; c < n; c++)
            if (rowZero[r] || colZero[c]) matrix[r][c] = 0;
}
```
```python
def setZeroes(matrix):
    m, n = len(matrix), len(matrix[0])
    row_zero = [False] * m
    col_zero = [False] * n
    for r in range(m):
        for c in range(n):
            if matrix[r][c] == 0:
                row_zero[r] = True
                col_zero[c] = True
    for r in range(m):
        for c in range(n):
            if row_zero[r] or col_zero[c]:
                matrix[r][c] = 0
```

### Complexity
- **Time**: O(m·n).
- **Space**: O(m + n).

### Verdict
Clean and correct, answers the O(m+n) follow-up. The O(1) version pushes the markers into the matrix itself.

---

## Approach 2 — First row/column as markers, O(1) space (optimal) ⭐

### Intuition
Use `matrix[r][0]` and `matrix[0][c]` as the `rowZero`/`colZero` flags. The catch: `matrix[0][0]` would serve double duty, so track the first row and first column with two separate booleans, and zero them **last** so they don't corrupt the marker reads.

### Algorithm
1. `firstRow` = does row 0 contain a zero? `firstCol` = does col 0 contain a zero?
2. For `r,c` in the inner region (`r>=1, c>=1`): if `matrix[r][c]==0`, set `matrix[r][0]=0` and `matrix[0][c]=0`.
3. For the inner region: zero `matrix[r][c]` if `matrix[r][0]==0` or `matrix[0][c]==0`.
4. If `firstRow`, zero all of row 0. If `firstCol`, zero all of col 0.

### Dry run on `[[0,1,2,0],[3,4,5,2],[1,3,1,5]]`
```
firstRow: row0 has 0 → true; firstCol: col0 has 0 → true
mark inner zeros: none in r>=1,c>=1 are 0 originally... col3 had 0 at (0,3) → that's row0, handled by firstRow
apply inner: nothing flagged inner
zero firstRow → row0 all 0; zero firstCol → col0 all 0
→ [[0,0,0,0],[0,4,5,0(? )]] — but (0,3)=0 set col3 marker via firstRow? 
Trace carefully: original zeros at (0,0) and (0,3) are BOTH in row 0.
firstRow=true handles row0. Column 0 and column 3 must also be zeroed.
(0,0)=0 → col0 via firstCol=true. (0,3)=0 → need col3 zeroed: marker matrix[0][3]
is in row 0, so set during the firstRow scan? We set matrix[0][3] stays 0 (it IS 0),
so inner apply sees matrix[0][3]==0 → zeroes column 3 for r>=1.
Result: [[0,0,0,0],[0,4,5,0],[0,3,1,0]]  ✓
```

### Code
```cpp
void setZeroes(vector<vector<int>>& matrix) {
    int m = matrix.size(), n = matrix[0].size();
    bool firstRow = false, firstCol = false;
    for (int c = 0; c < n; c++) if (matrix[0][c] == 0) firstRow = true;
    for (int r = 0; r < m; r++) if (matrix[r][0] == 0) firstCol = true;
    for (int r = 1; r < m; r++)
        for (int c = 1; c < n; c++)
            if (matrix[r][c] == 0) { matrix[r][0] = 0; matrix[0][c] = 0; }
    for (int r = 1; r < m; r++)
        for (int c = 1; c < n; c++)
            if (matrix[r][0] == 0 || matrix[0][c] == 0) matrix[r][c] = 0;
    if (firstRow) for (int c = 0; c < n; c++) matrix[0][c] = 0;
    if (firstCol) for (int r = 0; r < m; r++) matrix[r][0] = 0;
}
```
```java
public void setZeroes(int[][] matrix) {
    int m = matrix.length, n = matrix[0].length;
    boolean firstRow = false, firstCol = false;
    for (int c = 0; c < n; c++) if (matrix[0][c] == 0) firstRow = true;
    for (int r = 0; r < m; r++) if (matrix[r][0] == 0) firstCol = true;
    for (int r = 1; r < m; r++)
        for (int c = 1; c < n; c++)
            if (matrix[r][c] == 0) { matrix[r][0] = 0; matrix[0][c] = 0; }
    for (int r = 1; r < m; r++)
        for (int c = 1; c < n; c++)
            if (matrix[r][0] == 0 || matrix[0][c] == 0) matrix[r][c] = 0;
    if (firstRow) for (int c = 0; c < n; c++) matrix[0][c] = 0;
    if (firstCol) for (int r = 0; r < m; r++) matrix[r][0] = 0;
}
```
```python
def setZeroes(matrix):
    m, n = len(matrix), len(matrix[0])
    first_row = any(matrix[0][c] == 0 for c in range(n))
    first_col = any(matrix[r][0] == 0 for r in range(m))
    for r in range(1, m):
        for c in range(1, n):
            if matrix[r][c] == 0:
                matrix[r][0] = 0
                matrix[0][c] = 0
    for r in range(1, m):
        for c in range(1, n):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0
    if first_row:
        for c in range(n):
            matrix[0][c] = 0
    if first_col:
        for r in range(m):
            matrix[r][0] = 0
```

### Complexity
- **Time**: O(m·n).
- **Space**: O(1) — only two booleans beyond the matrix.

### Verdict
**The optimal answer** to the follow-up. The only trick is treating the first row/column specially because they double as marker storage.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Copy matrix | O(mn) | O(mn) | trivial baseline |
| Two marker arrays | O(mn) | O(m+n) | clean, answers first follow-up |
| First row/col markers | **O(mn)** | **O(1)** | optimal follow-up ⭐ |

---

## 🧪 Edge cases & pitfalls
- **Zero in the first row or first column** → handled by the `firstRow`/`firstCol` booleans applied last.
- **No zeros** → nothing changes.
- **All zeros** → entire matrix stays zero.
- **Pitfall — applying markers to row 0 / col 0 too early**: you must zero the first row and column *after* using them as markers, or you'd destroy the flags mid-pass.
- **Pitfall — eager zeroing**: setting a whole row/column the moment you see a zero (without a marker pass) propagates spurious zeros. Always separate "detect" from "apply."

---

## 🔗 Related problems
- **Rotate Image** (LC 48) — in-place matrix editing (earlier).
- **Game of Life** (LC 289) — in-place state update with encoded markers.
- **Spiral Matrix** (LC 54) — index discipline (previous).
- **Valid Sudoku** (LC 36) — row/column/box bookkeeping.

---

**→ Next:** [`04-Pow-X-N.md`](./04-Pow-X-N.md) | **Prev:** [`02-Spiral-Matrix.md`](./02-Spiral-Matrix.md) | [Problem set index](./00-Index.md)
