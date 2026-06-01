# Unique Paths

**Platform**: LeetCode 62 · **Difficulty**: Medium · **Topics**: Math, Dynamic Programming, Combinatorics · **Pattern**: Grid path counting

---

## 📜 Problem Statement

There is a robot on an `m x n` grid. The robot is initially located at the **top-left** corner (i.e., `grid[0][0]`). The robot tries to move to the **bottom-right** corner (i.e., `grid[m-1][n-1]`). The robot can only move either **down** or **right** at any point in time.

Given the two integers `m` and `n`, return the **number of possible unique paths** that the robot can take to reach the bottom-right corner.

The test cases are generated so that the answer will be **less than or equal to** `2 * 10^9`.

### Examples

**Example 1:**
```
Input:  m = 3, n = 7
Output: 28
```

**Example 2:**
```
Input:  m = 3, n = 2
Output: 3
Explanation: From the top-left corner, there are a total of 3 ways to reach the bottom-right corner:
1. Right -> Down -> Down
2. Down -> Down -> Right
3. Down -> Right -> Down
```

**Example 3:**
```
Input:  m = 1, n = 1
Output: 1
Explanation: Already at the destination; one trivial path.
```

### Constraints
```
1 <= m, n <= 100
```

---

## 🧠 Understanding the problem

To arrive at cell `(i, j)`, the robot's last move was either **from above** `(i-1, j)` or **from the left** `(i, j-1)` — those are the only two legal moves. The paths through those two predecessors are disjoint, so the count adds:

> `paths(i, j) = paths(i-1, j) + paths(i, j-1)`.

Cells in the first row or first column have exactly one path (keep going right, or keep going down).

