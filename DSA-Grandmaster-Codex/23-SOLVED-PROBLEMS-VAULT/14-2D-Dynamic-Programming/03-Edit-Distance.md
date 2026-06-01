# Edit Distance

**Platform**: LeetCode 72 · **Difficulty**: Medium · **Topics**: String, Dynamic Programming · **Pattern**: Two-sequence DP (Levenshtein distance)

---

## 📜 Problem Statement

Given two strings `word1` and `word2`, return the **minimum number of operations** required to convert `word1` to `word2`.

You have the following three operations permitted on a word:
- **Insert** a character
- **Delete** a character
- **Replace** a character

### Examples

**Example 1:**
```
Input:  word1 = "horse", word2 = "ros"
Output: 3
Explanation:
horse -> rorse (replace 'h' with 'r')
rorse -> rose  (remove 'r')
rose  -> ros   (remove 'e')
```

**Example 2:**
```
Input:  word1 = "intention", word2 = "execution"
Output: 5
Explanation:
intention -> inention (remove 't')
inention  -> enention (replace 'i' with 'e')
enention  -> exention (replace 'n' with 'x')
exention  -> exection (replace 'n' with 'c')
exection  -> execution (insert 'u')
```

**Example 3:**
```
Input:  word1 = "", word2 = "abc"
Output: 3
Explanation: Insert 'a', 'b', 'c'.
```

### Constraints
```
0 <= word1.length, word2.length <= 500
word1 and word2 consist of lowercase English letters.
```

---

## 🧠 Understanding the problem

This is the **Levenshtein distance**. Align the two strings prefix by prefix. Consider the last characters of `a[0..i)` and `b[0..j)`:

- If `a[i-1] == b[j-1]`, they already match: no cost, `dp[i][j] = dp[i-1][j-1]`.
- Otherwise we pay 1 for one of three moves:
  - **Replace** `a[i-1]` with `b[j-1]` → `1 + dp[i-1][j-1]`.
  - **Delete** `a[i-1]` → `1 + dp[i-1][j]`.
  - **Insert** `b[j-1]` → `1 + dp[i][j-1]`.

Take the cheapest. The base cases are pure insertions/deletions against an empty prefix.

5-step framework:
1. **State**: `dp[i][j]` = min edits to turn `a[0..i)` into `b[0..j)`.
2. **Transition**: match → `dp[i-1][j-1]`; else `1 + min(replace dp[i-1][j-1], delete dp[i-1][j], insert dp[i][j-1])`.
3. **Base case**: `dp[i][0] = i` (delete all), `dp[0][j] = j` (insert all).
4. **Order**: increasing `i`, then `j`.
5. **Answer**: `dp[m][n]`; collapses to O(n) with rolling rows.

---

## Approach 1 — Top-down memoization

### Intuition
`solve(i, j)` = edits to convert the first `i` chars of `a` into the first `j` of `b`. Recurse on the three operations when characters differ.

### Algorithm
1. If `i == 0`, return `j` (insert remaining). If `j == 0`, return `i` (delete remaining).
2. Match → `solve(i-1, j-1)`.
3. Else `1 + min(solve(i-1,j-1), solve(i-1,j), solve(i,j-1))`.
4. Memoize on `(i, j)`.

### Dry run on `a = "horse", b = "ros"`
```
'e' vs 's' differ -> 1 + min(replace solve(4,2), delete solve(4,3), insert solve(5,2))
... resolves to 3 (replace h->r, delete r, delete e)
```

