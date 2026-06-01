# Distinct Subsequences

**Platform**: LeetCode 115 · **Difficulty**: Hard · **Topics**: String, Dynamic Programming · **Pattern**: Two-sequence DP (counting embeddings)

---

## 📜 Problem Statement

Given two strings `s` and `t`, return the **number of distinct subsequences of `s` which equals `t`**.

A **subsequence** of a string is a new string formed from the original by deleting some (possibly zero) characters without disturbing the relative positions of the remaining characters. (For example, `"ACE"` is a subsequence of `"ABCDE"` while `"AEC"` is not.)

The test cases are generated so that the answer **fits on a 32-bit signed integer**.

### Examples

**Example 1:**
```
Input:  s = "rabbbit", t = "rabbit"
Output: 3
Explanation: As shown below, there are 3 ways you can generate "rabbit" from s.
rabbbit  (delete the 3rd 'b')
rabbbit  (delete the 4th 'b')
rabbbit  (delete the 5th 'b')
```

**Example 2:**
```
Input:  s = "babgbag", t = "bag"
Output: 5
Explanation: As shown below, there are 5 ways you can generate "bag" from s.
babgbag (positions 0,1,2 -> b,a,g... etc.)
There are 5 distinct subsequences equal to "bag".
```

**Example 3:**
```
Input:  s = "abc", t = ""
Output: 1
Explanation: The empty string is a subsequence of any string exactly once
(by deleting everything).
```

### Constraints
```
1 <= s.length, t.length <= 1000
s and t consist of English letters.
```

---

## 🧠 Understanding the problem

We're counting **how many ways** the target `t` can be embedded as a subsequence of the source `s`. Two embeddings differ if they use a different set of positions in `s`.

Work prefix by prefix. Consider `dp[i][j]` = number of ways the first `i` characters of `s` can form the first `j` characters of `t`. For the latest source character `s[i-1]`:

- We can **always skip** `s[i-1]` and form `t[0..j)` from `s[0..i-1)` → contributes `dp[i-1][j]`.
- If `s[i-1] == t[j-1]`, we may also **use** `s[i-1]` to match `t[j-1]`, forming the rest `t[0..j-1)` from `s[0..i-1)` → contributes `dp[i-1][j-1]`.

So `dp[i][j] = dp[i-1][j] + (s[i-1]==t[j-1] ? dp[i-1][j-1] : 0)`. The "always skip" carry is what makes this *counting* rather than the boolean reachability of Interleaving String.

5-step framework:
1. **State**: `dp[i][j]` = number of subsequences of `s[0..i)` equal to `t[0..j)`.
2. **Transition**: `dp[i][j] = dp[i-1][j] + (match ? dp[i-1][j-1] : 0)`.
3. **Base case**: `dp[i][0] = 1` (the empty target is matched exactly once, by deleting everything); `dp[0][j>0] = 0`.
4. **Order**: increasing `i`, `j`.
5. **Answer**: `dp[m][n]`; collapses to 1D with a backward inner sweep.

---

## Approach 1 — Top-down memoization

### Intuition
`solve(i, j)` = ways to form `t[j:]` from `s[i:]`. If `t` is exhausted, that's one valid embedding. If `s` runs out first, zero. Otherwise skip `s[i]`, and if it matches `t[j]` also use it.

### Algorithm
1. If `j == n` (matched all of `t`), return 1.
2. If `i == m` (ran out of `s`), return 0.
3. `ways = solve(i+1, j)` (skip `s[i]`); if `s[i]==t[j]`, add `solve(i+1, j+1)`.
4. Memoize on `(i, j)`.

### Dry run on `s="rabbbit", t="rabbit"`
```
The 'b' run: t needs two b's, s has three.
Choosing which 2 of the 3 b's to keep -> C(3,2) = 3 ways
answer = 3
```

