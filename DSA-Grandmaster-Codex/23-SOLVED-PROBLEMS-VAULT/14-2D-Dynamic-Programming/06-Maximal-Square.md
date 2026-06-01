# Maximal Square

**Platform**: LeetCode 221 · **Difficulty**: Medium · **Topics**: Array, Dynamic Programming, Matrix · **Pattern**: Grid DP — square side at bottom-right corner

---

## 📜 Problem Statement

Given an `m x n` binary `matrix` filled with `0`'s and `1`'s, find the largest **square** containing only `1`'s and return its **area**.

### Examples

**Example 1:**
```
Input:  matrix = [["1","0","1","0","0"],
                  ["1","0","1","1","1"],
                  ["1","1","1","1","1"],
                  ["1","0","0","1","0"]]
Output: 4
Explanation: The largest all-ones square has side 2, area 4.
```

**Example 2:**
```
Input:  matrix = [["0","1"],
                  ["1","0"]]
Output: 1
```

**Example 3:**
```
Input:  matrix = [["0"]]
Output: 0
```

### Constraints
```
m == matrix.length
n == matrix[i].length
1 <= m, n <= 300
matrix[i][j] is '0' or '1'.
```

---

## 🧠 Understanding the problem

We want the largest **square** (not rectangle) of all `1`s. The elegant DP insight: let `dp[i][j]` be the **side length of the largest all-ones square whose bottom-right corner is at cell `(i, j)`**.

A square of side `k` can end at `(i, j)` only if three smaller squares of side `k-1` end at the cell **above**, the cell to the **left**, and the cell **diagonally up-left** — and `(i, j)` itself is `1`. The largest side it can support is therefore:

> `dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])` when `matrix[i][j] == '1'`.

The `min` is the bottleneck: a square can only be as large as its smallest supporting neighbor allows. The answer is `(max dp)²`.

5-step framework:
1. **State**: `dp[i][j]` = side of the largest all-ones square ending at `(i, j)`.
2. **Transition**: cell is `1` → `1 + min(top, left, diagonal)`; cell is `0` → 0.
3. **Base case**: first row/column equal the cell's value (square of side 0 or 1).
4. **Order**: top-left to bottom-right.
5. **Answer**: `best²`, tracking the maximum `dp` value.

---

## Approach 1 — Brute force (expand every square)

### Intuition
For each cell that is `1`, try to grow a square: check whether all cells of a `k×k` block (top-left at that cell) are `1`, increasing `k` until it fails.

### Algorithm
1. For each top-left `(i, j)` with value `1`, expand `k = 1, 2, ...`; verify the new row and column of the `k×k` block are all `1`.
2. Track the largest valid `k`.

### Dry run on Example 2
```
(0,1)=1 -> can't grow (neighbors 0) -> side 1
(1,0)=1 -> side 1
best = 1 -> area 1
```

### Code
```cpp
class Solution {
public:
    int maximalSquare(vector<vector<char>>& matrix) {
        int m = matrix.size(), n = matrix[0].size(), best = 0;
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                if (matrix[i][j] == '1') {
                    int k = 1;
                    while (i + k <= m && j + k <= n) {
                        bool ok = true;
                        for (int r = i; r < i + k && ok; r++)
                            for (int c = j; c < j + k; c++)
                                if (matrix[r][c] == '0') { ok = false; break; }
                        if (ok) best = max(best, k);
                        else break;
                        k++;
                    }
                }
        return best * best;
    }
};
```
```java
class Solution {
    public int maximalSquare(char[][] matrix) {
        int m = matrix.length, n = matrix[0].length, best = 0;
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                if (matrix[i][j] == '1') {
                    int k = 1;
                    while (i + k <= m && j + k <= n) {
                        boolean ok = true;
                        for (int r = i; r < i + k && ok; r++)
                            for (int c = j; c < j + k; c++)
                                if (matrix[r][c] == '0') { ok = false; break; }
                        if (ok) best = Math.max(best, k);
                        else break;
                        k++;
                    }
                }
        return best * best;
    }
}
```
```python
class Solution:
    def maximalSquare(self, matrix: list[list[str]]) -> int:
        m, n = len(matrix), len(matrix[0])
        best = 0
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == '1':
                    k = 1
                    while i + k <= m and j + k <= n:
                        ok = all(matrix[r][c] == '1'
                                 for r in range(i, i + k)
                                 for c in range(j, j + k))
                        if ok:
                            best = max(best, k)
                        else:
                            break
                        k += 1
        return best * best
```

### Complexity
- **Time**: O(m × n × min(m,n)²) worst case.
- **Space**: O(1).

### Verdict
Correct but slow. The DP makes each cell O(1).

---

## Approach 2 — Bottom-up 2D DP (optimal idea) ⭐

### Intuition
Use `dp[i][j]` = largest square side ending at `(i, j)`. A padded `(m+1)×(n+1)` table lets the first real row/column read zeros above/left without special casing.

### Algorithm
1. `dp` is `(m+1)×(n+1)` zeros.
2. For each `(i, j)` (1-indexed into `dp`): if `matrix[i-1][j-1] == '1'`, `dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`; track `best`.
3. Return `best²`.

### Dry run on Example 1 (key cell)
```
At matrix (2,3) the three neighbors (up, left, diag) all have dp=1
-> dp=2 (side-2 square) -> best=2 -> area 4
```

