# Spiral Matrix

**Platform**: LeetCode 54 · **Difficulty**: Medium · **Topics**: Array, Matrix, Simulation · **Pattern**: Four shrinking boundaries

---

## 📜 Problem Statement

Given an `m x n` `matrix`, return *all elements of the* `matrix` *in spiral order*.

### Examples

**Example 1:**
```
Input:  matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [1,2,3,6,9,8,7,4,5]
```

**Example 2:**
```
Input:  matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
Output: [1,2,3,4,8,12,11,10,9,5,6,7]
```

**Example 3:**
```
Input:  matrix = [[7]]
Output: [7]
```

### Constraints
```
m == matrix.length
n == matrix[i].length
1 <= m, n <= 10
-100 <= matrix[i][j] <= 100
```

---

## 🧠 Understanding the problem

A spiral walks: across the top row left→right, down the right column, across the bottom row right→left, up the left column — then repeats one layer inward. The clean way to model this is with **four boundaries**: `top`, `bottom`, `left`, `right`. After traversing a side, we move that boundary inward (e.g. after the top row, `top++`).

The subtlety: for non-square matrices, after doing the top row and right column, you must re-check that there's still a row left (`top <= bottom`) before traversing the bottom row, and a column left (`left <= right`) before the left column. Without those checks, a single remaining row or column gets traversed twice.

---

## Approach 1 — Four shrinking boundaries (optimal) ⭐

### Intuition
Keep contracting a rectangle. Each loop iteration peels one full outer ring: right along `top`, down along `right`, left along `bottom`, up along `left`, shrinking each boundary as it's consumed.

### Algorithm
1. `top=0, bottom=m-1, left=0, right=n-1`, `res=[]`.
2. While `top <= bottom` and `left <= right`:
   - Left→right along `top`; then `top++`.
   - Top→bottom along `right`; then `right--`.
   - If `top <= bottom`: right→left along `bottom`; then `bottom--`.
   - If `left <= right`: bottom→top along `left`; then `left++`.
3. Return `res`.

### Dry run on `[[1,2,3],[4,5,6],[7,8,9]]`
```
top=0..: row0 → 1,2,3; top=1
right col → 6,9; right=1
bottom row (top<=bottom) → 8,7; bottom=1
left col (left<=right) → 4; left=1
loop: top=1,bottom=1,left=1,right=1 → row1 → 5; top=2 (>bottom) stop
res = [1,2,3,6,9,8,7,4,5]  ✓
```

### Code
```cpp
vector<int> spiralOrder(vector<vector<int>>& matrix) {
    vector<int> res;
    int top = 0, bottom = matrix.size() - 1;
    int left = 0, right = matrix[0].size() - 1;
    while (top <= bottom && left <= right) {
        for (int c = left; c <= right; c++) res.push_back(matrix[top][c]);
        top++;
        for (int r = top; r <= bottom; r++) res.push_back(matrix[r][right]);
        right--;
        if (top <= bottom) {
            for (int c = right; c >= left; c--) res.push_back(matrix[bottom][c]);
            bottom--;
        }
        if (left <= right) {
            for (int r = bottom; r >= top; r--) res.push_back(matrix[r][left]);
            left++;
        }
    }
    return res;
}
```
```java
public List<Integer> spiralOrder(int[][] matrix) {
    List<Integer> res = new ArrayList<>();
    int top = 0, bottom = matrix.length - 1;
    int left = 0, right = matrix[0].length - 1;
    while (top <= bottom && left <= right) {
        for (int c = left; c <= right; c++) res.add(matrix[top][c]);
        top++;
        for (int r = top; r <= bottom; r++) res.add(matrix[r][right]);
        right--;
        if (top <= bottom) {
            for (int c = right; c >= left; c--) res.add(matrix[bottom][c]);
            bottom--;
        }
        if (left <= right) {
            for (int r = bottom; r >= top; r--) res.add(matrix[r][left]);
            left++;
        }
    }
    return res;
}
```
```python
def spiralOrder(matrix):
    res = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            res.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):
            res.append(matrix[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                res.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                res.append(matrix[r][left])
            left += 1
    return res
```

### Complexity
- **Time**: O(m·n) — each cell appended exactly once.
- **Space**: O(1) extra (besides the output).

### Verdict
**Optimal.** The boundary method is the standard, and the two inner `if` guards are the only tricky part.

---

## Approach 2 — Direction vectors with a visited marker

### Intuition
Walk one step at a time, turning right whenever the next cell is out of bounds or already visited. Uses a direction array `[(0,1),(1,0),(0,-1),(-1,0)]` (right, down, left, up).

