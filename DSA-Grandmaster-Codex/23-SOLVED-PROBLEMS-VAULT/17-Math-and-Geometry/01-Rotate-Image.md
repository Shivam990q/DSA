# Rotate Image

**Platform**: LeetCode 48 · **Difficulty**: Medium · **Topics**: Array, Math, Matrix · **Pattern**: Transpose + reverse / 4-way cycle

---

## 📜 Problem Statement

You are given an `n x n` 2D `matrix` representing an image. Rotate the image by **90 degrees (clockwise)**.

You have to rotate the image **in-place**, which means you have to modify the input 2D matrix directly. **DO NOT** allocate another 2D matrix and do the rotation.

### Examples

**Example 1:**
```
Input:  matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [[7,4,1],[8,5,2],[9,6,3]]
```

**Example 2:**
```
Input:  matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
Output: [[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]
```

**Example 3:**
```
Input:  matrix = [[1]]
Output: [[1]]
```

### Constraints
```
n == matrix.length == matrix[i].length
1 <= n <= 20
-1000 <= matrix[i][j] <= 1000
```

---

## 🧠 Understanding the problem

A 90° clockwise rotation sends the element at `(row, col)` to `(col, n-1-row)`. The top row becomes the right column, the left column becomes the top row, and so on.

The cleanest in-place recipe decomposes this single rotation into two elementary operations:

1. **Transpose** — reflect across the main diagonal: swap `matrix[i][j]` with `matrix[j][i]`. This turns rows into columns.
2. **Reverse each row** — flip every row left-to-right.

Compose them and you get exactly the clockwise rotation. Both steps touch each cell O(1) times and need no second matrix. (For counter-clockwise: reverse each row *first*, then transpose — or transpose then reverse each *column*.)

---

## Approach 1 — Use an auxiliary matrix (not allowed, but the baseline)

### Intuition
Allocate a fresh `n×n` grid and copy each element to its rotated position `result[j][n-1-i] = matrix[i][j]`. Simple, but violates the in-place rule.

### Algorithm
1. Make `res` of size `n×n`.
2. For each `(i, j)`: `res[j][n-1-i] = matrix[i][j]`.
3. Copy `res` back into `matrix`.

### Dry run on `[[1,2,3],[4,5,6],[7,8,9]]`
```
(0,0)=1 → res[0][2]
(0,1)=2 → res[1][2]
(0,2)=3 → res[2][2]
... → res = [[7,4,1],[8,5,2],[9,6,3]]
```

### Code
```cpp
void rotate(vector<vector<int>>& matrix) {
    int n = matrix.size();
    vector<vector<int>> res(n, vector<int>(n));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            res[j][n - 1 - i] = matrix[i][j];
    matrix = res;
}
```
```java
public void rotate(int[][] matrix) {
    int n = matrix.length;
    int[][] res = new int[n][n];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            res[j][n - 1 - i] = matrix[i][j];
    for (int i = 0; i < n; i++)
        matrix[i] = res[i];
}
```
```python
def rotate(matrix):
    n = len(matrix)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            res[j][n - 1 - i] = matrix[i][j]
    for i in range(n):
        matrix[i] = res[i]
```

### Complexity
- **Time**: O(n²).
- **Space**: O(n²) — disallowed by the problem.

### Verdict
Trivially correct and a good sanity check, but it breaks the in-place constraint. Use it only to verify the in-place versions.

---

## Approach 2 — Transpose, then reverse each row (optimal) ⭐

### Intuition
Transpose to swap the matrix across its diagonal, then reverse each row to complete the clockwise turn. Two clean passes, O(1) extra space.

### Algorithm
1. Transpose: for `i` in `0..n-1`, for `j` in `i+1..n-1`, swap `matrix[i][j]` and `matrix[j][i]`.
2. Reverse each row.

### Dry run on `[[1,2,3],[4,5,6],[7,8,9]]`
```
transpose → [[1,4,7],[2,5,8],[3,6,9]]
reverse rows → [[7,4,1],[8,5,2],[9,6,3]]  ✓
```

### Code
```cpp
void rotate(vector<vector<int>>& matrix) {
    int n = matrix.size();
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            swap(matrix[i][j], matrix[j][i]);      // transpose
    for (int i = 0; i < n; i++)
        reverse(matrix[i].begin(), matrix[i].end()); // reverse each row
}
```
```java
public void rotate(int[][] matrix) {
    int n = matrix.length;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++) {
            int tmp = matrix[i][j];
            matrix[i][j] = matrix[j][i];
            matrix[j][i] = tmp;
        }
    for (int i = 0; i < n; i++) {
        int lo = 0, hi = n - 1;
        while (lo < hi) {
            int tmp = matrix[i][lo];
            matrix[i][lo] = matrix[i][hi];
            matrix[i][hi] = tmp;
            lo++; hi--;
        }
    }
}
```
```python
def rotate(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()
```