### Code
```cpp
class Solution {
    vector<vector<int>> memo;
    string a, b;
    int solve(int i, int j) {
        if (i == 0) return j;
        if (j == 0) return i;
        if (memo[i][j] != -1) return memo[i][j];
        if (a[i - 1] == b[j - 1]) return memo[i][j] = solve(i - 1, j - 1);
        return memo[i][j] = 1 + min({ solve(i - 1, j - 1),
                                      solve(i - 1, j),
                                      solve(i, j - 1) });
    }
public:
    int minDistance(string word1, string word2) {
        a = word1; b = word2;
        memo.assign(a.size() + 1, vector<int>(b.size() + 1, -1));
        return solve(a.size(), b.size());
    }
};
```
```java
class Solution {
    private int[][] memo;
    private String a, b;
    private int solve(int i, int j) {
        if (i == 0) return j;
        if (j == 0) return i;
        if (memo[i][j] != -1) return memo[i][j];
        if (a.charAt(i - 1) == b.charAt(j - 1)) return memo[i][j] = solve(i - 1, j - 1);
        return memo[i][j] = 1 + Math.min(solve(i - 1, j - 1),
                                Math.min(solve(i - 1, j), solve(i, j - 1)));
    }
    public int minDistance(String word1, String word2) {
        a = word1; b = word2;
        memo = new int[a.length() + 1][b.length() + 1];
        for (int[] row : memo) java.util.Arrays.fill(row, -1);
        return solve(a.length(), b.length());
    }
}
```
```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def solve(i: int, j: int) -> int:
            if i == 0:
                return j
            if j == 0:
                return i
            if word1[i - 1] == word2[j - 1]:
                return solve(i - 1, j - 1)
            return 1 + min(solve(i - 1, j - 1),
                           solve(i - 1, j),
                           solve(i, j - 1))

        return solve(len(word1), len(word2))
```

### Complexity
- **Time**: O(m × n).
- **Space**: O(m × n).

### Verdict
Mirrors the three operations cleanly. Now go bottom-up.

---

## Approach 2 — Bottom-up 2D table

### Intuition
Fill the table with the first row/column seeded by pure insert/delete counts, then apply the match/min rule.

### Algorithm
1. `dp[i][0] = i`, `dp[0][j] = j`.
2. For `i` 1..m, `j` 1..n: match → `dp[i-1][j-1]`; else `1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`.
3. Return `dp[m][n]`.

### Dry run on `a = "ros", b = "horse"`-style (small slice)
```
dp[0][*] = 0..n  ; dp[*][0] = 0..m
fill diagonally; equal chars copy the diagonal, else 1 + min of 3 neighbors
```

### Code
```cpp
class Solution {
public:
    int minDistance(string a, string b) {
        int m = a.size(), n = b.size();
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        for (int i = 0; i <= m; i++) dp[i][0] = i;
        for (int j = 0; j <= n; j++) dp[0][j] = j;
        for (int i = 1; i <= m; i++)
            for (int j = 1; j <= n; j++)
                dp[i][j] = (a[i - 1] == b[j - 1]) ? dp[i - 1][j - 1]
                          : 1 + min({ dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1] });
        return dp[m][n];
    }
};
```
```java
class Solution {
    public int minDistance(String a, String b) {
        int m = a.length(), n = b.length();
        int[][] dp = new int[m + 1][n + 1];
        for (int i = 0; i <= m; i++) dp[i][0] = i;
        for (int j = 0; j <= n; j++) dp[0][j] = j;
        for (int i = 1; i <= m; i++)
            for (int j = 1; j <= n; j++)
                dp[i][j] = (a.charAt(i - 1) == b.charAt(j - 1))
                        ? dp[i - 1][j - 1]
                        : 1 + Math.min(dp[i - 1][j - 1],
                              Math.min(dp[i - 1][j], dp[i][j - 1]));
        return dp[m][n];
    }
}
```
```python
class Solution:
    def minDistance(self, a: str, b: str) -> int:
        m, n = len(a), len(b)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if a[i - 1] == b[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
        return dp[m][n]
```

### Complexity
- **Time**: O(m × n).
- **Space**: O(m × n).

### Verdict
The canonical answer. Rolls to O(n) since each cell uses only the previous row and the current row's left neighbor.

---

## Approach 3 — Two rolling rows (space optimized) ⭐

### Intuition
`dp[i][j]` needs `dp[i-1][j]` (top), `dp[i][j-1]` (left), `dp[i-1][j-1]` (diagonal). Keep `prev` (row above) and build `cur`. Seed `cur[0] = i` each row (deleting `i` chars to match empty prefix).

