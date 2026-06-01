# Interleaving String

**Platform**: LeetCode 97 · **Difficulty**: Medium · **Topics**: String, Dynamic Programming · **Pattern**: Two-sequence DP (merge reachability)

---

## 📜 Problem Statement

Given strings `s1`, `s2`, and `s3`, find whether `s3` is formed by an **interleaving** of `s1` and `s2`.

An **interleaving** of two strings `s` and `t` is a configuration where `s` and `t` are divided into `n` and `m` substrings respectively, such that:
- `s = s1 + s2 + ... + sn`
- `t = t1 + t2 + ... + tm`
- `|n - m| <= 1`
- The interleaving is `s1 + t1 + s2 + t2 + ...` or `t1 + s1 + t2 + s2 + ...`

**Note:** `a + b` is the concatenation of strings `a` and `b`. Crucially, the relative order of characters from each source string must be preserved.

### Examples

**Example 1:**
```
Input:  s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"
Output: true
Explanation: One way to obtain s3 is:
Split s1 into "aa" + "bc" + "c", and s2 into "dbbc" + "a".
Interleaving the two splits: "aa" + "dbbc" + "bc" + "a" + "c" = "aadbbcbcac".
```

**Example 2:**
```
Input:  s1 = "aabcc", s2 = "dbbca", s3 = "aadbbbaccc"
Output: false
Explanation: It is impossible for s3 = "aadbbbaccc" to be an interleaving of s1 and s2.
```

**Example 3:**
```
Input:  s1 = "", s2 = "", s3 = ""
Output: true
```

### Constraints
```
0 <= s1.length, s2.length <= 100
0 <= s3.length <= 200
s1, s2, and s3 consist of lowercase English letters.
```

---

## 🧠 Understanding the problem

We weave `s1` and `s2` together — preserving each one's internal order — and ask if the result can equal `s3`. A greedy "take whichever matches" fails because sometimes both `s1` and `s2` offer the same next character and only one choice leads to success; you'd need to try both.

The DP captures *all* choices. Track how many characters we've consumed from each source: if we've used `i` from `s1` and `j` from `s2`, we must have produced exactly the first `i + j` characters of `s3`. The next character of `s3` (`s3[i+j]`) is contributed by either `s1[i]` (if it matches) or `s2[j]` (if it matches).

**Length check first**: if `|s1| + |s2| != |s3|`, it's immediately false.

5-step framework:
1. **State**: `dp[i][j]` = can `s1[0..i)` and `s2[0..j)` interleave to form `s3[0..i+j)`.
2. **Transition**: `dp[i][j] = (s1[i-1]==s3[i+j-1] && dp[i-1][j]) || (s2[j-1]==s3[i+j-1] && dp[i][j-1])`.
3. **Base case**: `dp[0][0] = true`.
4. **Order**: increasing `i`, `j`.
5. **Answer**: `dp[m][n]`; row `i` depends only on rows `i` and `i-1` → O(n) space.

---

## Approach 1 — Top-down memoization

### Intuition
`solve(i, j)` = can the suffixes `s1[i:]` and `s2[j:]` interleave into `s3[i+j:]`. Try consuming the next char from `s1` or from `s2` when it matches `s3[i+j]`.

### Algorithm
1. If `i+j == |s3|`, return true (all consumed).
2. Take from `s1` if `s1[i] == s3[i+j]` and `solve(i+1, j)`.
3. Take from `s2` if `s2[j] == s3[i+j]` and `solve(i, j+1)`.
4. Memoize on `(i, j)`.

### Dry run on `s1="ab", s2="cd", s3="acbd"`
```
solve(0,0): s3[0]='a' matches s1[0] -> solve(1,0)
solve(1,0): s3[1]='c' matches s2[0] -> solve(1,1)
solve(1,1): s3[2]='b' matches s1[1] -> solve(2,1)
solve(2,1): s3[3]='d' matches s2[1] -> solve(2,2) -> end -> true
```

