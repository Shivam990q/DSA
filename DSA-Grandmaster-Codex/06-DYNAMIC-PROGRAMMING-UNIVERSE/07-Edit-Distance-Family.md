# 🧬 Edit Distance Family

> *"How far apart are two strings? Count the edits."*

---

## I. EDIT DISTANCE (Levenshtein) — LC 72
Min insertions/deletions/substitutions to turn A into B.
```cpp
// dp[i][j] = edit distance between A[0..i-1] and B[0..j-1]
for (int i = 0; i <= n; i++) dp[i][0] = i;   // delete all
for (int j = 0; j <= m; j++) dp[0][j] = j;   // insert all
for (int i = 1; i <= n; i++)
  for (int j = 1; j <= m; j++)
    if (A[i-1] == B[j-1]) dp[i][j] = dp[i-1][j-1];        // match, free
    else dp[i][j] = 1 + min({dp[i-1][j],    // delete from A
                             dp[i][j-1],    // insert into A
                             dp[i-1][j-1]});// substitute
```
O(nm) time, O(min(n,m)) space (rolling).

---

## II. THE FAMILY

### One Edit Distance (LC 161)
Boolean: are A and B exactly one edit apart? O(n) two-pointer.

### Delete Operation for Two Strings (LC 583)
Only deletions allowed → n + m − 2·LCS.

### Minimum ASCII Delete Sum (LC 712)
Weighted deletions by ASCII value.

### Wildcard Matching (LC 44) — `?` and `*`
- `?` matches any single char.
- `*` matches any sequence (including empty).
```
if p[j]=='*': dp[i][j] = dp[i-1][j] (star consumes a char) || dp[i][j-1] (star matches empty)
elif p[j]=='?' or match: dp[i][j] = dp[i-1][j-1]
```

### Regular Expression Matching (LC 10) — `.` and `*`
- `.` matches any single char.
- `*` matches zero or more of the **preceding** element.
```
if p[j+1]=='*': dp[i][j] = dp[i][j+2] (zero) || (match(i,j) && dp[i+1][j])  (one+)
else: dp[i][j] = match(i,j) && dp[i+1][j+1]
```
The trickiest of the family — handle the `x*` pair carefully.

### Interleaving String (LC 97)
Can C be formed by interleaving A and B? `dp[i][j]` over prefixes.

### Distinct Subsequences (LC 115)
Count ways A's subsequences equal B.

---

## III. THE COMMON SKELETON
All are `dp[i][j]` over the two strings' prefixes; differ only in the transition (which operations are allowed and their cost/count).

---

## IV. INTERVIEW TIPS
- **Edit Distance** and **Regex Matching** are top-tier interview problems (Google, Meta).
- Draw the dp grid; fill base cases (empty string rows/cols) first.
- For `*` in regex, the "zero occurrences" branch is the one people forget.

---

## V. COMPLEXITY
O(nm) time; O(min(n,m)) space with rolling rows (full table if reconstruction needed).

---

## VI. PROBLEMS
- Edit Distance (72) ⭐, One Edit Distance (161)
- Delete Operation (583), Min ASCII Delete Sum (712)
- Wildcard Matching (44) ⭐, Regular Expression Matching (10) ⭐⭐
- Interleaving String (97), Distinct Subsequences (115)
- [CSES](https://cses.fi/problemset/) "Edit Distance"

---

**→ Next:** [`08-Stocks-DP.md`](./08-Stocks-DP.md)