5-step framework:
1. **State**: `dp[i][j]` = number of unique paths from `(0,0)` to `(i,j)`.
2. **Transition**: `dp[i][j] = dp[i-1][j] + dp[i][j-1]`.
3. **Base case**: `dp[0][j] = dp[i][0] = 1`.
4. **Order**: row by row, left to right.
5. **Answer**: `dp[m-1][n-1]`; each row needs only the row above → O(n) space. (And there's a closed-form combinatorial answer.)

---

## Approach 1 — Top-down memoization

### Intuition
Recurse from the destination back to the start, summing the two predecessors, caching each cell.

### Algorithm
1. `paths(0, 0) = 1`. Out-of-bounds → 0.
2. `paths(i, j) = paths(i-1, j) + paths(i, j-1)`.
3. Memoize on `(i, j)`.

### Dry run on `m = 3, n = 2`
```
paths(2,1) = paths(1,1) + paths(2,0)
paths(1,1) = paths(0,1) + paths(1,0) = 1 + 1 = 2
paths(2,0) = 1
=> paths(2,1) = 2 + 1 = 3
```

### Code
```cpp
class Solution {
    vector<vector<int>> memo;
    int solve(int i, int j) {
        if (i == 0 && j == 0) return 1;
        if (i < 0 || j < 0) return 0;
        if (memo[i][j] != -1) return memo[i][j];
        return memo[i][j] = solve(i - 1, j) + solve(i, j - 1);
    }
public:
    int uniquePaths(int m, int n) {
        memo.assign(m, vector<int>(n, -1));
        return solve(m - 1, n - 1);
    }
};
```
```java
class Solution {
    private int[][] memo;
    private int solve(int i, int j) {
        if (i == 0 && j == 0) return 1;
        if (i < 0 || j < 0) return 0;
        if (memo[i][j] != -1) return memo[i][j];
        return memo[i][j] = solve(i - 1, j) + solve(i, j - 1);
    }
    public int uniquePaths(int m, int n) {
        memo = new int[m][n];
        for (int[] row : memo) java.util.Arrays.fill(row, -1);
        return solve(m - 1, n - 1);
    }
}
```
```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def solve(i: int, j: int) -> int:
            if i == 0 and j == 0:
                return 1
            if i < 0 or j < 0:
                return 0
            return solve(i - 1, j) + solve(i, j - 1)

        return solve(m - 1, n - 1)
```

### Complexity
- **Time**: O(m × n).
- **Space**: O(m × n) memo + recursion depth.

### Verdict
Clear recurrence. Flip it bottom-up next.

---

## Approach 2 — Bottom-up 2D table

### Intuition
Fill the grid from the top-left. The first row/column are all 1s; every other cell sums its top and left neighbors.

### Algorithm
1. `dp[0][j] = 1`, `dp[i][0] = 1`.
2. For each interior cell: `dp[i][j] = dp[i-1][j] + dp[i][j-1]`.
3. Return `dp[m-1][n-1]`.

### Dry run on `m = 3, n = 7` (first rows)
```
row0: 1 1 1 1 1 1 1
row1: 1 2 3 4 5 6 7
row2: 1 3 6 10 15 21 28
answer = 28
```

### Code
```cpp
class Solution {
public:
    int uniquePaths(int m, int n) {
        vector<vector<int>> dp(m, vector<int>(n, 1));
        for (int i = 1; i < m; i++)
            for (int j = 1; j < n; j++)
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
        return dp[m - 1][n - 1];
    }
};
```
```java
class Solution {
    public int uniquePaths(int m, int n) {
        int[][] dp = new int[m][n];
        for (int[] row : dp) java.util.Arrays.fill(row, 1);
        for (int i = 1; i < m; i++)
            for (int j = 1; j < n; j++)
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
        return dp[m - 1][n - 1];
    }
}
```
```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [[1] * n for _ in range(m)]
        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
        return dp[m - 1][n - 1]
```

### Complexity
- **Time**: O(m × n).
- **Space**: O(m × n).

### Verdict
Standard 2D DP. But row `i` only ever reads row `i-1`, so we can shrink to one row.

---

## Approach 3 — 1D rolling row (space optimized) ⭐

### Intuition
Keep a single array `dp` of length `n` representing the current row. When you process cell `j`, `dp[j]` still holds the value from the row above (the "top" neighbor) and `dp[j-1]` already holds the new left neighbor. So `dp[j] += dp[j-1]` does both at once.

### Algorithm
1. `dp = [1] * n` (first row).
2. For each subsequent row, for `j` from 1 to n-1: `dp[j] += dp[j-1]`.
3. Return `dp[n-1]`.

### Dry run on `m = 3, n = 2`
```
dp = [1,1]
row1: dp[1]+=dp[0] -> [1,2]
row2: dp[1]+=dp[0] -> [1,3]
answer = 3
```

### Code
```cpp
class Solution {
public:
    int uniquePaths(int m, int n) {
        vector<int> dp(n, 1);
        for (int i = 1; i < m; i++)
            for (int j = 1; j < n; j++)
                dp[j] += dp[j - 1];
        return dp[n - 1];
    }
};
```
```java
class Solution {
    public int uniquePaths(int m, int n) {
        int[] dp = new int[n];
        java.util.Arrays.fill(dp, 1);
        for (int i = 1; i < m; i++)
            for (int j = 1; j < n; j++)
                dp[j] += dp[j - 1];
        return dp[n - 1];
    }
}
```
```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [1] * n
        for _ in range(1, m):
            for j in range(1, n):
                dp[j] += dp[j - 1]
        return dp[-1]
```

### Complexity
- **Time**: O(m × n).
- **Space**: O(n).

### Verdict
**The optimal DP answer.** Linear extra space, same time.

---

## Approach 4 — Combinatorics (closed form)

### Intuition
Every path makes exactly `m-1` downs and `n-1` rights, in some order — a sequence of `(m-1)+(n-1)` moves where we choose which positions are "down." That's a binomial coefficient:

> `answer = C(m+n-2, m-1)`.

### Algorithm
Compute `C(m+n-2, m-1)` multiplicatively, dividing as we go to keep numbers small and exact.

### Dry run on `m = 3, n = 7`
```
C(3+7-2, 3-1) = C(8, 2) = 8*7/2 = 28
```

### Code
```cpp
class Solution {
public:
    int uniquePaths(int m, int n) {
        long long result = 1;
        int total = m + n - 2, pick = m - 1;
        for (int i = 1; i <= pick; i++) {
            result = result * (total - pick + i) / i;
        }
        return (int)result;
    }
};
```
```java
class Solution {
    public int uniquePaths(int m, int n) {
        long result = 1;
        int total = m + n - 2, pick = m - 1;
        for (int i = 1; i <= pick; i++) {
            result = result * (total - pick + i) / i;
        }
        return (int) result;
    }
}
```
```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        from math import comb
        return comb(m + n - 2, m - 1)
```

### Complexity
- **Time**: O(min(m, n)).
- **Space**: O(1).

### Verdict
The fastest possible — pure math. Worth mentioning, though the rolling DP generalizes better to obstacle/cost variants.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Memoization | O(mn) | O(mn) | top-down recurrence |
| 2D table | O(mn) | O(mn) | standard DP |
| 1D rolling | O(mn) | **O(n)** | the optimal DP ⭐ |
| Combinatorics | **O(min(m,n))** | **O(1)** | closed form, doesn't generalize to obstacles |

---

## 🧪 Edge cases & pitfalls
- **`m = 1` or `n = 1`** → exactly 1 path (a straight line). The first row/column init handles it.
- **Pitfall — multiplication order in combinatorics**: multiply *then* divide (`result * (...) / i`) so each intermediate stays an exact integer; dividing first truncates.
- **Pitfall — overflow**: the answer can approach 2×10⁹, near the 32-bit limit. Use 64-bit intermediates in C++/Java (Python is unbounded).
- **Obstacles variant** (LC 63): set blocked cells' `dp` to 0 — the rolling DP adapts directly; the combinatorial formula does not.

---

## 🔗 Related problems
- **Unique Paths II** (LC 63) — same grid with obstacles.
- **Minimum Path Sum** (LC 64) — minimize the summed cost instead of counting paths.
- **Unique Paths III** (LC 980) — must visit every empty square (backtracking).
- **Dungeon Game** (LC 174) — grid DP traversed in reverse with a min-health constraint.

---

**→ Next:** [`02-Longest-Common-Subsequence.md`](./02-Longest-Common-Subsequence.md) | Back to [`00-Index.md`](./00-Index.md)