### Code
```cpp
class Solution {
    vector<vector<int>> memo;     // -1 unknown, 0 false, 1 true
    string s1, s2, s3;
    bool solve(int i, int j) {
        if (i + j == (int)s3.size()) return true;
        if (memo[i][j] != -1) return memo[i][j];
        bool ok = false;
        if (i < (int)s1.size() && s1[i] == s3[i + j]) ok = solve(i + 1, j);
        if (!ok && j < (int)s2.size() && s2[j] == s3[i + j]) ok = solve(i, j + 1);
        return memo[i][j] = ok;
    }
public:
    bool isInterleave(string s1, string s2, string s3) {
        if (s1.size() + s2.size() != s3.size()) return false;
        this->s1 = s1; this->s2 = s2; this->s3 = s3;
        memo.assign(s1.size() + 1, vector<int>(s2.size() + 1, -1));
        return solve(0, 0);
    }
};
```
```java
class Solution {
    private int[][] memo;
    private String s1, s2, s3;
    private boolean solve(int i, int j) {
        if (i + j == s3.length()) return true;
        if (memo[i][j] != -1) return memo[i][j] == 1;
        boolean ok = false;
        if (i < s1.length() && s1.charAt(i) == s3.charAt(i + j)) ok = solve(i + 1, j);
        if (!ok && j < s2.length() && s2.charAt(j) == s3.charAt(i + j)) ok = solve(i, j + 1);
        memo[i][j] = ok ? 1 : 0;
        return ok;
    }
    public boolean isInterleave(String s1, String s2, String s3) {
        if (s1.length() + s2.length() != s3.length()) return false;
        this.s1 = s1; this.s2 = s2; this.s3 = s3;
        memo = new int[s1.length() + 1][s2.length() + 1];
        for (int[] row : memo) java.util.Arrays.fill(row, -1);
        return solve(0, 0);
    }
}
```
```python
class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        if len(s1) + len(s2) != len(s3):
            return False
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def solve(i: int, j: int) -> bool:
            if i + j == len(s3):
                return True
            if i < len(s1) and s1[i] == s3[i + j] and solve(i + 1, j):
                return True
            if j < len(s2) and s2[j] == s3[i + j] and solve(i, j + 1):
                return True
            return False

        return solve(0, 0)
```

### Complexity
- **Time**: O(m × n).
- **Space**: O(m × n).

### Verdict
Clean two-choice recursion. Bottom-up next.

---

## Approach 2 — Bottom-up 2D table

### Intuition
`dp[i][j]` = reachable using `i` chars of `s1` and `j` of `s2`. Extend a reachable state by matching `s3[i+j-1]` with the next char from either source.

### Algorithm
1. `dp[0][0] = true`. Length check.
2. For all `(i, j)`: set `dp[i][j]` true if (came from top and `s1[i-1]` matches) or (came from left and `s2[j-1]` matches).
3. Return `dp[m][n]`.

### Dry run on Example 1 (boundary)
```
dp[0][j]: true while s2's prefix matches s3's prefix
dp[i][0]: true while s1's prefix matches s3's prefix
interior filled by OR of two matching extensions -> dp[m][n] = true
```

### Code
```cpp
class Solution {
public:
    bool isInterleave(string s1, string s2, string s3) {
        int m = s1.size(), n = s2.size();
        if (m + n != (int)s3.size()) return false;
        vector<vector<bool>> dp(m + 1, vector<bool>(n + 1, false));
        dp[0][0] = true;
        for (int i = 0; i <= m; i++)
            for (int j = 0; j <= n; j++) {
                if (i > 0 && s1[i - 1] == s3[i + j - 1])
                    dp[i][j] = dp[i][j] || dp[i - 1][j];
                if (j > 0 && s2[j - 1] == s3[i + j - 1])
                    dp[i][j] = dp[i][j] || dp[i][j - 1];
            }
        return dp[m][n];
    }
};
```
```java
class Solution {
    public boolean isInterleave(String s1, String s2, String s3) {
        int m = s1.length(), n = s2.length();
        if (m + n != s3.length()) return false;
        boolean[][] dp = new boolean[m + 1][n + 1];
        dp[0][0] = true;
        for (int i = 0; i <= m; i++)
            for (int j = 0; j <= n; j++) {
                if (i > 0 && s1.charAt(i - 1) == s3.charAt(i + j - 1))
                    dp[i][j] = dp[i][j] || dp[i - 1][j];
                if (j > 0 && s2.charAt(j - 1) == s3.charAt(i + j - 1))
                    dp[i][j] = dp[i][j] || dp[i][j - 1];
            }
        return dp[m][n];
    }
}
```
```python
class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        m, n = len(s1), len(s2)
        if m + n != len(s3):
            return False
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True
        for i in range(m + 1):
            for j in range(n + 1):
                if i > 0 and s1[i - 1] == s3[i + j - 1]:
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
                if j > 0 and s2[j - 1] == s3[i + j - 1]:
                    dp[i][j] = dp[i][j] or dp[i][j - 1]
        return dp[m][n]
```

### Complexity
- **Time**: O(m × n).
- **Space**: O(m × n).

### Verdict
The canonical table. Each row reads only the row above and the current row's left, so it rolls to 1D.

---

## Approach 3 — 1D rolling row (space optimized) ⭐

