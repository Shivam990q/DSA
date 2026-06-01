# Longest Common Subsequence

**Platform**: LeetCode 1143 · **Difficulty**: Medium · **Topics**: String, Dynamic Programming · **Pattern**: Two-sequence DP (prefix vs prefix)

---

## 📜 Problem Statement

Given two strings `text1` and `text2`, return the **length of their longest common subsequence**. If there is no common subsequence, return `0`.

A **subsequence** of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.
- For example, `"ace"` is a subsequence of `"abcde"`.

A **common subsequence** of two strings is a subsequence that is common to both strings.

### Examples

**Example 1:**
```
Input:  text1 = "abcde", text2 = "ace"
Output: 3
Explanation: The longest common subsequence is "ace" and its length is 3.
```

**Example 2:**
```
Input:  text1 = "abc", text2 = "abc"
Output: 3
Explanation: The longest common subsequence is "abc" and its length is 3.
```

**Example 3:**
```
Input:  text1 = "abc", text2 = "def"
Output: 0
Explanation: There is no such common subsequence, so the result is 0.
```

### Constraints
```
1 <= text1.length, text2.length <= 1000
text1 and text2 consist of only lowercase English characters.
```

---

## 🧠 Understanding the problem

Compare the two strings prefix by prefix. Look at the last characters of the prefixes `a[0..i)` and `b[0..j)`:

- If `a[i-1] == b[j-1]`, that shared character can end a common subsequence: `LCS = 1 + LCS(a[0..i-1), b[0..j-1))`.
- If they differ, the last character of one of them isn't in the LCS, so `LCS = max(LCS(a[0..i-1), b[0..j)), LCS(a[0..i), b[0..j-1)))`.

This is the archetypal **two-sequence DP**. Almost every string-pair DP (edit distance, distinct subsequences, shortest common supersequence) is a variation of this transition.

5-step framework:
1. **State**: `dp[i][j]` = LCS length of `a[0..i)` and `b[0..j)`.
2. **Transition**: match → `dp[i-1][j-1] + 1`; mismatch → `max(dp[i-1][j], dp[i][j-1])`.
3. **Base case**: `dp[0][*] = dp[*][0] = 0` (empty prefix shares nothing).
4. **Order**: increasing `i`, then `j`.
5. **Answer**: `dp[m][n]`; each row needs only the previous row → O(n) space.

---

## Approach 1 — Top-down memoization

### Intuition
`solve(i, j)` = LCS of the suffixes starting at `i` and `j`. Match advances both; mismatch tries skipping one side or the other.

### Algorithm
1. If `i == m` or `j == n`, return 0.
2. If `a[i] == b[j]`, return `1 + solve(i+1, j+1)`.
3. Else return `max(solve(i+1, j), solve(i, j+1))`.
4. Memoize on `(i, j)`.

### Dry run on `a = "ace", b = "abcde"` (conceptually)
```
match 'a' -> 1 + LCS("ce","bcde")
'c' vs 'b' mismatch -> skip 'b' -> match 'c' -> 1 + LCS("e","de")
'e' vs 'd' mismatch -> skip 'd' -> match 'e' -> 1
total = 3
```

### Code
```cpp
class Solution {
    vector<vector<int>> memo;
    string a, b;
    int solve(int i, int j) {
        if (i == (int)a.size() || j == (int)b.size()) return 0;
        if (memo[i][j] != -1) return memo[i][j];
        if (a[i] == b[j]) return memo[i][j] = 1 + solve(i + 1, j + 1);
        return memo[i][j] = max(solve(i + 1, j), solve(i, j + 1));
    }
public:
    int longestCommonSubsequence(string text1, string text2) {
        a = text1; b = text2;
        memo.assign(a.size(), vector<int>(b.size(), -1));
        return solve(0, 0);
    }
};
```
```java
class Solution {
    private int[][] memo;
    private String a, b;
    private int solve(int i, int j) {
        if (i == a.length() || j == b.length()) return 0;
        if (memo[i][j] != -1) return memo[i][j];
        if (a.charAt(i) == b.charAt(j)) return memo[i][j] = 1 + solve(i + 1, j + 1);
        return memo[i][j] = Math.max(solve(i + 1, j), solve(i, j + 1));
    }
    public int longestCommonSubsequence(String text1, String text2) {
        a = text1; b = text2;
        memo = new int[a.length()][b.length()];
        for (int[] row : memo) java.util.Arrays.fill(row, -1);
        return solve(0, 0);
    }
}
```
```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        from functools import lru_cache
        m, n = len(text1), len(text2)

        @lru_cache(maxsize=None)
        def solve(i: int, j: int) -> int:
            if i == m or j == n:
                return 0
            if text1[i] == text2[j]:
                return 1 + solve(i + 1, j + 1)
            return max(solve(i + 1, j), solve(i, j + 1))

        return solve(0, 0)
```

### Complexity
- **Time**: O(m × n).
- **Space**: O(m × n) memo + recursion.

### Verdict
Reads like the recurrence. Bottom-up next.

---

## Approach 2 — Bottom-up 2D table

### Intuition
Build the `(m+1) × (n+1)` table; row/column 0 are zeros. Fill by the match/mismatch rule.

### Algorithm
1. `dp[0][*] = dp[*][0] = 0`.
2. For `i` 1..m, `j` 1..n: match → `dp[i-1][j-1]+1`; else `max(dp[i-1][j], dp[i][j-1])`.
3. Return `dp[m][n]`.