### Code
```cpp
class Solution {
    vector<vector<int>> memo;
    string s, t;
    int m, n;
    int solve(int i, int j) {
        if (j == n) return 1;
        if (i == m) return 0;
        if (memo[i][j] != -1) return memo[i][j];
        int ways = solve(i + 1, j);
        if (s[i] == t[j]) ways += solve(i + 1, j + 1);
        return memo[i][j] = ways;
    }
public:
    int numDistinct(string s, string t) {
        this->s = s; this->t = t; m = s.size(); n = t.size();
        memo.assign(m, vector<int>(n, -1));
        return solve(0, 0);
    }
};
```
```java
class Solution {
    private int[][] memo;
    private String s, t;
    private int m, n;
    private int solve(int i, int j) {
        if (j == n) return 1;
        if (i == m) return 0;
        if (memo[i][j] != -1) return memo[i][j];
        int ways = solve(i + 1, j);
        if (s.charAt(i) == t.charAt(j)) ways += solve(i + 1, j + 1);
        return memo[i][j] = ways;
    }
    public int numDistinct(String s, String t) {
        this.s = s; this.t = t; m = s.length(); n = t.length();
        memo = new int[m][n];
        for (int[] row : memo) java.util.Arrays.fill(row, -1);
        return solve(0, 0);
    }
}
```
```python
class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        from functools import lru_cache
        m, n = len(s), len(t)

        @lru_cache(maxsize=None)
        def solve(i: int, j: int) -> int:
            if j == n:
                return 1
            if i == m:
                return 0
            ways = solve(i + 1, j)
            if s[i] == t[j]:
                ways += solve(i + 1, j + 1)
            return ways

        return solve(0, 0)
```

### Complexity
- **Time**: O(m × n).
- **Space**: O(m × n) memo + recursion.

### Verdict
Reads like the definition. Bottom-up next.

---

## Approach 2 — Bottom-up 2D table

### Intuition
Fill `dp[i][j]`. The empty-target column is all 1s. Apply the carry-plus-match rule.

### Algorithm
1. `dp[i][0] = 1` for all `i`.
2. For `i` 1..m, `j` 1..n: `dp[i][j] = dp[i-1][j]`; if `s[i-1]==t[j-1]`, `dp[i][j] += dp[i-1][j-1]`.
3. Return `dp[m][n]`.

### Dry run on `s="babgbag", t="bag"` → 5
```
The empty column = 1s.
Each matching position accumulates counts from the diagonal of the previous row.
Final dp[m][n] = 5.
```

### Code
```cpp
class Solution {
public:
    int numDistinct(string s, string t) {
        int m = s.size(), n = t.size();
        vector<vector<unsigned long long>> dp(m + 1, vector<unsigned long long>(n + 1, 0));
        for (int i = 0; i <= m; i++) dp[i][0] = 1;
        for (int i = 1; i <= m; i++)
            for (int j = 1; j <= n; j++) {
                dp[i][j] = dp[i - 1][j];
                if (s[i - 1] == t[j - 1]) dp[i][j] += dp[i - 1][j - 1];
            }
        return (int)dp[m][n];
    }
};
```
```java
class Solution {
    public int numDistinct(String s, String t) {
        int m = s.length(), n = t.length();
        long[][] dp = new long[m + 1][n + 1];
        for (int i = 0; i <= m; i++) dp[i][0] = 1;
        for (int i = 1; i <= m; i++)
            for (int j = 1; j <= n; j++) {
                dp[i][j] = dp[i - 1][j];
                if (s.charAt(i - 1) == t.charAt(j - 1)) dp[i][j] += dp[i - 1][j - 1];
            }
        return (int) dp[m][n];
    }
}
```
```python
class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        m, n = len(s), len(t)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = 1
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                dp[i][j] = dp[i - 1][j]
                if s[i - 1] == t[j - 1]:
                    dp[i][j] += dp[i - 1][j - 1]
        return dp[m][n]
```

### Complexity
- **Time**: O(m × n).
- **Space**: O(m × n).