### Intuition
Keep one boolean array `dp[j]` representing the current `i` row. `dp[j]` (before update) holds the "top" value `dp[i-1][j]`; `dp[j-1]` holds the freshly computed "left" `dp[i][j-1]`. Combine them with the matching conditions.

### Algorithm
1. Length check. `dp[0] = true`; seed the rest of row 0 from `s2` vs `s3`.
2. For each `i` from 1: update `dp[0]` (column 0 uses only `s1`); for `j` 1..n combine top (`dp[j]`) and left (`dp[j-1]`) with matches.
3. Return `dp[n]`.

### Code
```cpp
class Solution {
public:
    bool isInterleave(string s1, string s2, string s3) {
        int m = s1.size(), n = s2.size();
        if (m + n != (int)s3.size()) return false;
        vector<bool> dp(n + 1, false);
        dp[0] = true;
        for (int j = 1; j <= n; j++)
            dp[j] = dp[j - 1] && s2[j - 1] == s3[j - 1];
        for (int i = 1; i <= m; i++) {
            dp[0] = dp[0] && s1[i - 1] == s3[i - 1];
            for (int j = 1; j <= n; j++) {
                bool fromTop  = dp[j]     && s1[i - 1] == s3[i + j - 1];
                bool fromLeft = dp[j - 1] && s2[j - 1] == s3[i + j - 1];
                dp[j] = fromTop || fromLeft;
            }
        }
        return dp[n];
    }
};
```
```java
class Solution {
    public boolean isInterleave(String s1, String s2, String s3) {
        int m = s1.length(), n = s2.length();
        if (m + n != s3.length()) return false;
        boolean[] dp = new boolean[n + 1];
        dp[0] = true;
        for (int j = 1; j <= n; j++)
            dp[j] = dp[j - 1] && s2.charAt(j - 1) == s3.charAt(j - 1);
        for (int i = 1; i <= m; i++) {
            dp[0] = dp[0] && s1.charAt(i - 1) == s3.charAt(i - 1);
            for (int j = 1; j <= n; j++) {
                boolean fromTop  = dp[j]     && s1.charAt(i - 1) == s3.charAt(i + j - 1);
                boolean fromLeft = dp[j - 1] && s2.charAt(j - 1) == s3.charAt(i + j - 1);
                dp[j] = fromTop || fromLeft;
            }
        }
        return dp[n];
    }
}
```
```python
class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        m, n = len(s1), len(s2)
        if m + n != len(s3):
            return False
        dp = [False] * (n + 1)
        dp[0] = True
        for j in range(1, n + 1):
            dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]
        for i in range(1, m + 1):
            dp[0] = dp[0] and s1[i - 1] == s3[i - 1]
            for j in range(1, n + 1):
                from_top = dp[j] and s1[i - 1] == s3[i + j - 1]
                from_left = dp[j - 1] and s2[j - 1] == s3[i + j - 1]
                dp[j] = from_top or from_left
        return dp[n]
```

### Complexity
- **Time**: O(m × n).
- **Space**: O(n).

### Verdict
**The space-optimal answer.** One row of booleans.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Memoization | O(mn) | O(mn) | two-choice recursion |
| 2D table | O(mn) | O(mn) | canonical |
| 1D rolling | O(mn) | **O(n)** | space optimum ⭐ |

---

## 🧪 Edge cases & pitfalls
- **Length mismatch** (`m + n != |s3|`) → false immediately. Always check first.
- **All empty** → true (`dp[0][0]`).
- **One string empty** → reduces to "is `s3` equal to the other string."
- **Pitfall — greedy by single-char match**: when both `s1[i]` and `s2[j]` equal `s3[i+j]`, you must allow both branches. The DP's OR does this; a greedy pick can wrongly reject (e.g. `s1="aa", s2="a", s3="aaa"` style traps).
- **Pitfall — boundary seeding in 1D**: column 0 (`dp[0]`) and row 0 must be seeded from single-source prefix matches, and `dp[0]` must AND with the previous value as `i` grows.

---

## 🔗 Related problems
- **Longest Common Subsequence** (LC 1143) — sibling two-sequence grid.
- **Edit Distance** (LC 72) — two-sequence transformation DP.
- **Distinct Subsequences** (LC 115) — count embeddings of one string in another.
- **Scramble String** (LC 87) — recursive string interleaving/partition DP.

---

**→ Next:** [`08-Longest-Increasing-Path-Matrix.md`](./08-Longest-Increasing-Path-Matrix.md) | **→ Prev:** [`06-Maximal-Square.md`](./06-Maximal-Square.md) | Back to [`00-Index.md`](./00-Index.md)