### Algorithm
1. `prev[j] = j`.
2. For each `i`: `cur[0] = i`; fill `cur[j]` from `prev` and `cur[j-1]`; then `prev = cur`.
3. Return `prev[n]`.

### Dry run on `a = "horse", b = "ros"`
```
prev = [0,1,2,3]
i=1 ('h'): cur[0]=1; compute -> ...
... after all rows: prev[3] = 3
```

### Code
```cpp
class Solution {
public:
    int minDistance(string a, string b) {
        int m = a.size(), n = b.size();
        vector<int> prev(n + 1), cur(n + 1);
        for (int j = 0; j <= n; j++) prev[j] = j;
        for (int i = 1; i <= m; i++) {
            cur[0] = i;
            for (int j = 1; j <= n; j++)
                cur[j] = (a[i - 1] == b[j - 1]) ? prev[j - 1]
                        : 1 + min({ prev[j], cur[j - 1], prev[j - 1] });
            swap(prev, cur);
        }
        return prev[n];
    }
};
```
```java
class Solution {
    public int minDistance(String a, String b) {
        int m = a.length(), n = b.length();
        int[] prev = new int[n + 1], cur = new int[n + 1];
        for (int j = 0; j <= n; j++) prev[j] = j;
        for (int i = 1; i <= m; i++) {
            cur[0] = i;
            for (int j = 1; j <= n; j++)
                cur[j] = (a.charAt(i - 1) == b.charAt(j - 1))
                        ? prev[j - 1]
                        : 1 + Math.min(prev[j - 1], Math.min(prev[j], cur[j - 1]));
            int[] tmp = prev; prev = cur; cur = tmp;
        }
        return prev[n];
    }
}
```
```python
class Solution:
    def minDistance(self, a: str, b: str) -> int:
        m, n = len(a), len(b)
        prev = list(range(n + 1))
        for i in range(1, m + 1):
            cur = [i] + [0] * n
            for j in range(1, n + 1):
                if a[i - 1] == b[j - 1]:
                    cur[j] = prev[j - 1]
                else:
                    cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])
            prev = cur
        return prev[n]
```

### Complexity
- **Time**: O(m × n).
- **Space**: O(n).

### Verdict
**The space-optimal answer.** Same time, two rows.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Memoization | O(mn) | O(mn) | three-operation recurrence |
| 2D table | O(mn) | O(mn) | canonical, supports reconstruction |
| Two rolling rows | O(mn) | **O(n)** | the space optimum ⭐ |

---

## 🧪 Edge cases & pitfalls
- **One empty string** → the other's length (all inserts or all deletes). The base row/column encode this.
- **Identical strings** → 0.
- **Pitfall — which neighbor is which op**: top `dp[i-1][j]` = delete from `a`; left `dp[i][j-1]` = insert into `a`; diagonal `dp[i-1][j-1]` = replace (or free on match). Mixing these up still often gives the right number by symmetry, but reconstruction breaks.
- **Pitfall — forgetting to seed `cur[0] = i`** in the rolling version: without it, the "delete all of `a`'s prefix" base case is lost.

---

## 🔗 Related problems
- **Longest Common Subsequence** (LC 1143) — the sibling two-sequence DP.
- **Delete Operation for Two Strings** (LC 583) — only insert/delete (no replace).
- **One Edit Distance** (LC 161) — decide if distance is exactly 1 (O(n) scan).
- **Minimum ASCII Delete Sum** (LC 712) — weighted deletions.
- **Regular Expression Matching** (LC 10) / **Wildcard Matching** (LC 44) — pattern-matching grids.

---

**→ Next:** [`04-Coin-Change-II.md`](./04-Coin-Change-II.md) | **→ Prev:** [`02-Longest-Common-Subsequence.md`](./02-Longest-Common-Subsequence.md) | Back to [`00-Index.md`](./00-Index.md)
