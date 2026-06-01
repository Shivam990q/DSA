# Search a 2D Matrix

**Platform**: LeetCode 74 · **Difficulty**: Medium · **Topics**: Array, Binary Search, Matrix · **Pattern**: Flatten to 1D sorted array

---

## 📜 Problem Statement

You are given an `m x n` integer matrix `matrix` with the following two properties:

- Each row is sorted in **non-decreasing** order.
- The first integer of each row is **greater than** the last integer of the previous row.

Given an integer `target`, return `true` if `target` is in `matrix` or `false` otherwise.

You must write a solution in **O(log(m * n))** time complexity.

### Examples

**Example 1:**
```
Input:  matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
Output: true
Explanation: 3 is in the first row at column 1.
```

**Example 2:**
```
Input:  matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
Output: false
Explanation: 13 lies between 11 and 16 but is not present.
```

**Example 3:**
```
Input:  matrix = [[1]], target = 1
Output: true
```

### Constraints
```
m == matrix.length
n == matrix[i].length
1 <= m, n <= 100
-10^4 <= matrix[i][j], target <= 10^4
```

---

## 🧠 Understanding the problem

The two properties together are the whole trick. Read them carefully:

1. Each **row** is sorted left to right.
2. The first element of each row is **larger than the last element of the previous row**.

Chain those two facts and you get something powerful: if you **concatenate the rows end to end**, the result is one big strictly-increasing sorted array of length `m * n`. Row 0, then row 1, then row 2 — the values only ever go up.

```
[[1,3,5,7],[10,11,16,20],[23,30,34,60]]
  flattened →  [1,3,5,7,10,11,16,20,23,30,34,60]   ← fully sorted!
```

So this isn't really a 2D problem at all. It's a **1D binary search wearing a 2D costume**. The only new skill is converting between a flat index `idx` and its `(row, col)` coordinates:

```
row = idx / n      (integer division)
col = idx % n
```

The required O(log(m·n)) confirms it: that's exactly the cost of binary searching `m·n` elements.

---

## Approach 1 — Brute force (scan every cell)

### Intuition
Ignore all structure and check every cell. Baseline only.

### Algorithm
1. For each row `r`, for each column `c`: if `matrix[r][c] == target` → return `true`.
2. Return `false`.

### Code

```cpp
class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        for (auto& row : matrix)
            for (int x : row)
                if (x == target) return true;
        return false;
    }
};
```
```java
class Solution {
    public boolean searchMatrix(int[][] matrix, int target) {
        for (int[] row : matrix)
            for (int x : row)
                if (x == target) return true;
        return false;
    }
}
```
```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        for row in matrix:
            for x in row:
                if x == target:
                    return True
        return False
```

### Complexity
- **Time**: O(m·n) — visits every cell.
- **Space**: O(1).

### Verdict
Correct but **violates the required O(log(m·n))**. It throws away both sorted properties. Baseline only.

---

## Approach 2 — Staircase search (row then column)

### Intuition
Use the sortedness partially: first binary search (or scan) to find which row *could* contain the target — the row whose last element is `>= target` and whose first element is `<= target`. Then binary search within that row.

A cleaner framing of the same idea: start at the **top-right corner**. From there, moving left decreases the value, moving down increases it. So each comparison eliminates either a full column or a full row.

### Algorithm (top-right staircase)
1. Start at `r = 0`, `c = n - 1`.
2. While `r < m` and `c >= 0`:
   - If `matrix[r][c] == target` → return `true`.
   - If `matrix[r][c] > target` → this column is too big everywhere below, move left (`c--`).
   - Else (`< target`) → this row is too small to the left, move down (`r++`).
3. Return `false`.

### Code

```cpp
class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int m = matrix.size(), n = matrix[0].size();
        int r = 0, c = n - 1;
        while (r < m && c >= 0) {
            if (matrix[r][c] == target) return true;
            else if (matrix[r][c] > target) c--;
            else r++;
        }
        return false;
    }
};
```
```java
class Solution {
    public boolean searchMatrix(int[][] matrix, int target) {
        int m = matrix.length, n = matrix[0].length;
        int r = 0, c = n - 1;
        while (r < m && c >= 0) {
            if (matrix[r][c] == target) return true;
            else if (matrix[r][c] > target) c--;
            else r++;
        }
        return false;
    }
}
```
```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        r, c = 0, n - 1
        while r < m and c >= 0:
            if matrix[r][c] == target:
                return True
            elif matrix[r][c] > target:
                c -= 1
            else:
                r += 1
        return False
```

### Complexity
- **Time**: O(m + n) — each step removes a row or a column.
- **Space**: O(1).

