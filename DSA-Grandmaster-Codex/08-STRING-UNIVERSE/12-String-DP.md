# 🔤 String DP

> *"When two strings meet, dynamic programming is born."*

---

## I. THE CORE FAMILY
String DP problems usually have state `dp[i][j]` = answer considering prefixes/segments of one or two strings.

---

## II. THE CLASSIC PROBLEMS

### Longest Common Subsequence (LCS) — LC 1143
```
dp[i][j] = LCS of A[0..i-1], B[0..j-1]
if A[i-1]==B[j-1]: dp[i][j] = 1 + dp[i-1][j-1]
else:              dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```
O(nm).

### Edit Distance — LC 72
```
dp[i][j] = min edits to turn A[0..i-1] into B[0..j-1]
if match: dp[i][j] = dp[i-1][j-1]
else:     dp[i][j] = 1 + min(insert dp[i][j-1], delete dp[i-1][j], replace dp[i-1][j-1])
```

### Longest Palindromic Subsequence — LC 516
```
dp[i][j] = LPS in s[i..j]
if s[i]==s[j]: dp[i][j] = 2 + dp[i+1][j-1]
else:          dp[i][j] = max(dp[i+1][j], dp[i][j-1])
```
(= LCS of s and reverse(s))

### Distinct Subsequences — LC 115
Count subsequences of s equal to t. `dp[i][j]` with include/skip transitions.

### Wildcard Matching — LC 44 (`?` and `*`)
### Regular Expression Matching — LC 10 (`.` and `*`)
### Interleaving String — LC 97
### Shortest Common Supersequence — LC 1092 (length = n + m − LCS)
### Longest Common Substring (contiguous) — dp reset on mismatch

---

## III. THE TWO-STRING TEMPLATE
```cpp
int n = a.size(), m = b.size();
vector<vector<int>> dp(n+1, vector<int>(m+1, 0));
// base cases (row 0, col 0)
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= m; j++)
        if (a[i-1] == b[j-1]) dp[i][j] = /* match transition */;
        else                  dp[i][j] = /* mismatch transition */;
return dp[n][m];
```

### Space optimization
Most two-string DPs only use the previous row → reduce O(nm) space to O(m) with two 1D arrays.

---

## IV. PARTITION / PALINDROME DP
### Palindrome Partitioning II — LC 132 (min cuts)
- Precompute `isPalin[i][j]`.
- `dp[i]` = min cuts for s[0..i].

### Word Break — LC 139 / Word Break II — LC 140
- `dp[i]` = can s[0..i-1] be segmented into dictionary words?

---

## V. COUNTING STRING DP
- Count palindromic subsequences (LC 730)
- Distinct subsequences (LC 115, 940)
- Number of ways to form target from source

---

## VI. STRING DP + AUTOMATON (advanced)
- DP over (position, Aho-Corasick state) → count strings avoiding/containing patterns
- Digit-DP-style counting over strings

---

## VII. PROBLEMS (curated)
- LCS (1143), Edit Distance (72), Distinct Subsequences (115)
- Longest Palindromic Subsequence (516), Palindromic Substrings (647)
- Wildcard (44), Regex (10), Interleaving (97)
- Word Break I/II (139/140), Palindrome Partitioning II (132)
- Shortest Common Supersequence (1092), Min ASCII Delete Sum (712)
- Count Different Palindromic Subsequences (730)

---

## VIII. CROSS-REFERENCE
Full DP framework + all families: [`../06-DYNAMIC-PROGRAMMING-UNIVERSE/COMPENDIUM-Classical-DP.md`](../06-DYNAMIC-PROGRAMMING-UNIVERSE/COMPENDIUM-Classical-DP.md)

---

**→ Next:** [`13-Trie-Applications.md`](./13-Trie-Applications.md)