### Code
```cpp
class Solution {
public:
    int maximalSquare(vector<vector<char>>& matrix) {
        int m = matrix.size(), n = matrix[0].size(), best = 0;
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        for (int i = 1; i <= m; i++)
            for (int j = 1; j <= n; j++)
                if (matrix[i - 1][j - 1] == '1') {
                    dp[i][j] = 1 + min({ dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1] });
                    best = max(best, dp[i][j]);
                }
        return best * best;
    }
};
```
```java
class Solution {
    public int maximalSquare(char[][] matrix) {
        int m = matrix.length, n = matrix[0].length, best = 0;
        int[][] dp = new int[m + 1][n + 1];
        for (int i = 1; i <= m; i++)
            for (int j = 1; j <= n; j++)
                if (matrix[i - 1][j - 1] == '1') {
                    dp[i][j] = 1 + Math.min(dp[i - 1][j - 1],
                                   Math.min(dp[i - 1][j], dp[i][j - 1]));
                    best = Math.max(best, dp[i][j]);
                }
        return best * best;
    }
}
```
```python
class Solution:
    def maximalSquare(self, matrix: list[list[str]]) -> int:
        m, n = len(matrix), len(matrix[0])
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        best = 0
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if matrix[i - 1][j - 1] == '1':
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
                    best = max(best, dp[i][j])
        return best * best
```

### Complexity
- **Time**: O(m × n).
- **Space**: O(m × n).

### Verdict
The clear, standard DP. Each cell reads only its top/left/diagonal, so it collapses to one row.

---

## Approach 3 — 1D rolling row (space optimized) ⭐

### Intuition
Process row by row with a single `dp` array of length `n+1`. The catch: `dp[i-1][j-1]` (the diagonal) gets overwritten when we compute `dp[i][j-1]`. So we stash the old `dp[j]` in a `prev` variable before overwriting it — that `prev` is the diagonal for the next column.

### Algorithm
1. `dp = [0]*(n+1)`.
2. For each row: `prev = 0` (this is `dp[i-1][j-1]` for j=1). For `j` 1..n: `temp = dp[j]`; if cell is `1`, `dp[j] = 1 + min(dp[j], dp[j-1], prev)` else `dp[j] = 0`; `prev = temp`; update `best`.
3. Return `best²`.

### Dry run intuition
```
dp holds the previous row. temp = dp[j] saves "top" before it becomes "current".
prev carries the diagonal forward. One row of memory suffices.
```

### Code
```cpp
class Solution {
public:
    int maximalSquare(vector<vector<char>>& matrix) {
        int m = matrix.size(), n = matrix[0].size(), best = 0;
        vector<int> dp(n + 1, 0);
        for (int i = 1; i <= m; i++) {
            int prev = 0;                       // dp[i-1][j-1] (diagonal)
            for (int j = 1; j <= n; j++) {
                int temp = dp[j];               // old dp[j] = top neighbor
                if (matrix[i - 1][j - 1] == '1') {
                    dp[j] = 1 + min({ dp[j], dp[j - 1], prev });
                    best = max(best, dp[j]);
                } else {
                    dp[j] = 0;
                }
                prev = temp;
            }
        }
        return best * best;
    }
};
```
```java
class Solution {
    public int maximalSquare(char[][] matrix) {
        int m = matrix.length, n = matrix[0].length, best = 0;
        int[] dp = new int[n + 1];
        for (int i = 1; i <= m; i++) {
            int prev = 0;
            for (int j = 1; j <= n; j++) {
                int temp = dp[j];
                if (matrix[i - 1][j - 1] == '1') {
                    dp[j] = 1 + Math.min(dp[j], Math.min(dp[j - 1], prev));
                    best = Math.max(best, dp[j]);
                } else {
                    dp[j] = 0;
                }
                prev = temp;
            }
        }
        return best * best;
    }
}
```
```python
class Solution:
    def maximalSquare(self, matrix: list[list[str]]) -> int:
        m, n = len(matrix), len(matrix[0])
        dp = [0] * (n + 1)
        best = 0
        for i in range(1, m + 1):
            prev = 0
            for j in range(1, n + 1):
                temp = dp[j]
                if matrix[i - 1][j - 1] == '1':
                    dp[j] = 1 + min(dp[j], dp[j - 1], prev)
                    best = max(best, dp[j])
                else:
                    dp[j] = 0
                prev = temp
        return best * best
```

### Complexity
- **Time**: O(m × n).
- **Space**: O(n).

### Verdict
**The space-optimal answer.** The `prev`/`temp` dance to preserve the diagonal is the one subtle part.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute force | O(mn·min(m,n)²) | O(1) | baseline, slow |
| 2D DP | O(mn) | O(mn) | clean, standard ⭐ |
| 1D rolling | O(mn) | **O(n)** | space optimum ⭐ |

---

## 🧪 Edge cases & pitfalls
- **All zeros** → 0.
- **Single cell** → 1 if `'1'`, else 0.
- **Returns area, not side**: the answer is `side²`. Forgetting to square is the most common mistake.
- **Pitfall — the `min` vs `max`**: the side is limited by the *smallest* of the three neighbors. Using `max` would claim squares that aren't fully filled.
- **Pitfall — char vs int**: the matrix holds characters `'0'`/`'1'`, not integers. Compare against `'1'`.
- **Pitfall — diagonal in 1D**: must capture `dp[j]` into `temp` *before* overwriting, then set `prev = temp` for the next column.

---

## 🔗 Related problems
- **Maximal Rectangle** (LC 85) — largest all-ones rectangle (histogram + stack per row).
- **Largest Rectangle in Histogram** (LC 84) — the subroutine behind Maximal Rectangle.
- **Count Square Submatrices with All Ones** (LC 1277) — same `dp`, but sum all `dp[i][j]` to count squares.
- **Maximal Square of 0s/Borders** — variants on the same corner-DP idea.

---

**→ Next:** [`07-Interleaving-String.md`](./07-Interleaving-String.md) | **→ Prev:** [`05-Target-Sum.md`](./05-Target-Sum.md) | Back to [`00-Index.md`](./00-Index.md)