### Verdict
A neat O(m + n) that works even for the weaker LC 240 ("Search a 2D Matrix II", where only rows and columns are sorted). But for **this** problem the stronger guarantee lets us do better, and O(m + n) doesn't meet the O(log(m·n)) requirement.

---

## Approach 3 — Flattened binary search (optimal) ⭐

### Intuition
Because the flattened matrix is one sorted array of length `m·n`, run a single binary search over indices `0 .. m·n - 1`, converting each midpoint index into `(row, col)` on the fly with `row = mid / n`, `col = mid % n`.

### Algorithm
1. `lo = 0`, `hi = m * n - 1`.
2. While `lo <= hi`:
   - `mid = lo + (hi - lo) / 2`.
   - `val = matrix[mid / n][mid % n]`.
   - If `val == target` → return `true`.
   - Else if `val < target` → `lo = mid + 1`.
   - Else → `hi = mid - 1`.
3. Return `false`.

### Dry run on `matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]`, `target = 16`
```
m = 3, n = 4  → flat length = 12, indices 0..11
lo=0, hi=11
  mid = 0 + (11-0)/2 = 5
    row = 5/4 = 1, col = 5%4 = 1 → matrix[1][1] = 11 < 16 → lo = 6
lo=6, hi=11
  mid = 6 + (11-6)/2 = 8
    row = 8/4 = 2, col = 8%4 = 0 → matrix[2][0] = 23 > 16 → hi = 7
lo=6, hi=7
  mid = 6 + (7-6)/2 = 6
    row = 6/4 = 1, col = 6%4 = 2 → matrix[1][2] = 16 == 16 → return true ✅
```

### Code

```cpp
class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int m = matrix.size(), n = matrix[0].size();
        int lo = 0, hi = m * n - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            int val = matrix[mid / n][mid % n];
            if (val == target) return true;
            else if (val < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return false;
    }
};
```
```java
class Solution {
    public boolean searchMatrix(int[][] matrix, int target) {
        int m = matrix.length, n = matrix[0].length;
        int lo = 0, hi = m * n - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            int val = matrix[mid / n][mid % n];
            if (val == target) return true;
            else if (val < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return false;
    }
}
```
```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        lo, hi = 0, m * n - 1
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            val = matrix[mid // n][mid % n]
            if val == target:
                return True
            elif val < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return False
```

### Complexity
- **Time**: O(log(m·n)) — a single binary search over the flattened length.
- **Space**: O(1).

### Verdict
**The optimal answer** and the one the problem asks for. The index→coordinate mapping (`/n`, `%n`) is the only new idea; everything else is the LC 704 template.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Uses both properties | When to mention |
|----------|------|-------|----------------------|-----------------|
| Brute force | O(m·n) | O(1) | no | baseline only |
| Staircase (top-right) | O(m + n) | O(1) | only row/col sorting | great for LC 240; works here too |
| Flattened binary search | **O(log(m·n))** | O(1) | yes (the chaining property) | the required optimal answer ⭐ |

The key distinction to articulate: the **second property** (each row's first > previous row's last) is what makes full flattening valid. If you only had row-sorted and column-sorted (LC 240), you could *not* flatten, and the staircase O(m + n) would be the best general approach.

---

## 🧪 Edge cases & pitfalls
- **Single cell** (`1 x 1`) → `lo == hi == 0`; one comparison. Works.
- **Single row or single column** → `n = 1` makes `mid % n = 0` and `mid / n = mid`; the math still holds.
- **Pitfall — using `n` vs `m` in the mapping**: the divisor must be the **number of columns** `n` (row = idx / n, col = idx % n). Swapping `m` and `n` is the most common bug here.
- **Overflow**: `m * n <= 10^4` here so `int` is safe, but in general `m * n` could overflow — keep it in mind for larger-constraint variants.
- **Pitfall — confusing this with LC 240**: don't flatten when only rows *and* columns are independently sorted; that array isn't globally sorted.

---

## 🔗 Related problems
- **Binary Search** (LC 704) — the 1D engine this problem reduces to.
- **Search a 2D Matrix II** (LC 240) — weaker guarantee; use the staircase search.
- **Kth Smallest Element in a Sorted Matrix** (LC 378) — binary search on the *value* range.
- **Find Peak Element II** (LC 1901) — 2D binary search on a different property.

---

**→ Next:** [`03-Koko-Eating-Bananas.md`](./03-Koko-Eating-Bananas.md) | **→ Prev:** [`01-Binary-Search.md`](./01-Binary-Search.md) | [Problem set index](./00-Index.md)