### Verdict
The canonical table. Row `i` reads only row `i-1`, so it collapses to a single 1D array.

---

## Approach 3 — 1D rolling array (space optimized) ⭐

### Intuition
Keep one array `dp[j]` over `t`'s prefixes. For each character of `s`, sweep `j` **from high to low**. The backward sweep ensures `dp[j-1]` still holds the *previous row's* value (the diagonal `dp[i-1][j-1]`) when we update `dp[j]` — exactly the term we need.

### Algorithm
1. `dp[0] = 1`, rest 0.
2. For each char `cs` of `s`, for `j` from `n` down to 1: if `cs == t[j-1]`, `dp[j] += dp[j-1]`.
3. Return `dp[n]`.

### Dry run on `s="rabbbit", t="rabbit"`
```
dp tracks counts per prefix of t.
The three b's each add to dp at the 'b' positions; combinatorially yields dp[n]=3.
```

### Code
```cpp
class Solution {
public:
    int numDistinct(string s, string t) {
        int n = t.size();
        vector<unsigned long long> dp(n + 1, 0);
        dp[0] = 1;
        for (char cs : s)
            for (int j = n; j >= 1; j--)
                if (cs == t[j - 1]) dp[j] += dp[j - 1];
        return (int)dp[n];
    }
};
```
```java
class Solution {
    public int numDistinct(String s, String t) {
        int n = t.length();
        long[] dp = new long[n + 1];
        dp[0] = 1;
        for (int i = 0; i < s.length(); i++) {
            char cs = s.charAt(i);
            for (int j = n; j >= 1; j--)
                if (cs == t.charAt(j - 1)) dp[j] += dp[j - 1];
        }
        return (int) dp[n];
    }
}
```
```python
class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        n = len(t)
        dp = [0] * (n + 1)
        dp[0] = 1
        for cs in s:
            for j in range(n, 0, -1):
                if cs == t[j - 1]:
                    dp[j] += dp[j - 1]
        return dp[n]
```

### Complexity
- **Time**: O(m × n).
- **Space**: O(n).

### Verdict
**The space-optimal answer.** The backward `j` sweep is essential — it preserves the diagonal term, just like the 0/1 knapsack sweep preserves "use each item once."

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Memoization | O(mn) | O(mn) | skip + match recursion |
| 2D table | O(mn) | O(mn) | canonical |
| 1D rolling array | O(mn) | **O(n)** | backward sweep ⭐ |

---

## 🧪 Edge cases & pitfalls
- **Empty target** (`t = ""`) → 1: there's exactly one way to match the empty string (delete everything). This is the `dp[*][0] = 1` base case.
- **`t` longer than `s`** → 0 (can't embed a longer string).
- **`s == t`** → 1.
- **Pitfall — forward sweep in 1D**: sweeping `j` ascending would let `dp[j-1]` already be updated for the *current* row, double-counting. Must sweep `j` **downward**.
- **Pitfall — overflow**: intermediate counts can exceed 32-bit even though the final answer fits. Use 64-bit accumulators (`long` / `unsigned long long`) and cast at the end. (Python integers are unbounded.)
- **Pitfall — the carry term**: `dp[i][j]` always inherits `dp[i-1][j]` (skip), regardless of whether characters match. Forgetting the unconditional carry undercounts.

---

## 🔗 Related problems
- **Longest Common Subsequence** (LC 1143) — measure (not count) the shared subsequence.
- **Interleaving String** (LC 97) — boolean two-sequence reachability (no counting carry).
- **Edit Distance** (LC 72) — transform one string into another.
- **Wildcard Matching** (LC 44) / **Regular Expression Matching** (LC 10) — pattern matching grids.

---

**→ Next topic:** [`../15-Greedy/00-Index.md`](../15-Greedy/00-Index.md) | **← Prev:** [`10-Zero-One-Knapsack.md`](./10-Zero-One-Knapsack.md) | Back to [`00-Index.md`](./00-Index.md)