### Dry run on `a = "abc", b = "abc"`
```
diagonal matches all -> dp[3][3] = 3
```

### Code
```cpp
class Solution {
public:
    int longestCommonSubsequence(string a, string b) {
        int m = a.size(), n = b.size();
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        for (int i = 1; i <= m; i++)
            for (int j = 1; j <= n; j++)
                dp[i][j] = (a[i - 1] == b[j - 1]) ? dp[i - 1][j - 1] + 1
                                                  : max(dp[i - 1][j], dp[i][j - 1]);
        return dp[m][n];
    }
};
```
```java
class Solution {
    public int longestCommonSubsequence(String a, String b) {
        int m = a.length(), n = b.length();
        int[][] dp = new int[m + 1][n + 1];
        for (int i = 1; i <= m; i++)
            for (int j = 1; j <= n; j++)
                dp[i][j] = (a.charAt(i - 1) == b.charAt(j - 1))
                        ? dp[i - 1][j - 1] + 1
                        : Math.max(dp[i - 1][j], dp[i][j - 1]);
        return dp[m][n];
    }
}
```
```python
class Solution:
    def longestCommonSubsequence(self, a: str, b: str) -> int:
        m, n = len(a), len(b)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if a[i - 1] == b[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]
```

### Complexity
- **Time**: O(m × n).
- **Space**: O(m × n).

### Verdict
The canonical answer. Row `i` reads only row `i-1`, so we can roll.

---

## Approach 3 — Two rolling rows (space optimized) ⭐

### Intuition
Keep `prev` (row `i-1`) and `cur` (row `i`). The diagonal term `dp[i-1][j-1]` is `prev[j-1]`; the top is `prev[j]`; the left is `cur[j-1]`. Swap after each row.

### Algorithm
1. `prev = [0]*(n+1)`.
2. For each `i`, build `cur`: match → `prev[j-1]+1`; else `max(prev[j], cur[j-1])`. Then `prev = cur`.
3. Return `prev[n]`.

### Dry run on `a = "ace", b = "abcde"`
```
prev starts all zeros.
Processing 'a': cur[*] becomes 1 from column of 'a' onward.
... after 'e': prev[n] = 3
```

### Code
```cpp
class Solution {
public:
    int longestCommonSubsequence(string a, string b) {
        int m = a.size(), n = b.size();
        vector<int> prev(n + 1, 0), cur(n + 1, 0);
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++)
                cur[j] = (a[i - 1] == b[j - 1]) ? prev[j - 1] + 1
                                                : max(prev[j], cur[j - 1]);
            swap(prev, cur);
        }
        return prev[n];
    }
};
```
```java
class Solution {
    public int longestCommonSubsequence(String a, String b) {
        int m = a.length(), n = b.length();
        int[] prev = new int[n + 1], cur = new int[n + 1];
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++)
                cur[j] = (a.charAt(i - 1) == b.charAt(j - 1))
                        ? prev[j - 1] + 1
                        : Math.max(prev[j], cur[j - 1]);
            int[] tmp = prev; prev = cur; cur = tmp;
        }
        return prev[n];
    }
}
```
```python
class Solution:
    def longestCommonSubsequence(self, a: str, b: str) -> int:
        m, n = len(a), len(b)
        prev = [0] * (n + 1)
        for i in range(1, m + 1):
            cur = [0] * (n + 1)
            for j in range(1, n + 1):
                if a[i - 1] == b[j - 1]:
                    cur[j] = prev[j - 1] + 1
                else:
                    cur[j] = max(prev[j], cur[j - 1])
            prev = cur
        return prev[n]
```

### Complexity
- **Time**: O(m × n).
- **Space**: O(n) — two rows (or one with care).

### Verdict
**The space-optimal answer.** Caveat: with only two rows you can return the *length* but not easily reconstruct the actual subsequence — that needs the full table for backtracking.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Memoization | O(mn) | O(mn) | top-down recurrence |
| 2D table | O(mn) | O(mn) | canonical; allows reconstruction |
| Two rolling rows | O(mn) | **O(n)** | length only ⭐ |

---

## 🧪 Edge cases & pitfalls
- **No common characters** (`"abc"`, `"def"`) → 0. The table stays all zeros.
- **Identical strings** → length `m`.
- **One string a subsequence of the other** → the shorter length.
- **Pitfall — subsequence vs substring**: LCS does NOT need contiguity. The "skip one side" branch is exactly what allows gaps.
- **Pitfall — reconstruction with rolling rows**: if you must output the subsequence, keep the full 2D table and walk back from `dp[m][n]` (diagonal on a match, toward the larger of top/left on a mismatch).

---

## 🔗 Related problems
- **Edit Distance** (LC 72) — same two-sequence grid, minimizing operations.
- **Shortest Common Supersequence** (LC 1092) — built directly from the LCS.
- **Longest Common Substring** — contiguous variant (reset to 0 on mismatch).
- **Delete Operation for Two Strings** (LC 583) — `m + n - 2·LCS`.
- **Distinct Subsequences** (LC 115) — count, not length, of a target subsequence.

---

**→ Next:** [`03-Edit-Distance.md`](./03-Edit-Distance.md) | **→ Prev:** [`01-Unique-Paths.md`](./01-Unique-Paths.md) | Back to [`00-Index.md`](./00-Index.md)