### Complexity
- **Time**: O(n²) — every cell touched a constant number of times.
- **Space**: O(1).

### Verdict
**The optimal answer.** Two intuitive sub-steps, no extra matrix. This is what to present; it's the easiest to get right under pressure.

---

## Approach 3 — Four-way ring rotation (in-place, direct)

### Intuition
Rotate the matrix layer by layer (rings from outside in). For each ring, rotate four elements at a time in a cycle: top-left ← bottom-left ← bottom-right ← top-right ← top-left.

### Algorithm
1. For each layer `l` from `0` to `n/2 - 1`:
   - For `i` from `l` to `n-1-l-1`:
     - Save the top element; move left→top, bottom→left, right→bottom, top(saved)→right.

### Dry run on `[[1,2,3],[4,5,6],[7,8,9]]`
```
layer 0, i=0 (corners): 1,7,9,3 cycle clockwise → 7,? ... yields
top row becomes 7,4,1; bottom becomes 9,6,3; center 5 fixed
result [[7,4,1],[8,5,2],[9,6,3]]  ✓
```

### Code
```cpp
void rotate(vector<vector<int>>& matrix) {
    int n = matrix.size();
    for (int l = 0; l < n / 2; l++) {
        for (int i = l; i < n - 1 - l; i++) {
            int top = matrix[l][i];
            matrix[l][i]             = matrix[n - 1 - i][l];
            matrix[n - 1 - i][l]     = matrix[n - 1 - l][n - 1 - i];
            matrix[n - 1 - l][n - 1 - i] = matrix[i][n - 1 - l];
            matrix[i][n - 1 - l]     = top;
        }
    }
}
```
```java
public void rotate(int[][] matrix) {
    int n = matrix.length;
    for (int l = 0; l < n / 2; l++) {
        for (int i = l; i < n - 1 - l; i++) {
            int top = matrix[l][i];
            matrix[l][i]                 = matrix[n - 1 - i][l];
            matrix[n - 1 - i][l]         = matrix[n - 1 - l][n - 1 - i];
            matrix[n - 1 - l][n - 1 - i] = matrix[i][n - 1 - l];
            matrix[i][n - 1 - l]         = top;
        }
    }
}
```
```python
def rotate(matrix):
    n = len(matrix)
    for l in range(n // 2):
        for i in range(l, n - 1 - l):
            top = matrix[l][i]
            matrix[l][i] = matrix[n - 1 - i][l]
            matrix[n - 1 - i][l] = matrix[n - 1 - l][n - 1 - i]
            matrix[n - 1 - l][n - 1 - i] = matrix[i][n - 1 - l]
            matrix[i][n - 1 - l] = top
```

### Complexity
- **Time**: O(n²).
- **Space**: O(1).

### Verdict
Same complexity, no extra space, but the index arithmetic is error-prone. Most people prefer Approach 2; this one is worth knowing for the "do it in one pass" follow-up.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Auxiliary matrix | O(n²) | O(n²) | violates in-place rule |
| Transpose + reverse | **O(n²)** | **O(1)** | cleanest, recommended ⭐ |
| 4-way ring | O(n²) | O(1) | single pass, fiddly indices |

---

## 🧪 Edge cases & pitfalls
- **`n = 1`** → nothing to do; both in-place methods are no-ops.
- **Even vs odd `n`** → Approach 2 handles both seamlessly; the ring method's center stays fixed for odd `n` (loop bounds exclude it).
- **Counter-clockwise** → reverse each row first, then transpose (or transpose then reverse columns).
- **Pitfall — transpose loop bounds**: start the inner loop at `j = i + 1`. Starting at `j = 0` swaps every pair twice and undoes the transpose.
- **Pitfall**: allocating a new matrix and reassigning — that violates the explicit in-place requirement even if the output looks right.

---

## 🔗 Related problems
- **Spiral Matrix** (LC 54) — boundary traversal (next).
- **Set Matrix Zeroes** (LC 73) — in-place matrix editing.
- **Transpose Matrix** (LC 867) — just step 1.
- **Rotate Array** (LC 189) — the 1D reverse-trick analog.

---

**→ Next:** [`02-Spiral-Matrix.md`](./02-Spiral-Matrix.md) | [Problem set index](./00-Index.md)