### Algorithm
1. Start at `(0,0)`, direction index `d=0`.
2. For `m*n` steps: record the cell, mark visited; compute the next cell; if it's invalid/visited, turn right (`d = (d+1)%4`) and recompute; move.

### Dry run on `[[1,2,3],[4,5,6],[7,8,9]]`
```
move right 1,2,3 → blocked → turn down 6,9 → blocked → turn left 8,7
→ blocked → turn up 4 → blocked → turn right 5 → done
res = [1,2,3,6,9,8,7,4,5]  ✓
```

### Code
```cpp
vector<int> spiralOrder(vector<vector<int>>& matrix) {
    int m = matrix.size(), n = matrix[0].size();
    vector<vector<bool>> seen(m, vector<bool>(n, false));
    int dr[] = {0, 1, 0, -1}, dc[] = {1, 0, -1, 0};
    vector<int> res;
    int r = 0, c = 0, d = 0;
    for (int k = 0; k < m * n; k++) {
        res.push_back(matrix[r][c]);
        seen[r][c] = true;
        int nr = r + dr[d], nc = c + dc[d];
        if (nr < 0 || nr >= m || nc < 0 || nc >= n || seen[nr][nc]) {
            d = (d + 1) % 4;
            nr = r + dr[d]; nc = c + dc[d];
        }
        r = nr; c = nc;
    }
    return res;
}
```
```java
public List<Integer> spiralOrder(int[][] matrix) {
    int m = matrix.length, n = matrix[0].length;
    boolean[][] seen = new boolean[m][n];
    int[] dr = {0, 1, 0, -1}, dc = {1, 0, -1, 0};
    List<Integer> res = new ArrayList<>();
    int r = 0, c = 0, d = 0;
    for (int k = 0; k < m * n; k++) {
        res.add(matrix[r][c]);
        seen[r][c] = true;
        int nr = r + dr[d], nc = c + dc[d];
        if (nr < 0 || nr >= m || nc < 0 || nc >= n || seen[nr][nc]) {
            d = (d + 1) % 4;
            nr = r + dr[d]; nc = c + dc[d];
        }
        r = nr; c = nc;
    }
    return res;
}
```
```python
def spiralOrder(matrix):
    m, n = len(matrix), len(matrix[0])
    seen = [[False] * n for _ in range(m)]
    dr, dc = [0, 1, 0, -1], [1, 0, -1, 0]
    res = []
    r = c = d = 0
    for _ in range(m * n):
        res.append(matrix[r][c])
        seen[r][c] = True
        nr, nc = r + dr[d], c + dc[d]
        if not (0 <= nr < m and 0 <= nc < n) or seen[nr][nc]:
            d = (d + 1) % 4
            nr, nc = r + dr[d], c + dc[d]
        r, c = nr, nc
    return res
```

### Complexity
- **Time**: O(m·n).
- **Space**: O(m·n) for the `seen` grid (can be reduced by marking the matrix itself if mutation is allowed).

### Verdict
Conceptually clean ("walk and turn"), but it costs extra space for `seen`. The boundary method is preferred for its O(1) extra space.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Four boundaries | **O(mn)** | **O(1)** | recommended ⭐ |
| Direction + visited | O(mn) | O(mn) | clean logic, extra grid |

---

## 🧪 Edge cases & pitfalls
- **Single row** (`[[1,2,3]]`) → top row prints, then the `top <= bottom` guard stops the bottom-row pass from re-printing it.
- **Single column** → symmetric; the `left <= right` guard prevents double traversal.
- **`1×1`** → returns the single element.
- **Pitfall — missing inner `if` checks**: after `top++` and `right--`, a thin remaining strip can be traversed twice without the `top <= bottom` / `left <= right` guards.
- **Pitfall — empty matrix**: guard `matrix[0]` access if the problem allows `0` rows (the constraints here guarantee `m,n >= 1`).

---

## 🔗 Related problems
- **Spiral Matrix II** (LC 59) — fill an `n×n` matrix in spiral order.
- **Spiral Matrix III** (LC 885) — spiral from an arbitrary start, off-grid steps.
- **Rotate Image** (LC 48) — another boundary/index exercise (previous).
- **Diagonal Traverse** (LC 498) — directional matrix walk.

---

**→ Next:** [`03-Set-Matrix-Zeroes.md`](./03-Set-Matrix-Zeroes.md) | **Prev:** [`01-Rotate-Image.md`](./01-Rotate-Image.md) | [Problem set index](./00-Index.md)
