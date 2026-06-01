# 🧬 The LCS Family (Longest Common Subsequence)

> *"When two sequences meet, dp[i][j] is born."*

---

## I. LCS — the canonical 2D DP
`dp[i][j]` = LCS of A[0..i-1] and B[0..j-1].
```cpp
if (A[i-1] == B[j-1]) dp[i][j] = 1 + dp[i-1][j-1];
else                  dp[i][j] = max(dp[i-1][j], dp[i][j-1]);
```
O(nm) time, O(nm) space (→ O(min(n,m)) with rolling rows).

### Reconstructing the LCS
Backtrack from dp[n][m]: when chars match, take it and move diagonally; else move toward the larger neighbor.

---

## II. THE FAMILY

### Longest Common Substring (contiguous!)
Different from subsequence: `dp[i][j]` = length of common substring ENDING at (i,j); reset to 0 on mismatch. Answer = max over all cells.

### Shortest Common Supersequence (LC 1092)
Length = n + m − LCS(A,B). Reconstruct by merging via the LCS.

### Edit Distance (LC 72)
Min insert/delete/replace to turn A into B (see [`07-Edit-Distance-Family.md`](./07-Edit-Distance-Family.md)).

### Delete Operation for Two Strings (LC 583)
Min deletions to make equal = n + m − 2·LCS.

### Minimum ASCII Delete Sum (LC 712)
Like 583 but weighted by ASCII values.

### Longest Palindromic Subsequence (LC 516)
= LCS(s, reverse(s)). O(n²).

### Distinct Subsequences (LC 115)
Count subsequences of s equal to t (count, not length).

### Uncrossed Lines (LC 1035)
Literally LCS in disguise (connect equal numbers without crossing).

---

## III. THE 2D STRING DP TEMPLATE
```cpp
vector<vector<int>> dp(n+1, vector<int>(m+1, 0));
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= m; j++)
        if (A[i-1] == B[j-1]) dp[i][j] = /* match: usually 1 + diagonal */;
        else                  dp[i][j] = /* mismatch: max/min of neighbors */;
return dp[n][m];
```

---

## IV. SUBSEQUENCE VS SUBSTRING ⭐
- **Subsequence**: characters in order, gaps allowed → the dp uses max of neighbors on mismatch (carries best so far).
- **Substring**: contiguous → dp **resets to 0** on mismatch.

Getting this distinction right is the key to the whole family.

---

## V. SPACE OPTIMIZATION
Since `dp[i][*]` uses only `dp[i-1][*]` and the current row, keep two rows → O(m) space. (For reconstruction you need the full table or Hirschberg's O(min) divide-and-conquer.)

---

## VI. COMPLEXITY
- O(nm) time. For very long strings with small alphabet, bit-parallel methods (Hunt-Szymanski) can help, but O(nm) is standard.

---

## VII. PROBLEMS
- LCS (1143), Longest Common Substring
- Shortest Common Supersequence (1092)
- Delete Operation (583), Min ASCII Delete Sum (712)
- Longest Palindromic Subsequence (516)
- Distinct Subsequences (115)
- Uncrossed Lines (1035), Interleaving String (97)
- [CSES](https://cses.fi/problemset/) "Edit Distance"

---

**→ Next:** [`07-Edit-Distance-Family.md`](./07-Edit-Distance-Family.md)
